from celery import Task
from faster_whisper import WhisperModel


class WhisperBaseTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = None

    def __call__(self, *args, **kwargs):
        if self._model is None:
            self._model = WhisperModel("base", compute_type="int8")
        return self.run(*args, **kwargs)
