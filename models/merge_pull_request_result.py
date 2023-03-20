
from pydantic import BaseModel
from .merge_result import MergeResult
from .pull_request_validation_result import PullRequestValidationResult

class MergePullRequestResult(BaseModel):
    merge: MergeResult
    validation: PullRequestValidationResult