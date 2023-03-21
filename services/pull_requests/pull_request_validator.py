
from typing import List
from pydantic import BaseModel
from datetime import datetime
import inspect
import re
import pytz

from models import PullRequest, PullRequestValidationResult, ValidationResult
from utils import get_name_from_id, DateUtil

class Files(BaseModel):
    path: str
    filename: str
    extension: str
    def toString(self):
        return f"{self.filename}.{self.extension}"
    def toFullString(self):
        return f"{self.path}/{self.filename}.{self.extension}"
    
class PullRequestValidator(BaseModel):
    result: List[PullRequestValidationResult] = []
    
    default_result: bool = True
    default_reason: str = ''
    forbiden_pattern: str = r'[\s#%&{}\\/<>*!?${}\':"@+`|=]+'
    
    allowed_extension: set[str] = {"cpp", "c", "py", "java", 'js', 'h', 'ts', 'kt', 'kts', 'rb', 'swift'}
    
    def is_valid_title_format(self, title: str):
        pattern = r"\[Baekjoon\] \d{2}-\d{2}-\d{2}"
        return bool(re.match(pattern, title, re.IGNORECASE))
    
    def _validate_title_format(self, pull_request: PullRequest) -> ValidationResult:
        # 타이틀 형식이 다르면 invalid pull request
        result = self.default_result
        reason = self.default_reason
        if not self.is_valid_title_format(title=pull_request.title):
            reason = "잘못된 타이틀 형식입니다."
            result = False
            
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
        
    def _validate_title_date(self, pull_request: PullRequest) -> ValidationResult:
        """ Pull Request의 Title과 Created_time을 검증하는 함수. \n
        예시로 [Baekjoon] 23-03-21 의 이름을 가진 PR의 경우\n
        3월 21일 00시 ~ 3월 22일 08시 59분까지 허용
        """
        
        result = self.default_result
        reason = self.default_reason
        
        # 날짜가 다르면 invalid pull request
        title_date = datetime.strptime(pull_request.title.split()[-1], "%y-%m-%d").astimezone(pytz.timezone('Asia/Seoul'))
        due_date = DateUtil.get_pull_request_due_time(title_date)
        created_date = pull_request.created_at
        
        if created_date < title_date or created_date > due_date:
            reason = "Pull Request가 생성된 날짜와 타이틀의 날짜가 다릅니다."
            result = False
            
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
    
    def _validate_user_id(self, pull_request: PullRequest) -> ValidationResult:
        result = self.default_result
        reason = self.default_reason
        
        name = get_name_from_id(pull_request.user_id)
        if name is None:
            result = False
            reason = "알 수 없는 user_id 입니다."
            
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
        
    def _validate_labels(self, pull_request: PullRequest) -> ValidationResult:
        # label에 이름이 없으면 invalid pull request
        result = self.default_result
        reason = self.default_reason
        name = get_name_from_id(pull_request.user_id)
        
        if name not in pull_request.labels:
            result = False
            reason = "Label에 이름이 없습니다."
            
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
    
    def _has_space_or_special_letters(self, string: str):
        return bool(re.search(self.forbiden_pattern, string))
    
    def _parse_filenames(self, pull_request: PullRequest) -> List[Files]:
        filenames = []
        for f in pull_request.files:
            f_split = f.split('/')
            filename = f_split[-1]
            path = "/".join(f_split[:-1])
            extension = None
            if '.' in filename:
                filename, extension = filename.split('.')
            filenames.append(
                Files(
                    path=path,
                    filename=filename,
                    extension=extension
                )
            )
        return filenames

    def _validate_filenames(self, filenames: List[Files]):
        result = self.default_result
        reason = self.default_reason

        if invalid_files := [
            file.toString()
            for file in filenames
            if self._has_space_or_special_letters(file.toString())
        ]:
            if len(invalid_files) > 3:
                reason = f'파일명에 공백이나 특수문자가 있습니다. ({", ".join(invalid_files[:3])}...)'
            else:
                reason = f'파일명에 공백이나 특수문자가 있습니다. ({", ".join(invalid_files)})'
            result = False


        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
        
    def _validate_filename_format(self, filenames: List[Files]):
        result = self.default_result
        reason = self.default_reason
        if invalid_files := [
            file.toString()
            for file in filenames
            if len(file.filename.split('_')) != 2
        ]:
            result = False
            if len(invalid_files) > 3:
                reason = f'파일명의 형식이 올바르지 않습니다. ({", ".join(invalid_files[:])}...)'
            else:
                reason = f'파일명의 형식이 올바르지 않습니다. ({", ".join(invalid_files)})'

        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
    
    def _validate_file_extension(self, filenames: List[Files]) -> ValidationResult:
        result = self.default_result
        reason = self.default_reason
        if invalid_files := [
            file.toString()
            for file in filenames
            if file.extension not in self.allowed_extension
        ]:
            result = False
            if len(invalid_files) > 3:
                reason = f'허용되지 않은 확장자입니다. ({", ".join(invalid_files[:3])}...)'
            else:
                reason = f'허용되지 않은 확장자입니다. ({", ".join(invalid_files)})'
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
        
    def _validate_file_username(self, pull_request: PullRequest, filenames: List[Files]) -> ValidationResult:
        result = self.default_result
        reason = self.default_reason
        name = get_name_from_id(pull_request.user_id)

        if invalid_files := [
            file.toString()
            for file in filenames
            if file.filename.split('_')[-1] != name
        ]:
            result = False
            if len(invalid_files) > 3:
                reason = f'파일명에 이름이 잘못 기재되어 있습니다. ({", ".join(invalid_files[:3])}...)'
            else:
                reason = f'파일명에 이름이 잘못 기재되어 있습니다. ({", ".join(invalid_files)})'

        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
    
    def _validate_filename_week(self, pull_request: PullRequest, filenames: List[Files]) -> ValidationResult:
        result = self.default_result
        reason = self.default_reason
        
        week = DateUtil.get_weeknumber_from_startdate(pull_request.created_at)
        path = f"Baekjoon/{week}주차"
        if invalid_files := [
            file.toFullString()
            for file in filenames
            if file.path.lower() != path.lower()
        ]:
            result = False
            reason = f'현재 주차와 일치하지 않습니다. ({invalid_files[0]})'
        
        return ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        )
    
    def validate_pull_requests(self, pull_requests: List[PullRequest]):
        
        # 선행조건 
        # title_format이 성공해야 title_date 체크가능
        # user_id가 성공해야 labels, filenames 체크 가능
        # filename_format이 성공해서 file_username 체크 가능

        for pr in pull_requests:
            validation_details: List[ValidationResult] = []

            title_format_result = self._validate_title_format(pr)
            validation_details.append(title_format_result)
            if title_format_result.result:
                validation_details.append(self._validate_title_date(pr))

            user_id_result = self._validate_user_id(pr)
            validation_details.append(user_id_result)

            if user_id_result.result:
                validation_details.append(self._validate_labels(pr))

                filenames = self._parse_filenames(pr)
                validation_details.append(self._validate_filenames(filenames=filenames))
                validation_details.append(self._validate_file_extension(filenames=filenames))

                filename_format_result = self._validate_filename_format(filenames=filenames)
                validation_details.append(filename_format_result)

            if filename_format_result.result:
                validation_details.append(self._validate_filename_week(
                    pull_request=pr, filenames=filenames
                ))
            
            if user_id_result.result and filename_format_result.result:
                validation_details.append(self._validate_file_username(
                    pull_request=pr, filenames=filenames
                ))
            
            
            validation_result = all(res.result for res in validation_details)
            self.result.append(
                PullRequestValidationResult(
                    validation_result=validation_result,
                    validation_details=validation_details,
                    pull_request=pr
                )
            )
    
    def get_validation_result(self) -> List[PullRequestValidationResult]:
        return self.result
pullRequestValidator = PullRequestValidator()