# 🎬 VideoSummarizer

**VideoSummarizer** is a Python-based system that transcribes speech from short videos and generates concise text summaries using NLP techniques and large language models (LLMs).

---

## 🚀 Getting Started

### 🧰 Prerequisites

Make sure you have the following tools installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)

---

### 📦 Clone the Repository

Navigate to the directory where you want to store the project and run:

```bash
git clone https://github.com/WiktorPodwin/VideoSummarizer.git
cd VideoSummarizer
```

## Create a file for environment variables
Create .env file and fill it in the same way as .env.example file (you can change user, password and db by your own)

## Libraries
In main project directory (VideoSummarizer)
```bash
pip install -r requirements.txt
```

## Create containerized database
```bash
docker compose up --build
```

## Initialize tables in a database
```bash
python setup.py
```

## Run app
```bash
streamlit run app.py
```