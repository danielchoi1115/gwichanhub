from typing import List, Dict
from pydantic import BaseModel
from models import PullRequest
from datetime import datetime
import pytz

class PullRequestParser(BaseModel):
    parsed_pull_requests: List[PullRequest] = []
    
    def parse(
        self, 
        pull_requests: List[Dict],
        pull_request_files: Dict
    ):
        try:
            for p in pull_requests:
                number = p.get('number')
                title = p.get('title')
                user_id = p.get('user').get('login')
                
                utc_datetime = datetime.strptime(p.get('created_at'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                created_at = utc_datetime.astimezone(pytz.timezone('Asia/Seoul'))
                
                labels = [l.get("name") for l in p.get('labels')]
                files = [f['filename'] for f in pull_request_files.get(number) if f['status'] != "removed"]
                
                self.parsed_pull_requests.append(
                    PullRequest(
                        number=int(number),
                        title=title,
                        user_id=user_id,
                        created_at=created_at,
                        labels=labels,
                        files=files
                    )
                )
                
        except KeyError as ex:
            raise KeyError from ex