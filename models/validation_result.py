from pydantic import BaseModel
class ValidationResult(BaseModel):
    validation: str
    result: bool
    reason: str