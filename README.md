# CCMI GenAI Chatbot

> Team-specific AI assistant powered by Google Gemini, specialized for CCMI data analytics and Excel automation.

[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF0000?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Gemini_API](https://img.shields.io/badge/Gemini-1.5_Flash-4285F4?style=flat-square&logo=google)](https://ai.google.dev/)

---

## Overview

CCMI GenAI Chatbot is a custom-built Streamlit application developed specifically for the CCMI Systems & Data Team. This specialized AI assistant leverages Google's Gemini 1.5-Flash model with advanced prompt engineering to support data analysts with Excel-related challenges, Power Query solutions, VBA scripting, M code, and Power BI DAX queries.

The application demonstrates the power of tailored prompt engineering to align large language model behavior with specific team workflows, communication styles, and technical requirements. It provides a conversational interface to accelerate problem-solving and knowledge sharing within the team.

---

## Features

- Specialized assistance for data analytics and Excel automation
- Expert guidance on VBA, Power Query, M code, and Power BI DAX
- Conversational chat interface with conversation history
- Real-time code suggestions and explanations
- Context-aware responses tailored to CCMI workflows
- Responsive dark and light theme support
- Secure API key management via Streamlit Secrets
- Professional custom styling
- Message persistence within session
- Code block formatting with syntax highlighting

---

## Screenshots

> Drop screenshots into `screens/` or the root and they'll render here.

![CCMI GenAI Chatbot](images/screen.jpg)

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- Streamlit Community Cloud account (for deployment)

### Installation

```bash
git clone https://github.com/Naadir-Dev-Portfolio/Streamlit-ccmi-genai.git
cd Streamlit-ccmi-genai
pip install -r requirements.txt
```

### Configuration

1. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Create `.streamlit/secrets.toml`:

```toml
gemini_api_key = "YOUR_GEMINI_API_KEY_HERE"
```

3. (Optional) Customize the system prompt in `main.py` to tailor assistant behavior further

### Run Locally

```bash
streamlit run main.py
```

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Connect to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Add your Gemini API key to Streamlit Secrets
4. Deploy and share with your team

---

## Tech Stack

- Python 3.7+ — Core application
- Streamlit — Web UI framework
- google-generativeai — Gemini API SDK
- Advanced Prompt Engineering — Specialized system instructions
- Streamlit Cloud — Deployment
- Git/GitHub — Version control

---

## How It Works

1. Type your question or describe your technical challenge
2. The AI processes your query using CCMI-specialized prompt instructions
3. Receive expert guidance, code samples, and explanations
4. Ask follow-up questions for clarification
5. Conversation history is maintained during your session
6. Copy code snippets directly from the responses

---

## Specializations

The chatbot excels in these areas:

- **Excel & VBA** — Macro development, automation, and troubleshooting
- **Power Query** — Data transformation, M language expertise
- **Power BI DAX** — Advanced calculations and measure creation
- **Data Analysis** — SQL, Python, and analytics workflows
- **Power Apps** — Low-code app development support
- **Team Processes** — CCMI-specific workflows and standards

---

## Related Projects

- [Streamlit-AIQuizbot](https://github.com/Naadir-Dev-Portfolio/Streamlit-AIQuizbot)
- [Website-ccmi-team-site](https://github.com/Naadir-Dev-Portfolio/Website-ccmi-team-site)
