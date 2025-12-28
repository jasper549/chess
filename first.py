import chess
from flask import Flask, request, jsonify
from flask_cors import CORS

print("BACKEND FILE LOADED")

# Import chess business logic
from chess import ChessSessionManager

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Create chess session manager
chess_manager = ChessSessionManager()

@app.route("/start-session", methods=["POST"])
def start_session():
    data = request.get_json(force=True)
    session_id = data.get("sessionId")
    color_str = data.get("engineColor", "white").lower()

    if not session_id:
        return {"error": "Missing required fields"}, 400

    engine_color = chess.WHITE if color_str in ("white", "w") else chess.BLACK
    result = chess_manager.start_session(session_id, engine_color)

    return jsonify(result)


@app.route("/engine-move", methods=["POST"])
def engine_move():
    data = request.json
    session_id = data["sessionId"]
    human_move = data.get("humanMove")
    color_str = data.get("engineColor", "white").lower()
    engine_color = chess.WHITE if color_str in ("white", "w") else chess.BLACK

    result = chess_manager.make_move(session_id, human_move, engine_color)
    return jsonify(result)


@app.route("/resign", methods=["POST"])
def resign():
    session_id = request.json["sessionId"]
    result = chess_manager.resign(session_id)
    return jsonify(result)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "active_sessions": len(chess_manager.active_boards)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
