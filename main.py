from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import httpx
from schemas import CleanLeadData
from ai_parser import parse_unstructured_text

app = FastAPI(title="FlexiFlow-AI Pipeline")

class WebhookPayload(BaseModel):
    source: str
    data_type: str  
    raw_payload: str

async def send_to_crm_with_retry(data: CleanLeadData, retries=3, delay=2):
    """ Simulated defensive delivery pipeline with exponential back-off """
    async with httpx.AsyncClient() as client:
        # Simulating an external CRM endpoint that might flake out
        target_url = "https://httpbin.org/status/200" 
        
        for attempt in range(1, retries + 1):
            try:
                print(f"[Attempt {attempt}] Forwarding clean data to CRM...")
                response = await client.post(target_url, json=data.model_dump())
                
                if response.status_code == 200:
                    print(" Data successfully synced to CRM.")
                    return True
            except httpx.RequestError as e:
                print(f" Network error on attempt {attempt}: {e}")
            
            await asyncio.sleep(delay * attempt) # Exponential back-off
            
        print(" Critical: Webhook pipeline failed after maximum retries. Logging to dead-letter queue.")
        # In production, save to a DB/Queue here for human review

@app.post("/webhook")
async def receive_webhook(payload: WebhookPayload, background_tasks: BackgroundTasks):
    try:
        # Step 1: Process based on payload structure
        if payload.data_type == "unstructured":
            print(" Unstructured payload detected. Routing to GenAI Parser...")
            clean_data = await parse_unstructured_text(payload.raw_payload)
        else:
            # If it's already clean, parse it directly via Pydantic
            clean_data = CleanLeadData.model_validate_json(payload.raw_payload)
        
        # Step 2: Offload CRM syncing to background tasks so webhook returns a 200 instantly
        background_tasks.add_task(send_to_crm_with_retry, clean_data)
        
        return {"status": "accepted", "message": "Pipeline processing started.", "parsed_preview": clean_data}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Pipeline Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)