
from typing import List, Dict
from models import BaseRequest
from configs import settings

class PullRequestFetcher(BaseRequest):
    headers: dict = settings.github.SERVICE_HEADERS
    sleeptime: float = settings.request.DEFAULT_SLEEPTIME
    pull_requests: List[Dict] | None = None
    pull_request_files: Dict = {}
    
    def fetch_pull_requests(self):
        # Open되어있는 Pull request 전부 가져오기
        self.pull_requests = self.request(
            method='get', 
            url=settings.github.url_pull_requests()
        )
        
    def fetch_pull_request_files(self):
        for p in self.pull_requests:
            pull_number = p.get("number")
            self.pull_request_files[pull_number] = self.request(
                method='get', 
                url=settings.github.url_pull_request_files(pull_number)
            )
            
    def fetch_all(self):
        self.fetch_pull_requests()
        self.fetch_pull_request_files()
        
    def get_pull_requests(self) -> List[Dict]:
        return self.pull_requests
    
    def get_pull_request_files(self) -> Dict:
        return self.pull_request_files