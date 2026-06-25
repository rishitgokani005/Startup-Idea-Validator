# 🚀 Multi-Agent Startup Idea Validator

An elite AI-driven validation tool that uses a panel of specialized agents (VC, Customer, Growth Expert, Technical Architect) to audit and score your startup ideas.

## Features
- **Multi-Agent Orchestration**: Four distinct AI roles provide specialized feedback.
- **Synthesized Verdict**: A Lead Synthesizer Agent consolidates feedback into a final score and GO/NO-GO recommendation.

## Tech Stack
- **Frontend**: Streamlit
- **AI Models**: Llama 3 via Groq Cloud
- **Orchestration**: Custom Python Agents

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rishitgokani005/Startup-Idea-Validator.git
   cd Startup-Idea-Validator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app/frontend.py
   ```
