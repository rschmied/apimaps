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
def run(token, filename):
    "runs the code and write the markdown file"
    jmm = space.JupyterMindMaps(token)
    asyncio.run(jmm.gather_data())
    jmm.render_space(filename)
