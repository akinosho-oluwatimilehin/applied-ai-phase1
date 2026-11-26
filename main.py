from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemini_waste_parser import parse_waste_request

app = FastAPI()

class Complaint(BaseModel):
    customer_message: str

@app.post("/complaints")
async def submit_complaint(complaint: Complaint):
    result = await parse_waste_request(complaint.customer_message)

    if result is not None:
        return result.model_dump()

    else:
        raise HTTPException(
            status_code = 503,
            detail = "Gemini is curremtly unavailable. Please try again later."
        )