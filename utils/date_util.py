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
        t = datetime.now().astimezone(pytz.timezone('Asia/Seoul')) - timedelta(days = 1)
        weeknum = DateUtil.get_weeknumber_from_startdate(t)
        return f'({weeknum}주차) {t.strftime("%y년 %m월 %d일")} {date_map[t.weekday()]}'    
    
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
    
    @staticmethod
    def datetome_from_title(title: str):
        return datetime.strptime(title, "%y-%m-%d")
    
    @staticmethod
    def is_same_day(d1: datetime, d2: datetime):
        return d1.year == d2.year and d1.month == d2.month and d1.day == d2.day 