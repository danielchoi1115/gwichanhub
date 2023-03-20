
import discord
from typing import List
import time
import logging

logger = logging.getLogger(__name__)

from config import settings

class DiscordBot(discord.Client):
    async def on_ready(self):
        try:
            print(f'{self.user} has connected to Discord!')
            guild = self.get_guild(settings.DISCORD_GUILD_ID)
            channel = self.get_channel(settings.DISCORD_CHANNEL_ID)
            print(
                f'{self.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})\n'
                f'{channel.name}(id: {channel.id})'
            )
            for msg in self.messages:
                await channel.send(msg)
                time.sleep(1)
        except Exception as ex:
            logger.warn(ex)
        finally:
            await self.close()
        
    def set_message(self, messages: List[str]):
        self.messages = messages
    
    
    
discordBot = DiscordBot(intents=discord.Intents.default())

