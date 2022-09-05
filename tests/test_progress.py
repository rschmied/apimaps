"tests for the progress classes"

from unittest.mock import patch

import pytest
import apimaps.progress as prog


@pytest.mark.parametrize(
    "name",
    [
        prog.SimpleProgress,
        prog.FancyProgress,
    ],
)
def test_progress(name):
    "test the two progress implementations"

    if name.__name__ == "FancyProgress":
        with patch("apimaps.progress.fancy.Terminal") as mock_terminal:
            terminal = mock_terminal.return_value
            terminal.height = 25
            terminal.width = 80
            terminal.length.return_value = 120
            terminal.wrap.return_value = ["bla"]
            terminal.get_location.return_value = (25, 0)
            progress = name(10)
    else:
        progress = name()

    progress.initialize()
    progress.start("test")
    progress.stop_good(0, "OK")
    progress.stop_failed(0, "FAILED", None)
    progress.stop_failed(0, "FAILED", RuntimeError("bla"))
    progress.restore()
