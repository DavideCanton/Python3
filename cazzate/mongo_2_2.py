import random

import pymongo


def main():
    conn = pymongo.MongoClient("mongodb://localhost")
    db = conn.places

    query = [0, 0]
    res = db.places.aggregate([
        {
            "$geoNear": {
                "near": {"type": "Point", "coordinates": query},
                "distanceField": "dist.calculated",
                "includeLocs": "dist.location",
                "num": 5,
                "spherical": True
            }
        }
    ])

    for l in res:
        print("{} is at distance {} from {}".format(l['properties']['name'],
                                                    l['dist']['calculated'],
                                                    query))


def ins():
    conn = pymongo.MongoClient("mongodb://localhost")
    db = conn.places

    for i in range(10000):
        long = random.randint(0, 240000) / 1000 - 120
        lat = random.randint(0, 160000) / 1000 - 80

        doc = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [long, lat]
            },
            "properties": {
                "name": "Place {}".format(i)
            }
        }

        db.places.insert_one(doc)


if __name__ == "__main__":
    main()
