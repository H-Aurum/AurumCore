from twitchio import Client
from twitchio.ext import commands

class TwitchChatListener(commands.Bot):
    def __init__(self, token, channel, callback):
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[channel]
        )
        self.callback = callback

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return
        self.callback(message.author.name, message.content)
        
    def start(self):
        self.run()
