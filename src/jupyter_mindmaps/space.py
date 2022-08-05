"module docstring"

import asyncio

import httpx
from jinja2 import Environment, PackageLoader
import jupyter_mindmaps.apilist as apl

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class JupyterMindMaps:
    "the space API gather and render class"

    def __init__(self, token):
        self.token = token
        self.data = {}

    async def get(self, client, api: apl.API):
        "get the API via async httpx call"

        print("fetching", api.description)
        uri = api.uri
        if api.use_token:
            uri = uri.format(self.token)
        try:
            response = await client.get(uri)
        except Exception as exc:
            print("oh-oh:", api.description, exc)
            return
        # response.raise_for_status()
        self.data[api.name] = response.json()
        print("done", api.description)

    async def gather_data(self):
        "call all the APIs"

        apis = []
        async with httpx.AsyncClient() as client:
            for api in apl.apilist(fast=True):
                apis.append(self.get(client, api))
            await asyncio.gather(*apis)

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

    def render_space(self, filename: str):
        "fill the template with the gathered data"

        # stitch all templates together and render it
        env = Environment(loader=PackageLoader("jupyter_mindmaps"))
        loaders = []
        for api in self.data:
            loaders.append(env.get_template(api + ".j2"))
        space = env.get_template("space.j2")
        output = space.render(apis=loaders, **self.data)

        # Save File
        with open(filename, "w", encoding="utf8") as handle:
            handle.write(output)
