# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def earthquake_by_id(id):
    """
    Return earthquake by its ID.
        Args:
            id (int): The ID of the earthquake to retrieve.
    """
    quake = Earthquake.query.get(id)

    if not quake:
        body = {"message": f"Earthquake {id} not found."}
        return make_response(body, 404)

    body = {
        "id": quake.id,
        "magnitude": quake.magnitude,
        "location": quake.location,
        "year": quake.year,
    }
    return make_response(body, 200)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakes_by_magnitude(magnitude):
    """
    Return earthquakes with magnitude greater than or equal to the given value.
        Args:
            magnitude (float): The minimum magnitude to filter earthquakes.
    """
    quakes = (
        Earthquake.query.filter(Earthquake.magnitude >= magnitude)
        .order_by(Earthquake.magnitude.desc())
        .all()
    )

    quakes_list = [
        {
            "id": q.id,
            "magnitude": q.magnitude,
            "location": q.location,
            "year": q.year,
        }
        for q in quakes
    ]

    body = {
        "count": len(quakes_list),
        "quakes": quakes_list,
    }

    return make_response(body, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
