from flask import Flask, jsonify, request

app = Flask(__name__)

# -------------------------
# Simulated "database"
# -------------------------
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# -------------------------
# Helper function
# -------------------------
def find_event(event_id):
    return next((event for event in events if event.id == event_id), None)


# -------------------------
# GET /
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


# -------------------------
# GET /events
# -------------------------
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# -------------------------
# POST /events
# -------------------------
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_id = max([event.id for event in events]) + 1 if events else 1
    new_event = Event(new_id, data["title"])

    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# -------------------------
# PATCH /events/<id>
# -------------------------
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# -------------------------
# DELETE /events/<id>
# -------------------------
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    # IMPORTANT: pytest expects 204
    return "", 204


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5555)

