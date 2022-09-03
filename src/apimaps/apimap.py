"module docstring"

import asyncio
import json
from typing import List, Optional

import httpx
from jinja2 import Environment, PackageLoader

import apimaps.apilist as apl
from apimaps.progress import Progress

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class APIMindMap:
    "the space API gather and render class"

    def __init__(self, token: str, progress: Progress):
        self.token = token
        self.data: dict = {}
        self.progress = progress
        self.last_headers: Optional[httpx.Headers] = None

    async def get(self, idx: int, client: httpx.AsyncClient, api: apl.API):
        "get the API via async httpx call"

        self.progress.start(api.description)
        uri = api.uri.format(self.token) if api.use_token else api.uri
        try:
            response = await client.get(uri, headers=headers)
        except Exception as exc:
            self.progress.stop_failed(idx, api.description, exc)
            return
        if response.status_code >= 300:
            reason = f"{response.status_code}: {response.reason_phrase}"
            if len(response.text) > 0:
                reason = f"{reason}, {response.text}"
            self.progress.stop_failed(
                idx,
                api.description,
                RuntimeError(reason),
            )
            return
        self.last_headers = response.headers
        try:
            self.data[api.name] = response.json()
        except json.JSONDecodeError as exc:
            self.progress.stop_failed(idx, api.description, exc)
        else:
            self.progress.stop_good(idx, api.description)

    async def gather_data(self, apis: List[apl.API]):
        "call all the APIs asynchronously (semi-parallel)"

        self.progress.initialize()
        api_list = []
        timeout = httpx.Timeout(10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            for idx, api in enumerate(apis):
                api_list.append(self.get(idx, client, api))
            await asyncio.gather(*api_list)

    def render_markdown(self, filename: str):
        "fill the template with the gathered data"

        # stitch all templates together and render it
        env = Environment(loader=PackageLoader("apimaps"))
        loaders = []
        for api in self.data:
            loaders.append(env.get_template(api + ".j2"))
        space = env.get_template("space.j2")
        output = space.render(apis=loaders, **self.data)

        # Save File
        with open(filename, "w", encoding="utf8") as handle:
            handle.write(output)
