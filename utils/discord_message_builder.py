from typing import List
from pydantic import BaseModel
from models import MergePullRequestResult, PullRequest, MessageType
from .date_util import DateUtil
from configs import settings
class ResultCase(BaseModel):
    total: int
    successful: List = []
    rejected: List = []
    failed: List = []
    notFound: List = []
    
    def successfulToString(self):
        return f'({", ".join(sorted(self.successful))})' if self.successful else ''
    def rejectedToString(self):
        return f'({", ".join(sorted(self.rejected))})' if self.rejected else ''
    def failedToString(self):    
        return f'({", ".join(sorted(self.failed))})' if self.failed else ''
    def notFoundToString(self):    
        return f'({", ".join(sorted(self.notFound))})' if self.notFound else ''

class DiscordMessageBuilder:
    skip_merge: bool = False
    def set_skip_merge(self, skip_merge: bool):
        self.skip_merge = skip_merge
        
    def count_cases(self, merge_pull_request_results: List[MergePullRequestResult]) -> ResultCase:
        result_case = ResultCase(
            total=len(merge_pull_request_results)
        )
        
        found_id = set()
        for result in merge_pull_request_results:
            found_id.add(result.validation.pull_request.user_id.lower())
            
            name = settings.github.get_name_from_id(result.validation.pull_request.user_id)
            if result.merge.merged:
                result_case.successful.append(name)

            elif not result.validation.validation_result:
                result_case.rejected.append(name)
            else:
                result_case.failed.append(name)

        result_case.notFound = [
            settings.github.get_name_from_id(id) 
            for id in settings.github.id_map
            if id not in found_id
        ]

        return result_case
    
    def format_summary(self, result_case: ResultCase):
        head = DateUtil.get_pr_date_header()
        if self.skip_merge:
            head = f'TEST {head}'
        header = f"""**{head} Merge Pull Request Report** ```md\n<Summary>\n"""
        header += f"""No. Pull Requests: {result_case.total}\n"""
        header += f"""성공: {len(result_case.successful)}건 {result_case.successfulToString()}\n"""
        header += f"""반려: {len(result_case.rejected)}건 {result_case.rejectedToString()}\n"""
        header += f"""실패: {len(result_case.failed)}건 {result_case.failedToString()}```"""


        # 2023-07-11 이후 미제출 인원 출력 하지 않는 것으로 변경
        # 주말이 아니면 미제출 인원도 출력
        # if DateUtil.get_report_date().weekday() < 5:
        #     header = header.rstrip("```")
        #     header += f"""\n미제출: {len(result_case.notFound)}건 {result_case.notFoundToString()}```"""

        return header
    
    def format_pr_header(self, pull_request: PullRequest, text):
        return f"""<PR #{pull_request.number} "{pull_request.title}" by {settings.github.get_name_from_id(pull_request.user_id)}>\n{text}"""
    
    def build_message_from_result(self, msg_type: MessageType, result: MergePullRequestResult) -> str:
        text = ''
        if msg_type == MessageType.REJECTED:
            details = [validation.reason for validation in result.validation.validation_details if not validation.result]
            text = "\n".join(details)
        elif msg_type == MessageType.FAILED:
            text=result.merge.message
            
        return self.format_pr_header(
            pull_request=result.validation.pull_request,
            text=text
        )
        
    def get_rejected_messages(self, merge_pull_request_results: List[MergePullRequestResult]):
        return [
            self.build_message_from_result(msg_type=MessageType.REJECTED, result=result) 
            for result in merge_pull_request_results
            if not result.validation.validation_result
        ]

    def get_failed_messages(self, merge_pull_request_results: List[MergePullRequestResult]) :
        return [
            self.build_message_from_result(msg_type=MessageType.FAILED, result=result)
            for result in merge_pull_request_results
            if result.validation.validation_result and not result.merge.merged
        ]
    
    def message_list_to_string(self, msg_type: int, messages: List[str]) -> str:
        msg_text = "\n\n".join(messages)
        if msg_type == MessageType.REJECTED:
            return f"""\n**반려된 Pull Requests**\n```md\n{msg_text}```"""
        elif msg_type == MessageType.FAILED:
            return f"""\n**실패한 Pull Requests**\n```md\n{msg_text}```"""
    
    def build_report(self, merge_pull_request_results: List[MergePullRequestResult]) -> List[str]:
        result_case = self.count_cases(merge_pull_request_results)
        
        # Summary
        summary = self.format_summary(result_case)
        
        # Rejected Message
        rejected_message_list = self.get_rejected_messages(merge_pull_request_results)
        rejected_message = self.message_list_to_string(
            msg_type=MessageType.REJECTED, 
            messages=rejected_message_list
        )
        
        # Failed Message
        failed_messages_list = self.get_failed_messages(merge_pull_request_results)
        failed_message =  self.message_list_to_string(
            msg_type=MessageType.FAILED, 
            messages=failed_messages_list
        )
        
        reports = [summary] 
        if result_case.rejected:
            reports.append(rejected_message)
        if result_case.failed:
            reports.append(failed_message)
            
        return reports
