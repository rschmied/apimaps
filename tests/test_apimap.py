"tests for the apimap Class"

import asyncio
from unittest.mock import AsyncMock, patch, Mock
from httpx import Response

from apimaps.apimap import APIMindMap
from apimaps.apilist import get_api_set
from apimaps.post_process import astro_mangle


@patch("apimaps.apimap.httpx")
def test_apimap_gather(mock_httpx, test_data):
    "test the APIMindMap gather_data method with mocked httpx"

    mocked_async_client = Mock()

    data = test_data("people.json")
    response = Response(status_code=200, json=data)
    mocked_async_client.get = AsyncMock(return_value=response)
    mock_httpx.AsyncClient.return_value.__aenter__.return_value = mocked_async_client

    # good path
    mock_progress = Mock()
    apimap = APIMindMap("sometoken", mock_progress)
    api_list = get_api_set({"people"})
    asyncio.run(apimap.gather_data(api_list))
    mock_progress.stop_good.assert_called_once_with(0, "People in Space")

    # data is broken, JSON can't be parsed
    mock_progress.reset_mock()
    response = Response(status_code=200, text=",,,")
    mocked_async_client.get = AsyncMock(return_value=response)
    asyncio.run(apimap.gather_data(api_list))
    mock_progress.stop_failed.assert_called_once()

    # server error
    mock_progress.reset_mock()
    response = Response(status_code=500, text="something went wrong")
    mocked_async_client.get = AsyncMock(return_value=response)
    asyncio.run(apimap.gather_data(api_list))
    mock_progress.stop_failed.assert_called_once()

    # connection error
    mock_progress.reset_mock()
    mocked_async_client.get.side_effect = ConnectionError("baem")
    asyncio.run(apimap.gather_data(api_list))
    mock_progress.stop_failed.assert_called_once()


def test_apimap_render(test_data):
    "test the APIMindMap render method"

    data = test_data("people.json")
    astro_mangle(data)

    mock_progress = Mock()
    apimap = APIMindMap("sometoken", mock_progress)
    apimap.data = data
    apimap.render_markdown("/dev/null")
