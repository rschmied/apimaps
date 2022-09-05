[![CI](https://github.com/rschmied/apimaps/actions/workflows/python-app.yml/badge.svg)](https://github.com/rschmied/apimaps/actions/workflows/python-app.yml) [![Coverage Status](https://coveralls.io/repos/github/rschmied/apimaps/badge.svg?branch=main)](https://coveralls.io/github/rschmied/apimaps?branch=main)

# Create Mindmaps from API Output

> **Note**: this project was originally published by John Capobianco
> at <https://github.com/automateyournetwork/jupyter>.  I took the
> idea and refactored it massively.  In fact, the code is now almost
> 100% different from the original version which made me put it into
> a new repository of myself.

## Introduction

Using various APIs, this program collects JSON data and then uses Jinja2
templates to create a single markdown file. Using the markmap VS Code extension,
this markdown file then renders as a mind map!

## NASA API Key

Please visit the [NASA API website](https://api.nasa.gov/) and register for an
API key. Once you have your key you need to either pass it to the program with
the `--token` command line parameter or you need to export it as `TOKEN` in your
environment.

The "fast" APIs (if no specific parameters are provided to the command) will
work without a valid API token.

It's also possible to use the string `DEMO_KEY` as the API key which does have
some very limited daily use restrictions but can be used right away without
registration.

## Display the created mind map

Use the Markmap extension for VSCode to render markdown files as a mind map.
Search for "markmap"... Source is
[here](https://github.com/markmap/markmap-vscode).

## APIs

The "Token" column identifies APIs which require a NASA API token.

```plain
$ apimaps --list-apis
API     Token   Description
----------------------------------------
iss             ISS Location
people          People in Space
wom     +       Weather on Mars
apod    +       Astronomy Picture of the Day
cme     +       Coronal Mass Ejection
neo     +       Asteroids Near Earth Objects
gst     +       Geomagnetic Storms
ips     +       Interplanetary Shock
flr     +       Solar Flare
sep     +       Solar Energetic Particle
mpc     +       Magnetopause Crossing
rbe     +       Radiation Belt Enhancement
hss     +       High Speed Streams
notify  +       Notifications
natural         Natural Events
epic    +       Earth Polychromatic Imaging Camera
count           Known Celestial Body Count
bodies          Bodies
wsa     +       WSA+EnlilSimulation
$
```
