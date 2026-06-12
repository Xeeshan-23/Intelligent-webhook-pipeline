from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class CleanLeadData(BaseModel):
    name: str = Field(..., description="Full name of the prospect")
    email: EmailStr = Field(..., description="Validated email address")
    company: Optional[str] = Field("Unknown", description="Company name if available")
    budget: Optional[float] = Field(0.0, description="Estimated budget parsed as a float")
    summary: str = Field(..., description="A 1-sentence summary of their requirement")