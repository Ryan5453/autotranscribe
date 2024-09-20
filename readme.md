# AutoTranscribe

This is a very simple discord bot that automatically transcribes all voice messages it sees. It does not have any settings or commands.

The bot works by running two process, the main bot process that uses discord.py to connect to the Discord API, and a worker process that uses Celery to handle the transcription. 

AutoTranscribe uses OpenAI's Whisper STT model to transcribe text.