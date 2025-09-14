
# Travel Assistant Chatbot

An interactive multi-agent chatbot built with **Chainlit** and **Google Gemini API**, designed to assist users with travel-related queries such as Hotels, Transport, and Food services.

---

## Features

- **Triage Agent:** Categorizes user queries into Hotels, Transport, or Food.  
- **Guardrail Agent:** Ensures questions are travel-related and prevents irrelevant queries.  
- **Department Agents:**  
  - **Hotel Representative** – Handles hotel-related questions.  
  - **Transport Representative** – Handles transport-related questions.  
  - **Food Representative** – Handles food-related queries.  
- **Async Handling:** Powered by asynchronous agents for efficient processing.  
- **Integration with Gemini API:** Uses `gemini-2.5-flash` model for natural language understanding.  

---

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

2. **Create a virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

Start the chatbot using **Chainlit**:

```bash
chainlit run main.py
```

- On chat start, the bot will greet the user:
```
👋 Hi! I am your Travel Assistant. Ask me about Hotels, Transport, or Food.
```

- Ask a question about travel, and the **Triage Agent** will categorize it.  
- The appropriate **department agent** will respond with detailed guidance.  
- If a query is not travel-related, the **Guardrail** will block it.

---

## Project Structure

- `main.py` – Main chatbot application.  
- `agents.py` – Definitions for agents, guardrails, and runner logic.  
- `.env` – Environment variables (Gemini API key).  
- `requirements.txt` – Python dependencies.  

---

## Dependencies

- [Chainlit](https://www.chainlit.io/) – For chat UI and event handling.  
- [Pydantic](https://pydantic-docs.helpmanual.io/) – Data validation for guardrail outputs.  
- [Python Dotenv](https://pypi.org/project/python-dotenv/) – Load environment variables.  
- Google Gemini API (`gemini-2.5-flash`) – Language model for AI responses.  

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Chainlit](https://www.chainlit.io/)  
- Google Gemini API  
