from config import settings

class ApiUrlBuilder():
    def build_pull_requests_url(self):
        return f'https://api.github.com/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPOSITORY}/pulls'
    
    def build_pull_request_files_url(self, pull_number):
        return f'https://api.github.com/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPOSITORY}/pulls/{pull_number}/files'
    
    def build_merge_pull_request_url(self, pull_number):
        return f'https://api.github.com/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPOSITORY}/pulls/{pull_number}/merge'

apiUrlBuilder = ApiUrlBuilder()