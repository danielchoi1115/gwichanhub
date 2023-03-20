
from pydantic import BaseModel

class MergeResult(BaseModel):
    sha: str = ""
    merged: bool = False
    message: str = ""
    
    @staticmethod
    def test_merge_result(merged: bool = True):
        return MergeResult(
            sha = "",
            merged = merged,
            message = "This is a Test Merge"
        )