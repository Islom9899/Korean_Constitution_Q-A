# 🇰🇷 Korean Constitution Q&A Chatbot  

AI-powered **multilingual chatbot** that answers questions about the **Constitution of the Republic of Korea** using **Retrieval-Augmented Generation (RAG)**.  
Built with **LangChain, OpenAI GPT API, FAISS/ChromaDB, Deep Translator, and Streamlit** for accurate, context-aware, and multilingual responses.  

🌐 [Live Demo](https://koreanconstitutionq-a.streamlit.app/)  

---

## ✨ Features  
- 📖 **Contextual Q&A**: Understands and answers questions based on the Korean Constitution PDF.  
- 🔎 **RAG-based Search**: Retrieves the most relevant passages before generating an answer.  
- 🌍 **Multilingual Support**:  
  - 🇰🇷 Korean  
  - 🇺🇸 English  
  - 🇺🇿 Uzbek  
- ⚡ **Hybrid Vector DB**: FAISS + ChromaDB for efficient similarity search.  
- 🖥 **User-friendly UI**: Built with Streamlit, sidebar settings, and expandable sources.  
- 📥 **Export Chat**: Download full Q&A conversation as a `.txt` file.  

---

## 🛠️ Tech Stack  
- **Framework**: LangChain  
- **Models**: OpenAI GPT (gpt-4o-mini, gpt-3.5-turbo)  
- **Embeddings**: text-embedding-3-small  
- **Vector Store**: FAISS + ChromaDB  
- **Translation**: Deep Translator (Google Translate API)  
- **Frontend**: Streamlit  
- **Language**: Python  

---

## 📂 Project Structure  
```bash
Korean_Constitution_Q-A/
│── app.py               # Main Streamlit app
│── requirements.txt     # Dependencies
│── README.md            # Documentation
│── data/                # Constitution PDFs
│── vectorstore/         # FAISS / ChromaDB index

---

# 🚀 Getting Started
## Clone the repository
git clone https://github.com/your-username/Korean_Constitution_Q-A.git
cd Korean_Constitution_Q-A






