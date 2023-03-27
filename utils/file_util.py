import re
from typing import List

from models import CommitFile

from configs import settings
class FileUtil:
    @staticmethod
    def is_valid_title_format(title: str):
        return bool(re.match(settings.validator.TITLE_PATTERN, title, re.IGNORECASE))
    
    @staticmethod
    def has_space_or_special_letters(string: str):
        return bool(re.search(settings.validator.FORBIDEN_PATTERN, string))
    
    @staticmethod
    def parse_files(files: List[str]) -> List[CommitFile]:
        filenames = []
        for f in files:
            f_split = f.split('/')
            filename = f_split[-1]
            path = f_split[:-1]
            extension = None
            if '.' in filename and filename[0] != ".":
                filename, extension = filename.split('.')
            filenames.append(
                CommitFile(
                    path=path,
                    filename=filename,
                    extension=extension
                )
            )
        return filenames
    