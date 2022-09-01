"A progress printing protocol"

from typing import Optional, Protocol


class Progress(Protocol):
    "the progress base class"

    def initialize(self):
        "initialize a progress object"

    def start(self, desc: str):
        "start with some progress message"

    def stop_good(self, idx: int, desc: str):
        "end the progress message -- the good case"

    def stop_failed(self, idx: int, desc: str, exc: Optional[Exception]):
        "end the progress message -- the failed case"

    def restore(self):
        "restore whatever initialize did"
