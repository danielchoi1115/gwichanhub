
from pydantic import BaseModel
from typing import List
from .pull_request import PullRequest
from .validation_result import ValidationResult

class PullRequestValidationResult(BaseModel):
    pull_request: PullRequest
    validation_result: bool
    validation_details: List[ValidationResult]