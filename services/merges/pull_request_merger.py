
from typing import List
import time
from utils import apiUrlBuilder
from models import BaseRequest, PullRequestValidationResult, MergeResult, MergePullRequestResult

class PullRequestMerger(BaseRequest):
    results: List[MergePullRequestResult] = []
    skip_merge: bool = False
    
    def set_skip_merge(self, skip_merge: bool):
        self.skip_merge = skip_merge
    
    def merge(self, validation_results: List[PullRequestValidationResult]):
        for item in validation_results:
            if self.skip_merge:
                self.results.append(
                    MergePullRequestResult(
                        merge=MergeResult.test_merge_result(item.validation_result),
                        validation=item
                    )
                )
                continue
            res = {}
            if item.validation_result:
                res = self.request(
                    method='put', 
                    url=apiUrlBuilder.build_merge_pull_request_url(pull_number=item.pull_request.number)
                )
            merge_result = MergeResult(
                **res
            )
            self.results.append(
                MergePullRequestResult(
                    merge=merge_result,
                    validation=item
                )
            )
    def get_merge_result(self) -> List[MergePullRequestResult]:
        return self.results
