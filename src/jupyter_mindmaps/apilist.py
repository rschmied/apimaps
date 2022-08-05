"the list of available / enabled APIs"

from dataclasses import dataclass


@dataclass()
class API:
    "an API endpoint"
    name: str
    uri: str
    description: str
    use_token: bool = True


# NOTE: APIs which are commented out might need work in the template
def apilist(fast: bool = True) -> list[API]:
    "returns the list of defined APIs"
    apl = [
        API("iss", "http://api.open-notify.org/iss-now.json", "ISS Location", False),
        API(
            "people", "http://api.open-notify.org/astros.json", "People in Space", False
        ),
    ]
    if fast:
        return apl

    apl.extend(
        [
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
            # API(
            #     "gst",
            #     "https://api.nasa.gov/DONKI/GST?startDate=2021-01-01&api_key={}",
            #     "Geomagetic Storms",
            # ),
            # API("ips", "https://api.nasa.gov/DONKI/IPS?api_key={}", "Interplanetary Shock"),
            # API("flr", "https://api.nasa.gov/DONKI/FLR?api_key={}", "Solar Flare"),
            # API(
            #     "sep",
            #     "https://api.nasa.gov/DONKI/SEP?startDate=2021-01-01&api_key={}",
            #     "Solar Energetic Particle",
            # ),
            # API(
            #     "mpc", "https://api.nasa.gov/DONKI/MPC?api_key={}", "Magnetopause Crossing"
            # ),
            # API(
            #     "rbe",
            #     "https://api.nasa.gov/DONKI/RBE?api_key={}",
            #     "Radiation Belt Enhancement",
            # ),
            # API("hss", "https://api.nasa.gov/DONKI/HSS?api_key={}", "High Speed Streams"),
            # API(
            #     "wsa",
            #     "https://api.nasa.gov/DONKI/WSAEnlilSimulations?api_key={}",
            #     "WSA+EnlilSimulation",
            # ),
            API(
                "notification",
                "https://api.nasa.gov/DONKI/notifications?api_key={}",
                "Notifications",
            ),
            API(
                "natural",
                "https://eonet.gsfc.nasa.gov/api/v2.1/events",
                "Natural Events",
                False,
            ),
            # API(
            #     "epicNat",
            #     "https://api.nasa.gov/EPIC/api/natural?api_key={}",
            #     "Earth Polychromatic Imaging Camera",
            # ),
            API(
                "knowncount",
                "https://api.le-systeme-solaire.net/rest/knowncount/",
                "Known Celestial Body Count",
                False,
            ),
            API(
                "planets",
                "https://api.le-systeme-solaire.net/rest/bodies?filter=isPlanet,eq,true",
                "Planets",
                False,
            ),
            # API(
            #     "wsa",
            #     "https://api.nasa.gov/DONKI/WSAEnlilSimulations?api_key={}",
            #     "WSA+EnlilSimulation",
            # ),
        ]
    )
    return apl
