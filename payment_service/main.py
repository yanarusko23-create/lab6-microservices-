import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

STUDENT_N = int(os.getenv("STUDENT_N", 15))
app = FastAPI(title=f"Payment Service N{STUDENT_N}")

METER_SERVICE_URL = "http://meter-service-15:8000"
PAYMENTS = []

class PaymentRequest(BaseModel):
    charge_id: int
    card_last4: str

@app.post("/payments")
def create_payment(req: PaymentRequest):
    try:
        r = requests.get(f"{METER_SERVICE_URL}/meters/{req.charge_id}")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Meter Service is unavailable")
    if r.status_code == 404:
        raise HTTPException(status_code=400, detail="Charge not found")
    charge = r.json()["data"]
    if charge["status"] == "Paid":
        raise HTTPException(status_code=400, detail="Already paid")
    payment = {
        "payment_id": len(PAYMENTS) + 1,
        "student_id": STUDENT_N,
        "charge_id": req.charge_id,
        "service": charge["service"],
        "amount": charge["amount"],
        "card_last4": req.card_last4,
        "status": "Success"
    }
    PAYMENTS.append(payment)
    return payment

@app.get("/payments")
def get_payments():
    return {"student_id": STUDENT_N, "payments": PAYMENTS}
