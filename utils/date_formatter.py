from datetime import datetime


date_map = {
        0: '월요일',
        1: '화요일',
        2: '수요일',
        3: '목요일',
        4: '금요일',
        5: '토요일',
        6: '일요일',
    }

class DateFormatter:
    @staticmethod
    def yymmdd_date():
        t = datetime.now()
        return t.strftime("%y-%m-%d ") + date_map[t.weekday()]