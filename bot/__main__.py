import os

import discord
from discord.colour import Colour

from worker.worker import transcribe


class AutoTranscribe(discord.Client):
    async def on_message(self, message: discord.Message):
        # Check if the message is from a bot
        if message.author.bot:
            return

        # Check if the message contains attachments
        if not message.attachments:
            return

        voice_msg = [
            attachment
            for attachment in message.attachments
            if attachment.is_voice_message()
        ]
        if not voice_msg:
            return

        # If the voice message is longer than 30s, quit
        if voice_msg[0].duration > 30:
            return

        # Get the file url
        file_url = voice_msg[0].url

        # Send the file url to the worker
        result = transcribe.delay(file_url)

        # Get text, and quit if there is no text
        text = await self.loop.run_in_executor(None, result.get)
        if not text:
            return

        # Send the result
        embed = discord.Embed(
            title="Transcription", description=text, color=Colour.blurple()
        )
        await message.reply(embed=embed)


if __name__ == "__main__":
    client = AutoTranscribe(
        intents=discord.Intents(messages=True, message_content=True)
    )
    client.run(os.environ["AUTOTRANSCRIBE_DISCORD_TOKEN"])
