
import requests
import json
import logging
from pydantic import BaseModel
import time
from typing import Dict
log = logging.getLogger(__name__)

class BaseRequest(BaseModel):
    sleeptime: float
    headers: Dict[str, str]
    def request(self, method: str, url: str) -> Dict:
        time.sleep(self.sleeptime)
        try:
            res = None
            if method.lower() == "get":
                res = requests.get(url, headers=self.headers)
            elif method.lower() == "put":
                res = requests.put(url, headers=self.headers)
            return {} if res is None else json.loads(res.content)
        
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException
        ) as ex:
            log.warning(ex)
            return {}

