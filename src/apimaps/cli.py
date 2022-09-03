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
    "--simple",
    is_flag=True,
    help="use simple progress output",
    default=False,
)
@click.option(
    "--list-apis",
    help="list known APIs",
    is_flag=True,
    default=False,
)
@click.argument(
    "api",
    required=False,
)
def run(token, filename, all_apis, simple, list_apis, api):
    """
    Fetch the built-in APIs and render it to markdown.  It is then written into
    the file "space.md" (can be changed via the --filename argument).  By
    default, it just runs two APIs which don't require a NASA token.

    If you have a NASA API token, then this can be passed either via the --token
    command line option or via the TOKEN environment variable.  The optional API
    argument runs only the specified API, see --list-apis for a list of valid
    APIs.

    A valid token is DEMO_KEY, it has some usage restrictions (30 uses per day).
    """

    # list all APIs, if requested
    if list_apis:
        print("\n".join(apl.print_apis(apl.apilist())))
        return

    # 1. prepare the API list
    if api is not None:
        complete = apl.apilist()
        api_list = [a for a in complete if a.name == api]
        if len(api_list) != 1:
            print(f"Unknown API '{api}', known APIs are:")
            print("\n".join(apl.print_apis(complete)))
            return
    else:
        api_list = apl.apilist(all_apis)

    # 2. check if we need a token to continue
    if token is None and any(api for api in api_list if api.use_token):
        print("API token is missing but required!  Use --help for help.")
        return

    # 3. provide a progress printing instance
    progress = SimpleProgress() if simple else FancyProgress(len(api_list))
    # 4. create an instance of the API fetcher/renderer
    instance = apimap.APIMindMap(token, progress)
    # 5. fetch all the data
    asyncio.run(instance.gather_data(api_list))
    # 6. post-process the data
    for mangler in manglers:
        mangler(instance.data)
    # 7. render the markdown file from the data
    instance.render_markdown(filename)

    # 8. print rate limit information
    if instance.last_headers:
        limit = instance.last_headers.get("x-ratelimit-limit", 0)
        remaining = instance.last_headers.get("x-ratelimit-remaining", 0)
        print(f"Rate limit: {remaining}/{limit}")
