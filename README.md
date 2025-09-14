# 📘 헌법 Q&A 챗봇 – 대한민국 헌법 프로젝트

이 프로젝트는 **대한민국 헌법**에 대한 질문을 다양한 언어(한국어, 영어, 우즈벡어)로 입력하면, AI가 관련 내용을 검색하고 답변해주는 **지능형 챗봇**입니다.  
PDF 형식의 헌법 문서를 벡터화하여 질문에 적합한 문서를 검색(RAG)하고, 답변은 한국어로 제공됩니다. 사용자 언어로 번역도 지원합니다.

---
Demo-https://koreanconstitutionq-a.streamlit.app/
## 🚀 주요 기능

- 📄 헌법 PDF 문서를 분할 및 벡터화
- 🤖 GPT-4o / GPT-3.5-turbo 기반의 응답 생성
- 🌐 다국어 지원 (한국어, 영어, 우즈벡어)
- 🧠 LangChain 기반 문서 검색 및 대화 흐름 관리
- 💬 대화 기록 다운로드 기능
- 📚 출처 문서 표시 (출처 링크 및 페이지 정보)

---

## 🧩 사용된 기술

- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS / Chroma 벡터DB
- Deep Translator (Google 번역기)
- dotenv 환경변수

---

## ⚙️ 설치 및 실행 방법

### 1. 프로젝트 클론

```bash
git clone https://github.com/Islom9899/Korean_Constitution_Q-A.git
cd Korean_Constitution_Q-A
```

### 2. 가상 환경 설정 및 활성화

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
# 또는
venv\Scripts\activate          # Windows
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=your_project_name
```

---

## ▶️ 실행 방법

```bash
streamlit run manabu_app.py
```

앱 실행 후 브라우저에서 다음을 선택하세요:

1. 좌측에서 언어 선택: 🇰🇷 한국어 | 🇺🇸 영어 | 🇺🇿 우즈벡어
2. 모델 선택: `gpt-4o-mini` 또는 `gpt-3.5-turbo`
3. 질문 입력 → 자동 번역 및 응답 생성
4. 응답은 항상 한국어로 제공되며, 선택한 언어로 다시 번역되어 표시됩니다
5. 대화 내용은 `.txt` 파일로 다운로드 가능

---

## 📂 프로젝트 구조

```
├── app.py           # Streamlit 애플리케이션 코드
├── requirements.txt        # 필수 라이브러리 목록
├── .env.example            # 환경 변수 예시 파일
├── 대한민국헌법.pdf         # 분석 대상 헌법 문서
└── chroma_db/              # 벡터 DB 저장 디렉토리 (FAISS 또는 Chroma)
```

---

## 👨‍💻 개발자 정보

**이름:** MANSUROV ISLOM  
**이메일:** [mansurovislom2@gmail.com](mailto:mansurovislom2@gmail.com)

---

## 🤝 기여 방법

오픈소스 프로젝트에 기여하고 싶으시다면 다음 단계를 따라 주세요:

1. 이 저장소를 **Fork** 합니다
2. 새로운 브랜치를 만듭니다: `feature/내이름`
3. 기능을 추가하거나 버그를 수정합니다
4. **Pull Request**를 생성하여 제출합니다

---

## 📄 라이선스

이 프로젝트는 학습 및 비상업적 연구 목적으로 사용 가능합니다. 상업적 이용을 원하시면 먼저 개발자에게 문의해 주세요.

---





