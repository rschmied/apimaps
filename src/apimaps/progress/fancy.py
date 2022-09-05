"A progress printing implementation"

from typing import ContextManager, Optional
from blessed import Terminal
from apimaps.progress.messages import FETCH, FAILURE, SUCCESS


class FancyProgress:
    "a fancy progress implementation"

    def __init__(self, api_len):
        self.terminal = Terminal()
        self.offset = 0
        self.cursor_y = 0
        self.api_len = api_len

    def initialize(self):
        "initialize a progress object"
        self.cursor_y, _ = self.terminal.get_location()
        start = self.terminal.height - self.cursor_y
        if start <= self.api_len:
            self.offset = self.api_len - start + 1

    def start(self, desc: str):
        "start with some progress message"
        print(f"{self.terminal.underline_cyan}{FETCH}{self.terminal.normal} {desc}")

    def location(self, idx: int) -> ContextManager:
        "returns the proper cursor location based on the index"
        return self.terminal.location(0, self.cursor_y + idx - self.offset)

    def stop_good(self, idx: int, desc: str):
        "end the progress message (good case)"
        _ = desc
        with self.location(idx):
            print(self.terminal.green + SUCCESS + self.terminal.normal)

    def stop_failed(self, idx: int, desc: str, exc: Optional[Exception]):
        "end the progress message (failed case)"
        with self.location(idx):
            exc_str = type(exc).__name__
            if len(str(exc)) > 0:
                exc_str = f"{exc}, {exc_str}"
            msg = (
                f"{self.terminal.bold_red}{FAILURE}{self.terminal.normal} "
                f"{desc}, {exc_str}{self.terminal.clear_eol}"
            )
            if self.terminal.length(msg) > self.terminal.width:
                msg = self.terminal.wrap(msg)[0]
            print(msg)

    def restore(self):
        "nothing to do here either"
