"module docstring"

import asyncio
import json
from typing import List

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

    async def get(self, idx: int, client: httpx.AsyncClient, api: apl.API):
        "get the API via async httpx call"

        self.progress.start(api.description)
        uri = api.uri
        if api.use_token:
            uri = uri.format(self.token)
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
        async with httpx.AsyncClient() as client:
            for idx, api in enumerate(apis):
                api_list.append(self.get(idx, client, api))
            await asyncio.gather(*api_list)

        # post processing
        self.astro_mangle()
        self.natural_mangle()

    def natural_mangle(self):
        "re-organize the data and put events in a categories hierachy"

        if self.data.get("natural") is None:
            return

        new_data = {}
        for event in self.data["natural"]["events"]:
            categories = event.pop("categories")

            for category in categories:
                title = category["title"]
                if new_data.get(title) is None:
                    new_data[title] = []
                new_data[title].append(event)
        self.data["natural"] = new_data

    def astro_mangle(self):
        "re-shuffle the ISS people data so that we can render it more efficiently"
        if self.data.get("people") is None:
            return
        people = self.data["people"]

        craft_long_names = {
            "ISS": "International Space Station",
            "Tiangong": "",
        }

        # shuffle the data around
        new_data = {"vehicle": {}, "total_number": people["number"]}
        vehicles = new_data["vehicle"]
        for person in people["people"]:
            person_craft = person["craft"]
            vehicle = vehicles.get(person_craft)
            if vehicle is None:
                vehicles[person_craft] = {
                    "long": craft_long_names.get(person_craft, "Unknown spacecraft"),
                    "people": [],
                }
            vehicles[person_craft]["people"].append(person["name"])

        # sort by people's last name [1]
        for _, craft in vehicles.items():
            craft["people"].sort(key=lambda p: p.split()[1])

        self.data["people"] = new_data

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
