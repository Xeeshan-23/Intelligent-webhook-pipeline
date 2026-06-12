# FlexiFlow-AI: Intelligent Webhook Data Pipeline

FlexiFlow-AI is a production-ready, asynchronous web gateway built with **FastAPI** and **Python** that transforms rigid, error-prone business automations into flexible, **semantic data pipelines**. 

By orchestrating the **Google Gemini AI Engine** with native **Pydantic v2 Structured Outputs**, FlexiFlow-AI automatically captures unstructured natural language payloads (such as messy incoming customer emails or raw lead alerts), converts them into validated corporate data schemas, and safely streams them to destination CRMs using asynchronous background queue workers with exponential back-off resilience.

---

##  Key Architectural Features

* **Instantaneous 200 OK Edge Ingestion:** Webhook endpoints accept incoming HTTP requests immediately and offload heavy processing to internal background threads via FastAPI `BackgroundTasks`, eliminating client-side timeouts.
* **Semantic AI Orchestration Layer:** Integrates the modern `google-genai` SDK (`gemini-2.5-flash`) using strict JSON schema constraints. Messy text is deterministically parsed into structural code schemas on the fly.
* **Strict Type Safety & Validation:** Leverages **Pydantic v2** (`EmailStr`, `Field` metadata) to enforce data validation at runtime before any downstream mutations occur.
* **Defensive Pipeline Engineering:** Implements an exponential back-off retry queue worker. If external webhooks or CRMs experience intermittent downtime, the system backs off gracefully rather than losing critical business data.

---

##  Tech Stack

* **Core Framework:** Python 3.12+, FastAPI
* **AI Orchestration:** Google Gen AI SDK (`gemini-2.5-flash`)
* **Data Validation:** Pydantic v2 (with `email-validator`)
* **Async HTTP Engine:** HTTPX
* **Server Gateway:** Uvicorn
* **Configuration:** Python-Dotenv

---

##  Project Directory Structure

```text
flexiflow-ai/
│
├── main.py              # FastAPI server routing & background workers
├── schemas.py           # Pydantic schema validation layers
├── ai_parser.py         # Google Gemini AI connection & parsing engine
├── .env                 # Environment configurations (Git-ignored)
├── requirements.txt     # Locked project dependencies
└── README.md            # System documentation

## Installation & Local Setup
1. Clone the Repository
   git clone https://github.com/Xeeshan-23/Intelligent-webhook-pipeline.git
   cd flexiflow-ai

2. Set Up a Virtual Environment & Activate It
   python -m venv venv
  # On Windows PowerShell: .\venv\Scripts\Activate.ps1 
  # On Mac/Linux: source venv/bin/activate

3. Install Required Dependencies
   pip install -r requirements.txt

4. Configure Your Environment Variables
   Create a .env file in the root directory:
   GEMINI_API_KEY=your_actual_gemini_api_key_here

5. Running the Server
   Start the local Uvicorn development server on port 8001:  uvicorn main:app --reload --port 8001
   The gateway will initialize and listen natively on http://127.0.0.1:8001.

6. Verification & End-to-End Testing
   Open a secondary terminal window and execute the following PowerShell command to simulate a messy, real-world incoming customer email alert targeting your webhook receiver:
   
   $body = @{
    source = "Email Integration"
    data_type = "unstructured"
    raw_payload = "Hey team, my name is John Doe from TechStart Solutions. I am looking for an automation dev. Our budget is around 2500 dollars. Hit me back at john.doe@techstart.com"
} | ConvertTo-Json

   Invoke-RestMethod -Uri "[http://127.0.0.1:8001/webhook](http://127.0.0.1:8001/webhook)" -Method Post -Body $body -ContentType "application/json"

   Expected JSON Output Payload:
   {
  "status": "accepted",
  "message": "Pipeline processing started.",
  "parsed_preview": {
    "name": "John Doe",
    "email": "john.doe@techstart.com",
    "company": "TechStart Solutions",
    "budget": 2500.0,
    "summary": "Prospect is explicitly looking for an automation developer."
  }}

  License & Contact
  Distributed under the MIT License. Developed with ❤ by Muhammad Zeeshan Sadiq.