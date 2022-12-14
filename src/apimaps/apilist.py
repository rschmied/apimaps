"the list of available / enabled APIs"

from dataclasses import dataclass

# The original list of APIs was taken from John Capobianco's
# repository at <https://github.com/automateyournetwork/jupyter>.


@dataclass()
class API:
    "an API endpoint"
    name: str
    uri: str
    description: str
    use_token: bool = True


def apilist() -> list[API]:
    "returns a dictionary of the defined APIs"
    return [
        API("iss", "http://api.open-notify.org/iss-now.json", "ISS Location", False),
        API(
            "people", "http://api.open-notify.org/astros.json", "People in Space", False
        ),
        API(
            "wom",
            "https://api.nasa.gov/insight_weather/?api_key={}&feedtype=json&ver=1.0",
            "Weather on Mars",
        ),
        API(
            "apod",
            "https://api.nasa.gov/planetary/apod?api_key={}",
            "Astronomy Picture of the Day",
        ),
        API(
            "cme",
            "https://api.nasa.gov/DONKI/CME?api_key={}",
            "Coronal Mass Ejection",
        ),
        API(
            "neo",
            "https://api.nasa.gov/neo/rest/v1/feed?api_key={}",
            "Asteroids Near Earth Objects",
        ),
        API(
            "gst",
            "https://api.nasa.gov/DONKI/GST?&api_key={}",
            "Geomagnetic Storms",
        ),
        API(
            "ips",
            "https://api.nasa.gov/DONKI/IPS?api_key={}",
            "Interplanetary Shock",
        ),
        API("flr", "https://api.nasa.gov/DONKI/FLR?api_key={}", "Solar Flare"),
        API(
            "sep",
            "https://api.nasa.gov/DONKI/SEP?api_key={}",
            "Solar Energetic Particle",
        ),
        API(
            "mpc",
            "https://api.nasa.gov/DONKI/MPC?api_key={}",
            "Magnetopause Crossing",
        ),
        API(
            "rbe",
            "https://api.nasa.gov/DONKI/RBE?api_key={}",
            "Radiation Belt Enhancement",
        ),
        API("hss", "https://api.nasa.gov/DONKI/HSS?api_key={}", "High Speed Streams"),
        API(
            "notify",
            "https://api.nasa.gov/DONKI/notifications?api_key={}",
            "Notifications",
        ),
        API(
            "natural",
            "https://eonet.gsfc.nasa.gov/api/v2.1/events",
            "Natural Events",
            False,
        ),
        API(
            "epic",
            "https://api.nasa.gov/EPIC/api/natural?api_key={}",
            "Earth Polychromatic Imaging Camera",
        ),
        API(
            "count",
            "https://api.le-systeme-solaire.net/rest/knowncount/",
            "Known Celestial Body Count",
            False,
        ),
        API(
            "bodies",
            "https://api.le-systeme-solaire.net/rest/bodies",
            "Bodies",
            False,
        ),
        API(
            "wsa",
            "https://api.nasa.gov/DONKI/WSAEnlilSimulations?api_key={}",
            "WSA+EnlilSimulation",
        ),
    ]


def get_api_set(apiset: set[str]) -> list[API]:
    "return a list of APIs which match the API name set"
    complete = apilist()

    api_names = {a.name for a in complete}
    if len(apiset.difference(api_names)) > 0:
        raise ValueError("unknown API name")

    return [a for a in complete if a.name in apiset]


def printable(apis: list[API]) -> list[str]:
    "returns a printable version of the provided API list"
    out = ["API\tToken\tDescription", "-" * 40]
    for api in apis:
        token = "+" if api.use_token else ""
        out.append(f"{api.name}\t{token}\t{api.description}")
    return out
