import os
from io import BytesIO

import httpx
from celery import Celery

from worker.task import WhisperBaseTask

app = Celery("worker")
app.conf.task_acks_late = True
app.conf.task_default_expires = 60
app.conf.broker_url = os.environ["AUTOTRANSCRIBE_CELERY_BROKER_URL"]
app.conf.result_backend = os.environ["AUTOTRANSCRIBE_CELERY_RESULT_BACKEND_URL"]


@app.task(base=WhisperBaseTask)
def transcribe(audio_url: str) -> str:
    r = httpx.get(audio_url, timeout=10)
    if r.status_code != 200:
        raise Exception(
            f"Failed to download audio from {audio_url}. Status code: {r.status_code}"
        )

    segments, _ = transcribe._model.transcribe(BytesIO(r.content), vad_filter=True)
    return "".join([segment.text for segment in segments]).strip()
