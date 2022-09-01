"module docstring"

import asyncio
import click

from apimaps import apimap
from apimaps.progress import SimpleProgress, FancyProgress

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

    api_list = apl.apilist(fast=not all_apis)
    if not_fancy:
        progress = SimpleProgress()
    else:
        progress = FancyProgress(len(api_list))
    jmm = apimap.APIMindMap(token, progress)
    asyncio.run(jmm.gather_data(api_list))
    jmm.render_space(filename)
