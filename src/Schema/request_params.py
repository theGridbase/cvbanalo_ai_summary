from pydantic import BaseModel, Field, field_validator
from typing import List

class CVRequest(BaseModel):
    job_title: str = Field(..., title="Job Title", description="The title of the job the user has or desires")
    experience: str = Field(..., title="Experience", description="The number of years of experience the user has")
    technical_skills: List[str] = Field(..., title="Technical Skills", description="List of technical skills the user has")
    soft_skills: List[str] = Field(..., title="Soft Skills", description="List of soft skills the user possesses")

    @field_validator('experience')
    def experience_must_be_numeric(cls, value):
        if not value.isdigit():
            raise ValueError('Experience must be a numeric value')
        return value
    
class StreamCVRequest(BaseModel):
    job_title: str
    experience: str
    technical_skills: List[str]
    soft_skills: List[str]
    character_limit: int = 500
    tone: str = "formal"
    
    @field_validator('experience')
    def experience_must_be_numeric(cls, value):
        if not value.isdigit():
            raise ValueError('Experience must be a numeric value')
        return value
    
    @field_validator('character_limit')
    def character_limit_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Character limit must be a positive integer')
        return value    
    
class RepromptRequest(BaseModel):
    session_id: str
    user_input: str