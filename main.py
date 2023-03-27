
import logging

from services import PullRequestFetcher, PullRequestParser, PullRequestValidator, PullRequestMerger, DiscordBot
from utils import DiscordMessageBuilder
from configs import settings
    
def main(
    skip_merge: bool = False,
    test_channel: bool = False,
    test_repository: bool = False
):
    pullRequestFetcher = PullRequestFetcher()
    pullRequestParser = PullRequestParser()
    pullRequestValidator = PullRequestValidator()
    pullRequestMerger = PullRequestMerger()
    discordMessageBuilder = DiscordMessageBuilder()
    discordBot = DiscordBot.bot(settings.discord.BOT_TOKEN)
    
    if test_repository:
        settings.github.set_test()
        
    if skip_merge:
        pullRequestMerger.set_skip_merge(True)
        discordMessageBuilder.set_skip_merge(True)
    
    if test_channel:
        discordBot.set_channel_id(settings.discord.CHANNEL_ID_TEST)
    else:
        discordBot.set_channel_id(settings.discord.CHANNEL_ID_SERVICE)
    
    logger.info("Fetching pull requests...")
    pullRequestFetcher.fetch_all()

    logger.info("Parsing pull requests...")
    pullRequestParser.parse(
        pull_requests=pullRequestFetcher.get_pull_requests(),
        pull_request_files=pullRequestFetcher.get_pull_request_files()
    )

    logger.info("Validating pull requests...")
    validation_result = pullRequestValidator.get_validation_result(pullRequestParser.parsed_pull_requests)

    logger.info("Merging pull requests...")
    pullRequestMerger.merge(validation_result)
    
    merge_result = pullRequestMerger.get_merge_result()
    
    logger.info("Building report...")
    report = discordMessageBuilder.build_report(merge_pull_request_results=list(reversed(merge_result)))
        
    logger.info("Sending report to Discord Bot...")
    discordBot.notify(report)
    
    logger.info("Report Successfully sent!")
    
if __name__ == '__main__':
    logging.basicConfig(
        filename='/usr/share/gwichanhub/main.log',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger = logging.getLogger(__name__)
    
    try:
        settings.update()
        
        main(
            # skip_merge=True,
            # test_channel=True
        )
        
    except Exception as ex:
        logger.exception(ex)
        DiscordBot.bot(settings.discord.BOT_TOKEN).set_channel_id(settings.discord.CHANNEL_ID_TEST).notify([ex])