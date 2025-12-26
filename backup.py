import chess
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

ITALIAN = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": ["e2e4"],

    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1": ["e7e5"],

    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 1 2": ["g1f3"],

    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2": ["b8c6"],

    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": ["f1c4"],

    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3": ["g8f6"]
}

SICILIAN = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": ["e2e4"],

    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1": ["c7c5"],

    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2": ["g1f3"],

    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2": ["d7d6", "b8c6"],

    "rnbqkbnr/pp1ppppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": ["d2d4"],

    "r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": ["d2d4"]
}

app = Flask(__name__)
CORS(app)

active_boards = {}
position_history = {} 
resigned_sessions = set()
engine_colors = {} 

def fen_key(board):
    return " ".join(board.fen().split(" ")[:4])

def get_board(session_id, fen=None):
    if session_id in resigned_sessions:
        return None
    if session_id not in active_boards:
        active_boards[session_id] = chess.Board(fen or chess.STARTING_FEN)
        position_history[session_id] = [fen_key(active_boards[session_id])]
    return active_boards[session_id]

def end_session(session_id):
    active_boards.pop(session_id, None)
    position_history.pop(session_id, None)
    resigned_sessions.discard(session_id)
    engine_colors.pop(session_id, None)
    if len(eval_cache) > 20000:
        eval_cache.clear()

INF = float('inf')
MAX_DEPTH = 3
QUIESCENCE_MAX_DEPTH = 3

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

eval_cache = {}

def material_score(board, color):
    score = 0
    for piece, value in PIECE_VALUES.items():
        score += value * (len(board.pieces(piece, color)) - len(board.pieces(piece, not color)))
    return score

def evaluate(board, engine_color):
    fen = board.fen()
    if fen in eval_cache:
        return eval_cache[fen]
    if board.is_checkmate():
        return -100000 if board.turn == engine_color else 100000
    material = material_score(board, engine_color)
    king_sq = board.king(engine_color)
    attackers = len(board.attackers(not engine_color, king_sq)) if king_sq else 0
    king_safety = -30 * attackers
    score = material + king_safety
    eval_cache[fen] = score
    return score

def ordered_moves(board):
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)
    return moves

TT = {}
EXACT, LOWERBOUND, UPPERBOUND = 0, 1, 2

def quiescence(board, alpha, beta, engine_color, depth=0):
    if depth >= QUIESCENCE_MAX_DEPTH:
        return evaluate(board, engine_color)
    stand_pat = evaluate(board, engine_color)
    if stand_pat >= beta: return beta
    if alpha < stand_pat: alpha = stand_pat
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence(board, -beta, -alpha, not engine_color, depth+1)
            board.pop()
            if score >= beta: return beta
            if score > alpha: alpha = score
    return alpha

def minimax(board, engine_color, depth, alpha=-INF, beta=INF):
    key = board._transposition_key()
    if key in TT:
        tt_depth, tt_score, tt_flag = TT[key]
        if tt_depth >= depth:
            if tt_flag == EXACT: return tt_score
            if tt_flag == LOWERBOUND: alpha = max(alpha, tt_score)
            if tt_flag == UPPERBOUND: beta = min(beta, tt_score)
            if alpha >= beta: return tt_score

    if depth == MAX_DEPTH:
        return quiescence(board, alpha, beta, engine_color)

    best = -INF
    alpha_orig = alpha
    for move in ordered_moves(board):
        board.push(move)
        score = -minimax(board, engine_color, depth+1, -beta, -alpha)
        board.pop()
        best = max(best, score)
        alpha = max(alpha, score)
        if alpha >= beta: break

    if best <= alpha_orig: flag = UPPERBOUND
    elif best >= beta: flag = LOWERBOUND
    else: flag = EXACT
    TT[key] = (depth, best, flag)
    return best

def find_best_move(board, engine_color):
    fen = fen_key(board)

    if engine_color == chess.WHITE and fen in ITALIAN:
        return random.choice(ITALIAN[fen])
    if engine_color == chess.BLACK and fen in SICILIAN:
        return random.choice(SICILIAN[fen])

    TT.clear()
    eval_cache.clear()
    best_move = None
    best_score = -INF
    for move in ordered_moves(board):
        board.push(move)
        score = -minimax(board, engine_color, 1)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move.uci() if best_move else None


def check_game_over(board, session_id):
    if board.is_checkmate(): return True, "checkmate"
    if board.is_stalemate(): return True, "stalemate"
    history = position_history.get(session_id, [])
    if history.count(fen_key(board)) >= 3: return True, "threefold_repetition"
    return False, None

@app.route("/engine-move", methods=["POST"])
def engine_move():
    data = request.json
    session_id = data["sessionId"]
    board = get_board(session_id)
    if board is None:
        return jsonify({"game_over": True, "reason": "resignation"})

    if session_id not in engine_colors:
        engine_colors[session_id] = chess.WHITE if data["engineColor"]=="white" else chess.BLACK
    engine_color = engine_colors[session_id]

    over, reason = check_game_over(board, session_id)
    if over:
        end_session(session_id)
        return jsonify({"game_over": True, "reason": reason})
    
    if board.turn != engine_color:
        return jsonify({"move": None, "fen": board.fen()})

    move = find_best_move(board, engine_color)
    if move:
        board.push_uci(move)
        position_history[session_id].append(fen_key(board))

    over, reason = check_game_over(board, session_id)
    if over:
        end_session(session_id)

    return jsonify({
        "move": move,
        "fen": board.fen(),
        "game_over": over,
        "reason": reason
    })

@app.route("/resign", methods=["POST"])
def resign():
    session_id = request.json["sessionId"]
    resigned_sessions.add(session_id)
    end_session(session_id)
    return jsonify({"game_over": True, "reason": "resignation"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "active_sessions": len(active_boards)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
