# text-summarizer

# 📘 AI Notes Generator (Groq Powered)

AI Notes Generator is a **student-friendly AI web application** that converts long text and PDF files into **smart, exam-ready study notes** using Groq LLM.  
It helps students save time, improve revision, and generate structured notes instantly.

---

## 🚀 Live Features

✅ Convert text into structured AI notes  
✅ Upload PDF files and summarize content  
✅ Exam-focused bullet point notes  
✅ Download generated notes as PDF  
✅ Daily usage limit protection  
✅ Token usage tracking  
✅ Mobile-friendly UI  
✅ Beautiful dark theme dashboard  
✅ History of generated notes  

---

## 🧠 How It Works

User Input (Text / PDF)
↓
Groq LLM API
↓
AI Processes Content
↓
Structured Study Notes Output
↓
PDF Download + History Save


---

## 🛠 Tech Stack

### Frontend + Backend
- Streamlit (Web UI)
- Python

### AI Model
- Groq API
- llama-3.1-8b-instant

### Libraries Used
- streamlit  
- groq  
- python-dotenv  
- pypdf  
- reportlab  
- tiktoken  

---

## 📂 Project Structure

groq-text-summarizer/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
├── data/
│ └── history.txt
└── downloads/



---

## ⚙ Installation Guide

###  Clone Repository

bash
git clone https://github.com/Aryan-Bose/text-summarizer
cd groq-text-summarizer

## Create Virtual Environment
python -m venv venv

### Activate Virtual Environment

Windows:
source venv/Scripts/activate

Mac/Linux:
source venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Add Groq API Key
Create .env file:

GROQ_API_KEY=your_api_key_here

## Run Application
streamlit run app.py

## Open browser:

http://localhost:8501





