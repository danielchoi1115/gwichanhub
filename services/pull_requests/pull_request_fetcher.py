
from typing import List, Dict
import time

from models import BaseRequest
from utils import apiUrlBuilder

class PullRequestFetcher(BaseRequest):    
    pull_requests: List[Dict] | None = None
    pull_request_files: Dict = {}
    
    def fetch_pull_requests(self):
        # Open되어있는 Pull request 전부 가져오기
        self.pull_requests = self.request(
            method='get', 
            url=apiUrlBuilder.build_pull_requests_url()
        )
        
    def fetch_pull_request_files(self):
        for p in self.pull_requests:
            pull_number = p.get("number")
            self.pull_request_files[pull_number] = self.request(
                method='get', 
                url=apiUrlBuilder.build_pull_request_files_url(pull_number)
            )
            time.sleep(0.5)
            
    def fetch_all(self):
        self.fetch_pull_requests()
        self.fetch_pull_request_files()
        
    def get_pull_requests(self) -> List[Dict]:
        return self.pull_requests
    
    def get_pull_request_files(self) -> Dict:
        return self.pull_request_files