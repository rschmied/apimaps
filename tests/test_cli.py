"test for the top level entry point function which uses Click"

import os
from unittest.mock import AsyncMock, patch

from click.testing import CliRunner

from apimaps.cli import run


@patch("apimaps.apimap.APIMindMap")
def test_cli_method(mock_apimap):
    "cli function test"

    if os.environ.get("TOKEN") is None:
        os.environ["TOKEN"] = "some token"

    instance = mock_apimap.return_value
    instance.data = {}
    instance.gather_data = AsyncMock(return_value={})
    runner = CliRunner()

    # basic invocation -- no specific args, token provided via env
    result = runner.invoke(run)
    assert result.exit_code == 0

    # provide an API name that doesn't exist
    result = runner.invoke(run, ["doesntexist"])
    assert result.exit_code == 1

    # list all APIs
    result = runner.invoke(run, ["--list-apis"])
    assert result.exit_code == 0

    # epic API requires a token, we don't provide one
    if os.environ.get("TOKEN") is not None:
        del os.environ["TOKEN"]
    result = runner.invoke(run, ["epic"])
    assert result.exit_code == 1
