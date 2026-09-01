from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Tele-Rehab Assessment API")


class PatientData(BaseModel):
  patient_id: str = Field(..., example="PAT-101")
  knee_angle: float = Field(..., ge=0, le=180, example=115.0)
  pain_score: int = Field(..., ge=1, le=10, example=3)


@app.get("/")
def home():
  return {"status": "24/7 Tele-Rehab Backend Active"}


@app.post("/assess")
def assess_patient(data: PatientData):
  status = (
      "Normal Mobility"
      if data.knee_angle >= 110
      else "Restricted Range of Motion"
  )
  return {
      "patient_id": data.patient_id,
      "knee_angle": data.knee_angle,
      "mobility_status": status,
      "flag_doctor": data.pain_score > 6,
  }