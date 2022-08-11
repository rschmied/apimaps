"module docstring"

import asyncio
import click

from jupyter_mindmaps import space


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
    jmm = space.JupyterMindMaps(token, not_fancy=not_fancy)
    asyncio.run(jmm.gather_data(fast=not all_apis))
    jmm.render_space(filename)
