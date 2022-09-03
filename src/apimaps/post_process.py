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


def bodies_mangle(data: dict):
    "re-organize the bodies data and put them into categories"

    if data.get("bodies") is None:
        return

    bodies = {body["id"]: body for body in data["bodies"]["bodies"]}

    categories: dict = {}
    for body in bodies.values():
        body_type = body.pop("bodyType")

        # moons go into a planet category (dict), everything else is a list
        if categories.get(body_type) is None:
            categories[body_type] = {} if body_type == "Moon" else []

        # if this body has moons... fix the name (it's French!)
        if body["moons"]:
            for moon in body["moons"]:
                # the last part of the relation URL has the ID of the
                # planet to look up the body.
                moon_id = moon["rel"].split("/")[-1]
                moon["moon"] = bodies[moon_id]["englishName"]

        # put all moons into an additionl planet hierarchy
        if body_type == "Moon":
            around = body["aroundPlanet"]["planet"]
            planet_name = bodies[around]["englishName"]
            # use the English name, not the French one
            body["aroundPlanet"]["planet"] = planet_name
            if categories[body_type].get(planet_name) is None:
                categories[body_type][planet_name] = []
            categories[body_type][planet_name].append(body)
        else:
            categories[body_type].append(body)
    data["bodies"] = {"categories": categories, "total_count": len(bodies)}


def epic_mangle(data: dict):
    "create a proper image link, based on https://epic.gsfc.nasa.gov/about/api"

    if data.get("epic") is None:
        return

    for image in data["epic"]:
        year = image["identifier"][:4]
        month = image["identifier"][4:6]
        day = image["identifier"][6:8]

        image["url"] = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/png/{image['image']}.png"
        )


manglers = [astro_mangle, bodies_mangle, epic_mangle, natural_mangle]
