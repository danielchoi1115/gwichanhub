import re 
from datetime import datetime, timedelta

from utils import DateUtil
from configs import settings
from models import PullRequest, CommitFile
class Validation:
    @staticmethod
    def is_valid_userid(pr: PullRequest):
        return settings.github.get_name_from_id(pr.user_id) is not None
    
    @staticmethod
    def is_valid_title_format(pr: PullRequest):
        return bool(re.match(settings.validator.TITLE_PATTERN, pr.title, re.IGNORECASE))
    
    @staticmethod
    def is_valid_title_date(pr: PullRequest):
        title_date = DateUtil.datetome_from_title(pr.title.split()[-1])
        return DateUtil.is_same_day(title_date, datetime.now()-timedelta(days=1))
    
    @staticmethod
    def is_valid_label(pr: PullRequest):
        name = settings.github.get_name_from_id(pr.user_id)
        return name in pr.labels
    
    @staticmethod
    def has_no_special_in_file(file: CommitFile):
        return not bool(re.search(settings.validator.FORBIDEN_PATTERN, file.toString()))
    
    @staticmethod
    def is_firstchar_not_digit(file: CommitFile):
        return (file.prefix != "" or not file.filename[0].isdigit())
    
    @staticmethod
    def is_valid_file_path(file: CommitFile):
        return len(file.path) == 2 and file.path[1].lower() in settings.validator.ALLOWED_FOLDERNAMES
    
    @staticmethod
    def is_valid_file_extension(file: CommitFile):
        return file.extension.lower() in settings.validator.ALLOWED_EXTENSIONS
    
    @staticmethod
    def is_valid_file_format(file: CommitFile):
        delimeter = settings.validator.FILENAME_DELIMITER
        return len(file.filename.split(delimeter)) == 2
    
    @staticmethod
    def is_valid_file_prefix_after_num(file: CommitFile):
        return bool(file.prefix == "" or file.filename[0].isdigit())
    
    @staticmethod
    def is_valid_file_username(file: CommitFile, pr: PullRequest):
        return file.filename.split('_')[-1] == settings.github.get_name_from_id(pr.user_id)