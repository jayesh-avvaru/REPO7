from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------- In-memory "database" ----------
db = {}
next_id = 1

FIELDS = ("name", "description", "price")


def not_found():
    return jsonify(detail="Item not found"), 404


# ---------- CREATE ----------
@app.post("/items")
def create_item():
    global next_id
    data = request.get_json(silent=True) or {}
    if "name" not in data or "price" not in data:
        return jsonify(detail="name and price are required"), 400

    item = {
        "id": next_id,
        "name": data["name"],
        "description": data.get("description"),
        "price": data["price"],
    }
    db[next_id] = item
    next_id += 1
    return jsonify(item), 201


# ---------- READ ----------
@app.get("/items")
def list_items():
    return jsonify(list(db.values()))


@app.get("/items/<int:item_id>")
def get_item(item_id):
    item = db.get(item_id)
    return jsonify(item) if item else not_found()


# ---------- UPDATE ----------
@app.put("/items/<int:item_id>")
def update_item(item_id):
    item = db.get(item_id)
    if not item:
        return not_found()
    data = request.get_json(silent=True) or {}
    item.update({k: data[k] for k in FIELDS if k in data})
    return jsonify(item)


# ---------- DELETE ----------
@app.delete("/items/<int:item_id>")
def delete_item(item_id):
    if item_id not in db:
        return not_found()
    del db[item_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, port=8000)

# Run:  pip install flask
#       python app.py
