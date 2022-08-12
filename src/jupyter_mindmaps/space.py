"module docstring"

import asyncio
import json
from typing import Optional

import httpx
from blessed import Terminal
from jinja2 import Environment, PackageLoader

import jupyter_mindmaps.apilist as apl

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

FAILURE = "  fail  "
SUCCESS = "  done  "
FETCH = "fetching"


class JupyterMindMaps:
    "the space API gather and render class"

    def __init__(self, token: str, not_fancy: bool):
        self.token = token
        self.data: dict = {}
        self.fancy = not not_fancy
        self.terminal: Optional[Terminal] = None
        self.offset = 0
        self.cursor_y = 0

    async def get(self, idx: int, client, api: apl.API):
        "get the API via async httpx call"

        self.progress_start(FETCH, api.description)
        uri = api.uri
        if api.use_token:
            uri = uri.format(self.token)
        try:
            response = await client.get(uri, headers=headers)
        except Exception as exc:
            self.progress_stop(idx, FAILURE, api.description, exc)
            return
        if response.status_code > 300:
            reason = f"{response.status_code}: {response.reason_phrase}"
            if len(response.text) > 0:
                reason = f"{reason}, {response.text}"
            self.progress_stop(
                idx,
                FAILURE,
                api.description,
                RuntimeError(reason),
            )
            return
        try:
            self.data[api.name] = response.json()
        except json.JSONDecodeError as exc:
            self.progress_stop(idx, FAILURE, api.description, exc)
        else:
            self.progress_stop(idx, SUCCESS, api.description, None)

    def prep_terminal(self, api_len):
        "prepares the terminal"
        self.terminal = Terminal()
        self.cursor_y, _ = self.terminal.get_location()
        start = self.terminal.height - self.cursor_y
        if start <= api_len:
            self.offset = api_len - start + 1

    def progress_start(self, status: str, desc: str):
        "print a message when we start the API call"
        term = self.terminal
        if term is not None:
            print(f"{term.underline_cyan}{status}{term.normal} {desc}")
            return
        print(f"{status} {desc}")

    def progress_stop(self, idx: int, status: str, desc: str, exc: Optional[Exception]):
        "print a message when the API call is done"
        term = self.terminal
        if term is not None:
            with term.location(0, self.cursor_y + idx - self.offset):
                if exc is None:
                    print(term.green + status)
                else:
                    exc_str = type(exc).__name__
                    if len(str(exc)) > 0:
                        exc_str = f"{exc}, {exc_str}"
                    print(
                        f"{term.bold_red}{status}{term.normal} {exc_str}{term.clear_eol}"
                    )
            return

        if exc is None:
            print(f"{status} {desc}")
        else:
            print(f"{status} {desc}, {exc}")

    async def gather_data(self, fast=True):
        "call all the APIs"

        api_list = apl.apilist(fast=fast)

        if self.fancy:
            self.prep_terminal(len(api_list))

        apis = []
        async with httpx.AsyncClient() as client:
            for idx, api in enumerate(api_list):
                apis.append(self.get(idx, client, api))
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
