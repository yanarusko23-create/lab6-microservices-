import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

STUDENT_N = int(os.getenv("STUDENT_N", 15))
app = FastAPI(title=f"Meter Service N{STUDENT_N}")

# ID починаються з 100 * N = 1500
CHARGES = {
    1501: {"id": 1501, "service": "Електроенергія", "amount": 385.50, "period": "2026-05", "status": "Unpaid"},
    1502: {"id": 1502, "service": "Водопостачання",  "amount": 142.00, "period": "2026-05", "status": "Unpaid"},
    1503: {"id": 1503, "service": "Газопостачання",  "amount": 620.75, "period": "2026-05", "status": "Unpaid"},
}

class ReadingRequest(BaseModel):
    meter_id: int
    value: float

@app.get("/meters")
def get_charges():
    return {"student_id": STUDENT_N, "charges": list(CHARGES.values())}

@app.get("/meters/{charge_id}")
def get_charge(charge_id: int):
    if charge_id not in CHARGES:
        raise HTTPException(status_code=404, detail="Charge not found")
    return {"student_id": STUDENT_N, "data": CHARGES[charge_id]}

@app.post("/readings")
def submit_reading(req: ReadingRequest):
    return {"student_id": STUDENT_N, "message": "Reading accepted", "meter_id": req.meter_id, "value": req.value}
