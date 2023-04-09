from typing import List

from models import CommitFile
from configs import settings
class FileUtil:
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
    
    @staticmethod
    def format_content(files: List[CommitFile]):
        maxlen = settings.validator.MAX_ERROR_CONTENT_LENGTH
        return (
            ", ".join(files[:maxlen]) + "..."
            if len(files) > maxlen
            else ", ".join(files)
        )