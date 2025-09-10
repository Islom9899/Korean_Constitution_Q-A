import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
import os
from langchain.vectorstores import FAISS
from deep_translator import GoogleTranslator
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

load_dotenv()
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    vectorstore = FAISS.from_documents(
    split_docs,
    OpenAIEmbeddings(model='text-embedding-3-small')
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
st.sidebar.header("⚙️ Settings")
language = st.sidebar.selectbox("🌍 Language", ("한국어", "English", "Oʻzbekcha"))
option = st.sidebar.selectbox("🤖 Select Model", ("gpt-4o-mini", "gpt-3.5-turbo"))
rag_chain = initialize_components(option)

chat_history = StreamlitChatMessageHistory(key="chat_messages")

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="history",
    output_messages_key="answer",
)

# ----------------------
# Translate Helper
# ----------------------
def translate_text(text, src, tgt):
    try:
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except:
        return text

# ----------------------
# UI Header
# ----------------------
st.title("헌법 Q&A Chatbot 💬📘")
st.write("Ask questions about the Korean Constitution in **Korean, English, or Uzbek**.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "헌법에 대해 무엇이든 물어보세요! (Ask me anything about the Constitution)"}
    ]

# ----------------------
# Chat Display
# ----------------------
for msg in chat_history.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt_message := st.chat_input("Your question..."):
    # Detect source language
    src_lang = "auto"
    tgt_lang = "ko"  # Always query in Korean
    
    translated_question = translate_text(prompt_message, src_lang, tgt_lang)

    st.chat_message("human").write(prompt_message)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            config = {"configurable": {"session_id": "any"}}
            response = conversational_rag_chain.invoke({"input": translated_question}, config=config)

            # Translate back to selected language
            answer = response["answer"]
            if language == "English":
                answer = translate_text(answer, "ko", "en")
            elif language == "Oʻzbekcha":
                answer = translate_text(answer, "ko", "uz")

            st.write(answer)

            with st.expander("📄 Sources"):
                for doc in response["context"]:
                    st.markdown(f"**Source:** {doc.metadata['source']}", help=doc.page_content)

# ----------------------
# Download Q&A History
# ----------------------
if st.sidebar.button("⬇️ Download Chat"):
    history_text = "\n".join([f"{m.type.upper()}: {m.content}" for m in chat_history.messages])
    st.sidebar.download_button("Download Q&A as TXT", history_text, file_name="chat_history.txt")
