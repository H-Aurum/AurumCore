from twitchio import Client
from twitchio.ext import commands
import logging

class TwitchChatListener(commands.Bot):
    def __init__(self, token, channel, callback):
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[channel]
        )
        self.channel = channel
        self.callback = callback
        self.logger = logging.getLogger('twitch_integration')

    async def event_ready(self):
        self.logger.info(f'Logged in to Twitch as | {self.nick}')
        self.logger.info(f'Monitoring channel | {self.channel}')

    async def event_message(self, message):
        if message.echo or not message.content:
            return
            
        try:
            self.callback({
                'user': message.author.name,
                'message': message.content,
                'timestamp': message.timestamp
            })
        except Exception as e:
            self.logger.error(f'Error processing message: {str(e)}')
        
    def start_listener(self):
        try:
            self.run()
            return True
        except Exception as e:
            self.logger.error(f'Failed to start Twitch listener: {str(e)}')
            return False
