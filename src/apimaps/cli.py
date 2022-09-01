"module docstring"

import asyncio
import click

from apimaps import apimap
from apimaps.progress import SimpleProgress, FancyProgress
from apimaps.post_process import manglers

import apimaps.apilist as apl


@click.command()
@click.option(
    "--token",
    help="NASA Token",
    required=True,
    envvar="TOKEN",
)
@click.option(
    "--filename",
    help="the name of the markdown file to write",
    default="space.md",
)
@click.option(
    "--all-apis",
    is_flag=True,
    help="use all APIs, otherwise only use the fast ones",
    default=False,
)
@click.option(
    "--not-fancy",
    is_flag=True,
    help="don't use fancy terminal tricks",
    default=False,
)
def run(token, filename, all_apis, not_fancy):
    "runs the code and write the markdown file"

    # 1. prepare the API list
    api_list = apl.apilist(fast=not all_apis)
    # 2. provide a progress printing instance
    if not_fancy:
        progress = SimpleProgress()
    else:
        progress = FancyProgress(len(api_list))
    # 3. create an instance of the API fetcher/renderer
    instance = apimap.APIMindMap(token, progress)
    # 4. fetch all the data
    asyncio.run(instance.gather_data(api_list))
    # 5. post-process the data
    for mangler in manglers:
        mangler(instance.data)
    # 6. render the markdown file from the data
    instance.render_markdown(filename)
