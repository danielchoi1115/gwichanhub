from datetime import datetime, timedelta
import pytz
from configs import settings
import math
date_map = {
        0: '월요일',
        1: '화요일',
        2: '수요일',
        3: '목요일',
        4: '금요일',
        5: '토요일',
        6: '일요일',
    }
# https://www.w3schools.com/python/python_datetime.asp
class DateUtil:
    @staticmethod
    def get_pr_date_header():
        t = datetime.now()
        return t.strftime("%y-%m-%d ") + date_map[t.weekday()]
    
    @staticmethod
    def to_full_date(date: datetime):
        return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_weeknumber_from_startdate(date: datetime = None) -> int:
        if date is None:
            date = datetime.now()
        dt = date - datetime.strptime(settings.validator.START_DATE, "%Y-%m-%d").astimezone(pytz.timezone('Asia/Seoul')) 
        return math.floor(dt.days/7)+1
    
    @staticmethod
    def get_pull_request_due_time(start_time: datetime) -> datetime:
        return start_time + timedelta(seconds=settings.validator.PR_DUE_SECONDS)