from typing import List
from typing_extensions import Self
from pydantic import BaseModel
import inspect
from enum import Enum

from models import PullRequest, PullRequestValidationResult, ValidationResult, CommitFile
from utils import FileUtil
from configs import settings
from .pull_request_validator_helper import Validation
class Flags(Enum):
    TITLE = 1
    USER_ID = 2
    FILE_SPECIAL = 3
    FILE_FORMAT = 4
    
def check_and_set_flag(flags_to_check, flag_to_add = None):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            if args[0].has_flags(flags_to_check):
                res = fun(*args, **kwargs)  
                if res.validation_details[-1].result:
                    args[0].add_flag(flag_to_add)
                return res
            else: 
                return args[0]
        return wrapper
    return decorator

class PullRequestValidator(BaseModel):
    pull_request: PullRequest | None = None
    commit_files: List[CommitFile] | None = None
    validation_details: List[ValidationResult] = []
    validation_flags: set[Flags] = set() # 검사 통과한 항목
    
    @classmethod
    def validator(cls: Self) -> Self:
        return cls()
    
    def has_flags(self, flags: List[Flags]):
        return all((f in self.validation_flags) for f in flags)
    
    def set_pull_request(self, pull_request: PullRequest) -> Self:
        self.pull_request = pull_request
        return self
    
    def set_commit_files(self, commit_files: List[CommitFile]) -> Self:
        self.commit_files = commit_files
        return self
    
    def validate(self) -> ValidationResult:
        validation_result = all(res.result for res in self.validation_details)
        return PullRequestValidationResult(
                    validation_result=validation_result,
                    validation_details=self.validation_details,
                    pull_request=self.pull_request
                )
    
    def add_result(self, result: ValidationResult):
        self.validation_details.append(result)
    
    def add_flag(self, flag: Flags):
        self.validation_flags.add(flag)
    
    @check_and_set_flag([], Flags.USER_ID)
    def validate_user_id(self) -> Self:
        """user_id가 있는지 검사"""
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        
        if not Validation.is_valid_userid(self.pull_request):
            result = False
            reason = "알 수 없는 user_id 입니다."
            
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.USER_ID], Flags.TITLE)
    def validate_title_format(self) -> Self:
        """Pull Request의 타이틀 형식이 [Baekjoon] yy-mm-dd인지 검사. 대소문자 무시"""
        result = settings.validator.DEFAULT_RESULT
        reason = settings.validator.DEFAULT_REASON
        if not Validation.is_valid_title_format(self.pull_request):
            reason = "잘못된 타이틀 형식입니다."
            result = False
        
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.TITLE, Flags.USER_ID])
    def validate_title_date(self) -> Self:
        """ Pull Request의 Title과 Created_time을 검증하는 함수. \n
        예시로 23년 3월 22일에 검증 진행 시 [Baekjoon] 23-03-21 의 이름을 가진 PR만 허용\n
        
        선행함수 validate_title_format
        """
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        
        if not Validation.is_valid_title_date(self.pull_request):
            reason = "타이틀의 날짜가 일치하지 않습니다."
            result = False
            
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.USER_ID])
    def validate_labels(self) -> Self:
        """label에 이름이 있는지 검사"""
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        
        if not Validation.is_valid_label(self.pull_request):
            result = False
            reason = "Label에 이름이 없습니다."
            
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.USER_ID], Flags.FILE_SPECIAL)
    def validate_file_no_special(self) -> Self:
        """파일명에 공백이나 특수문자가 있는지 검사
        """
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT

        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.has_no_special_in_file(file)
        ]:
            content = FileUtil.format_content(invalid_files)
            reason = f'파일명에 공백이나 특수문자가 있습니다. ({content})'
            result = False

        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.FILE_SPECIAL])
    def validate_file_firstchar_not_digit(self) -> Self:
        """파일명이 숫자로 시작하지 않는지 검사
        """
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT

        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.is_firstchar_not_digit(file)
        ]:
            content = FileUtil.format_content(invalid_files)
            reason = f'파일명이 숫자로 시작합니다. ({content})'
            result = False

        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.FILE_SPECIAL])
    def validate_file_path(self) -> Self:
        """파일이 올바른 위치에 있는지 검사. 
        예시) baekjoon/정수론 폴더에 있는지 확인.
        """

        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        
        if invalid_files := [
            file.toFullString()
            for file in self.commit_files
            if not Validation.is_valid_file_path(file)
        ]: 
            # file.path should look like ["baekjoon", "정수론"]
            result = False
            content = FileUtil.format_content(invalid_files)
            reason = f'파일이 올바른 위치에 있지 않습니다. ({content})'

        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self

    @check_and_set_flag([Flags.FILE_SPECIAL])
    def validate_file_extension(self) -> Self:
        """파일명의 확장자가 올바른지 검사"""
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.is_valid_file_extension(file)
        ]:
            result = False
            content = FileUtil.format_content(invalid_files)
            reason = f'허용되지 않는 확장자입니다. ({content})'
        
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
        
    @check_and_set_flag([Flags.FILE_SPECIAL], Flags.FILE_FORMAT)
    def validate_file_format(self) -> Self:
        """파일명의 형식이 문제명_이름 으로 되어있는지 검사.\n
        `_` 를 기준으로 파일명을 분리해서 길이가 2인지 아닌지 검사한다.
        """
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.is_valid_file_format(file)
        ]:
            result = False
            content = FileUtil.format_content(invalid_files)
            reason = f'파일명의 형식이 올바르지 않습니다. ({content})'
        
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.FILE_FORMAT])
    def validate_file_prefix_after_num(self) -> Self:
        """`H_` 로 시작하는데 다음에 숫자가 없는 경우 검사한다.
        """
        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.is_valid_file_prefix_after_num(file)
        ]:
            result = False
            content = FileUtil.format_content(invalid_files)
            reason = f'숫자로 시작하지 않는 파일명에 H_ 키워드가 있습니다. ({content})'
        
        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    @check_and_set_flag([Flags.FILE_FORMAT])
    def validate_file_username(self) -> Self:
        """파일명의 이름이 올바른지 검사. 다른 유저의 파일을 커밋/삭제 하는 경우를 방지하기 위함함"""

        reason = settings.validator.DEFAULT_REASON
        result = settings.validator.DEFAULT_RESULT
        

        if invalid_files := [
            file.toString()
            for file in self.commit_files
            if not Validation.is_valid_file_username(file=file, pr=self.pull_request)
        ]:
            result = False
            content = FileUtil.format_content(invalid_files)
            reason = f'파일명에서 이름을 찾을 수 없습니다. ({content})'

        self.add_result(ValidationResult(
            validation=inspect.currentframe().f_code.co_name,
            result=result,
            reason=reason
        ))
        return self
    
    def validate_pull_request(self, pull_request: PullRequest) -> PullRequestValidationResult:
        files = FileUtil.parse_files(pull_request.files)
        return PullRequestValidator.validator()         \
                        .set_pull_request(pull_request) \
                        .set_commit_files(files)        \
                        .validate_user_id()             \
                        .validate_title_format()        \
                        .validate_title_date()          \
                        .validate_labels()              \
                        .validate_file_no_special() \
                        .validate_file_firstchar_not_digit() \
                        .validate_file_path()       \
                        .validate_file_extension()      \
                        .validate_file_format()     \
                        .validate_file_prefix_after_num() \
                        .validate_file_username()       \
                        .validate()


    def get_validation_result(self, pull_requests: List[PullRequest]):
        return [
            self.validate_pull_request(p) 
            for p in pull_requests
        ]

pullRequestValidator = PullRequestValidator()
