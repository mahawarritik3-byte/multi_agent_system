# 🤖 Multi-Agent Research System

An AI-powered **Multi-Agent Research Assistant** built using **LangGraph**, **LangChain**, **OpenAI GPT**, **Tavily Search API**, and **BeautifulSoup**. The system intelligently researches a given topic by combining web search with webpage scraping and produces well-structured, comprehensive reports.

---

## 🚀 Features

- 🔍 AI-powered web research using Tavily Search API
- 🌐 Webpage scraping with BeautifulSoup
- 🤖 Multiple specialized AI agents
- 🔄 Agent collaboration using LangGraph
- 📄 Automatic report generation
- 💬 Interactive Streamlit interface
- ⚡ Fast and structured research workflow

---

## 🏗️ System Architecture

```
                User Query
                     │
                     ▼
             Research Coordinator
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
  Web Search Agent          Web Scraper Agent
   (Tavily API)            (BeautifulSoup)
        │                         │
        └────────────┬────────────┘
                     ▼
             Research Analyzer
                     │
                     ▼
              Final Report Agent
                     │
                     ▼
                Streamlit UI
```

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- LangChain
- LangGraph

### AI Model
- OpenAI GPT Models

### APIs
- OpenAI API
- Tavily Search API

### Libraries
- BeautifulSoup4
- Requests
- Python-dotenv

---

## 📂 Project Structure

```
multi-agent-system/
│
├── agents/
│   ├── researcher.py
│   ├── analyzer.py
│   └── report_writer.py
│
├── tools/
│   ├── web_search.py
│   └── web_scraper.py
│
├── graph/
│   └── workflow.py
│
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-agent-system.git

cd multi-agent-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key

TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

---

## 🧠 Workflow

1. User enters a research topic.
2. Research Agent searches the web using Tavily.
3. Scraper Agent extracts information from webpages.
4. Analyzer Agent summarizes and filters the content.
5. Report Agent generates a detailed final report.
6. Streamlit displays the results.

---

## 📷 Demo

### Home Page

Add screenshot here

```
images/home.png
```

### Generated Report

Add screenshot here

```
images/report.png
```

---

## 📦 Requirements

- Python 3.10+
- OpenAI API Key
- Tavily API Key

---

## 🔮 Future Improvements

- PDF report export
- Citation generation
- Multi-source verification
- Memory-enabled conversations
- Support for multiple LLM providers
- Research history
- Document upload support
- Parallel agent execution
- Report sharing

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Ritik Mahawar**

- GitHub: https://github.com/mahawarritik3-byte
- LinkedIn: https://linkedin.com/in/ritik-mahawar-b313a6282

---

## ⭐ If you found this project useful, don't forget to star the repository!
