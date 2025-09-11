헌법 Q&A 챗봇 💬📚
--본 프로젝트는 개인적으로 개발한 RAG(Retrieval-Augmented Generation) 기반 인공지능 챗봇으로, 대한민국 헌법 PDF 데이터를 기반으로 질의응답 기능을 제공합니다.
LangChain 프레임워크와 OpenAI 모델을 활용하여, 헌법 관련 질문에 대해 정확하고 맥락을 반영한 답변을 생성하도록 설계되었습니다.
📌 주요 기능
--문서 임베딩 및 검색: 헌법 PDF를 세분화하여 벡터 데이터베이스(ChromaDB)에 저장 및 검색
맥락 기반 답변 생성: 대화 이력을 반영한 질의응답 처리
효율적 성능 관리: Streamlit 캐싱을 통한 최적화된 응답 속도
대화형 사용자 인터페이스: Streamlit 기반 직관적 UI 제공
--⚙️ 기술 스택
언어: Python
프레임워크: LangChain, Streamlit
AI 모델: OpenAI GPT API
Vector DB: ChromaDB
--🎯 프로젝트 의의
본 프로젝트는 법률 문서를 대상으로 한 AI 기반 정보 검색 및 대화 시스템의 가능성을 검증하는 사례입니다.
데이터 로딩, 임베딩, 검색, 답변 생성을 포함한 전 과정을 독자적으로 구현하여, 엔드투엔드 AI 솔루션 설계 및 개발 역량을 보여줍니다.
https://koreanconstitutionq-a.streamlit.app/
-----------------------------------------------------------
-----------------------------------------------------------
Constitution Q&A Chatbot 💬📚
--This project is an individually developed AI-powered chatbot utilizing Retrieval-Augmented Generation (RAG) to provide question-answering functionality based on the Constitution of the Republic of Korea.
Leveraging the LangChain framework and OpenAI models, it is designed to generate accurate and context-aware answers to constitutional queries.
--📌 Key Features
Document Embedding & Retrieval: Splits constitutional PDFs and stores them in ChromaDB for semantic search
Context-Aware Response Generation: Incorporates conversational history for enhanced accuracy
Optimized Performance: Accelerated response with Streamlit caching mechanisms
Conversational User Interface: Intuitive and accessible UI built with Streamlit
--⚙️ Tech Stack
Language: Python
Frameworks: LangChain, Streamlit
AI Models: OpenAI GPT API
Vector DB: ChromaDB
--🎯 Project Significance
This project serves as a demonstration of applying AI-driven information retrieval and dialogue systems to legal documents.
The full pipeline — from document ingestion, embedding, and retrieval to response generation — has been independently developed, highlighting end-to-end AI solution design and implementation capabilities.
demo: https://koreanconstitutionq-a.streamlit.app/
