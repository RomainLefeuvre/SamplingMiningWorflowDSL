from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/endpoint", methods=["POST"])
def handle_post():
    data = request.get_json()
    print("data : ", data)
    return jsonify({"received": data}), 200


if __name__ == "__main__":
    app.run(port=8000)
