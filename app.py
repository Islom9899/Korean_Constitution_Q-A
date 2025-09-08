import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
import os
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

openai_api_key = st.secrets["openai"]["api_key"]
os.environ['OPENAI_API_KEY'] = openai_api_key

# LangChain API parametrlari
lc_api_key = st.secrets["langchain"]["api_key"]
lc_endpoint = st.secrets["langchain"]["endpoint"]
lc_project = st.secrets["langchain"]["project"]

@st.cache_resource # 한번 실행한 결과를 캐싱해서 재실행시 빠르게 로드
def loader_and_split_pdf(file_path):
    """PDF 로드 함수"""
    loader = PyPDFLoader(file_path)
    return loader.load_and_split()

@st.cache_resource
def create_vector_store(_docs):
    """텍스트 청크들을 임베딩 벡터로 저장"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    split_docs = text_splitter.split_documents(_docs)
    persist_directory = './chroma_db'
    vectorstore = Chroma.from_documents(split_docs,OpenAIEmbeddings(model='text-embedding-3-small'),
                                        persist_directory=persist_directory
                                        )
    return vectorstore

@st.cache_resource
def get_vectorstore(_docs):
    """만약 기존의 저장해둔 벡터db가 있는 경우, 이를 불러온다(로드)"""
    persist_directory = './chroma_db'
    if os.path.exists(persist_directory):
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=OpenAIEmbeddings(model='text-embedding-3-small')
        )
    else:
        return create_vector_store(_docs)

@st.cache_resource
def initialize_components(selected_model):
    file_path = '대한민국헌법(헌법)(제00010호)(19880225).pdf'
    pages = loader_and_split_pdf(file_path)
    vectorstore = get_vectorstore(pages)
    retriever = vectorstore.as_retriever()
    
# 채팅 히스토리 요약 시스템 프롬프트
    contextualize_q_system_prompt = '''Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is.'''
    contextualize_q_system_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', contextualize_q_system_prompt),
            MessagesPlaceholder('history'),
            ('human', '{input}'),
        ]
    )
    
    # 질문-답변 시스템 프롬프트
    qa_system_prompt = '''You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Keep the answer perfect. please use imogi with the answer.
    대답은 한국어로 하고, 존댓말을 써줘.\

    {context}
    '''
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', qa_system_prompt),
            MessagesPlaceholder('history'),
            ('human', '{input}'),
        ]
    )
    
    llm = ChatOpenAI(model=selected_model)
    # 대화 히스토리를 고려해서
    history_aware_retriever = create_history_aware_retriever(llm,
                                                             retriever,
                                                             contextualize_q_system_prompt
                                                             )
    # 검색된 문서로 답변 생성
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # 검색과 생성을 연결하는 최종 체인
    rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)
    
    return rag_chain
# -----------------------
# Streamlit UI
st.header('헌법 Q&A 챗봇 💬 📚')

option = st.selectbox('Select GPT Model', ('gpt-4o-mini', 'gpt-3.5-turbo'))
rag_chain = initialize_components(option)
chat_history = StreamlitChatMessageHistory(key='chat_messages')

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: chat_history,
    input_messages_key='input',
    history_messages_key='history',
    output_messages_key='answer',
)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'assistant',
         'content': '한법에 대해 무엇이든 물어보세요!'}
    ]
    
for msg in chat_history.messages:
    st.chat_message(msg.type).write(msg.content)
    
if prompt_message := st.chat_input('Your question'):
    st.chat_message('human').write(prompt_message)
    with st.chat_message('ai'):
        with st.spinner('Thinking...'):
            config = {'configurable': {'session_id': 'any'}}
            response = conversational_rag_chain.invoke(
                {'input': prompt_message},
                config=config
            )
            answer = response['answer']
            st.write(answer)
            with st.expander('참고 문서 확인'):
                for doc in response['context']:
                    st.markdown(doc.metadata['source'], help=doc.page_content)
