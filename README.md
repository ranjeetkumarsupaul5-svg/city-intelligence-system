# 🌆 City Intelligence System

An AI-powered city information assistant built with **Python, FastAPI, LangChain, Groq, OpenWeather API, and Tavily Search**.

The system allows users to ask questions about a city and provides useful information such as current weather and latest news through AI-powered tool calling.

## ✨ Features

* 🤖 AI-powered city assistant
* 🌤️ Real-time weather information
* 📰 Latest city news using Tavily Search
* 🔧 LangChain tool calling
* ⚡ FastAPI backend
* 💻 HTML, CSS and JavaScript frontend
* 🌌 Modern futuristic dashboard UI
* 📱 Responsive interface
* 📊 Live activity updates

## 🛠️ Technologies Used

### Backend

* Python
* FastAPI
* LangChain
* Groq
* OpenWeather API
* Tavily Search

### Frontend

* HTML5
* CSS3
* JavaScript

## 📁 Project Structure

```text
city-intelligence-system/
│
├── backend/
│   ├── __init__.py
│   ├── createAgents.py
│   └── main.py
│
├── frontend/
│   ├── assets/
│   │   └── night-sky.jpg
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your `.env` file or API keys to GitHub.**

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ranjeetkumarsupaul5-svg/city-intelligence-system.git
cd city-intelligence-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API keys

Create `.env` and add the required API keys.

### 5. Start the backend

```bash
uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 6. Open the frontend

Open:

```text
frontend/index.html
```

in your browser.

## 🔌 APIs Used

* **Groq** — AI language model
* **OpenWeather** — Current weather data
* **Tavily** — Web/news search

## 📌 Future Improvements

* City-based dashboard customization
* More real-time city data
* Additional information tools
* Production deployment
* Improved analytics and visualization

## 👨‍💻 Author

**Ranjeet Kumar**

GitHub:
https://github.com/ranjeetkumarsupaul5-svg

## 📄 License

This project is intended for educational and portfolio purposes.
