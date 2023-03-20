
import logging
from services import PullRequestFetcher, PullRequestParser, PullRequestValidator, PullRequestMerger, discordBot
from utils import DiscordMessageBuilder
from config import settings

logging.basicConfig(
    filename='main.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

# TODO Rename this here and in `main`
def run(
    pullRequestFetcher: PullRequestFetcher, 
    pullRequestParser: PullRequestParser, 
    pullRequestValidator: PullRequestValidator, 
    pullRequestMerger: PullRequestMerger
):
    logger.info("Fetching pull requests...")
    pullRequestFetcher.fetch_all()

    logger.info("Parsing pull requests...")
    pullRequestParser.parse(
        pull_requests=pullRequestFetcher.get_pull_requests(),
        pull_request_files=pullRequestFetcher.get_pull_request_files()
    )

    logger.info("Validating pull requests...")
    pullRequestValidator.validate_pull_requests(pullRequestParser.parsed_pull_requests)

    logger.info("Merging pull requests...")
    pullRequestMerger.merge(pullRequestValidator.get_validation_result())

    return pullRequestMerger.get_merge_result()
    
def make_report_and_send(merge_result):
    logger.info("Building report...")
    report = discordMessageBuilder.build_report(merge_pull_request_results=list(reversed(merge_result)))
    
        # 누구누구 했는지도 보고서에 보내야하나...?
    logger.info("Sending report to Discord Bot...")
    discordBot.set_message(report)
    discordBot.run(
        token=settings.DISCORD_BOT_TOKEN,
        log_level=logging.WARN
    )
    logger.info("Report Successfully sent!")
    
def main(
    skip_merge: bool = False,
    test_channel: bool = False,
    test_repository: bool = False
):
    if test_repository:
        settings.set_test_respository()
    if test_channel:
        settings.set_test_channel()
    if skip_merge:
        pullRequestMerger.set_skip_merge(True)
        discordMessageBuilder.set_skip_merge(True)
    
    try:
        merge_result = run(
            pullRequestFetcher,
            pullRequestParser,
            pullRequestValidator,
            pullRequestMerger,
        )
        make_report_and_send(merge_result)
        
    except Exception as e:
        logger.exception("An error occurred")

if __name__ == '__main__':
    pullRequestFetcher = PullRequestFetcher()
    pullRequestParser = PullRequestParser()
    pullRequestValidator = PullRequestValidator()
    pullRequestMerger = PullRequestMerger()
    
    discordMessageBuilder = DiscordMessageBuilder()
    
    main(
        skip_merge=True,
        test_channel=True,
        test_repository=False
    )
    
