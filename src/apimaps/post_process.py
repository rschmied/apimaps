"functions to post process data"


def astro_mangle(data: dict):
    "re-shuffle the ISS people data so that we can render it more efficiently"
    if data.get("people") is None:
        return
    people = data["people"]

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

    data["people"] = new_data


def natural_mangle(data: dict):
    "re-organize the data and put events in a categories hierachy"

    if data.get("natural") is None:
        return

    new_data: dict = {}
    for event in data["natural"]["events"]:
        categories = event.pop("categories")

        for category in categories:
            title = category["title"]
            if new_data.get(title) is None:
                new_data[title] = []
            new_data[title].append(event)
    data["natural"] = new_data


manglers = [astro_mangle, natural_mangle]
