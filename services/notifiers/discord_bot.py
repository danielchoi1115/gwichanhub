
import discord
from typing import List
from typing_extensions import Self
import time
import logging

logger = logging.getLogger(__name__)

from configs import settings

class DiscordBot(discord.Client):
    channel_id: int = None
    token: str = None
    messages: List[str] | str = None
    
    @classmethod
    def bot(cls: Self, token: str) -> Self:
        return cls(intents=discord.Intents.default()).set_token(token)
    
    def set_channel_id(self, _id: int) -> Self:
        self.channel_id = _id
        return self
    
    def set_message(self, messages: List[str] | str) -> Self:
        self.messages = messages
        return self
    
    def set_token(self, token: str) -> Self:
        self.token = token
        return self
    
    def notify(self, messages: List[str]):
        self.set_message(messages).run(
            token=self.token,
            log_level=logging.WARN
        )
    
    async def on_ready(self):
        if type(self.channel_id) != int:
            raise AttributeError("channel_id should be set as integer value. Use set_channel_id method")
        try:
            # guild = self.get_guild(settings.discord.GUILD_ID)
            channel = self.get_channel(self.channel_id)
            print(
                f'{self.user} is connected to the following guild:\n'
                # f'{guild.name}(id: {guild.id})\n'
                f'{channel.name}(id: {channel.id})'
            )
            if type(self.messages) == str:
                await channel.send(msg)
            else:
                for msg in self.messages:
                    if type(msg) != str:
                        msg = str(msg)
                    await channel.send(msg)
                    time.sleep(1)
        except Exception as ex:
            logger.warn(ex)
        finally:
            await self.close()
        
    


