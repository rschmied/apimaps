# Create Mindmaps from API Output

> **Note**: this project was originally published by John Capobianco
> at <https://github.com/automateyournetwork/jupyter>.  I took the
> idea and refactored it massively.  In fact, the code is now almost
> 100% different from the original version which made me put it init
> a new repository of myself.

## Introduction

Using various APIs, this program collects JSON data and then uses Jinja2
templates to create a single markdown file. Using the markmap VS Code extension
this markdown file then renders as a mind map!

## NASA API Key

Please visit [NASA](api.nasa.gov) and register for an API key. Once you have
your key you need to either pass it to the program with the `--token` command
line parameter or you need to export it as `TOKEN` in your environment.

It's also possible to use the string `DEMO_KEY` as the API key which does have
some very limited daily use restrictions but can be used right away without
registration.
