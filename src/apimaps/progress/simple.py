"A progress printing implementation"

from typing import Optional

from apimaps.progress.messages import FETCH, FAILURE, SUCCESS


class SimpleProgress:
    "a simple progress (just prints) implementation"

    def initialize(self):
        "initialize a progress object, nothing to do here"

    def start(self, desc: str):
        "start with some progress message"
        print(f"{FETCH} {desc}")

    def stop_good(self, idx: int, desc: str):
        "end the progress message (good case)"
        _ = idx
        print(f"{SUCCESS} {desc}")

    def stop_failed(self, idx: int, desc: str, exc: Optional[Exception]):
        "end the progress message (failed case)"
        _ = idx
        print(f"{FAILURE} {desc}, {exc}")

    def restore(self):
        "nothing to do here either"
