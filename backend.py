import chess
import random
import time

# Opening book data
LONDON = {
    "rnbqkb1r/ppp1pppp/5n2/3p4/3P4/5N2/PPP1BPPP/RNBQK2R w KQkq": ["e3", "c3"],
    "rnbqkb1r/pp2pppp/5n2/2pp4/3P4/5N2/PPP1BPPP/RNBQK2R w KQkq": ["c3", "e3"],
    "r1bqkb1r/ppp1pppp/2n2n2/3p4/3P1B2/5N2/PPP1BPPP/RN1QK2R w KQkq -": ["e3", "c3", "Nc3"]
}

JOBAVA_LONDON = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["d2d4"],
    # 1.d4 Nf6 2.Nc3 d5 3.Bf4
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq": ["b1c3"],
    "r1bqkbnr/ppp1pppp/2n5/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq": ["c1f4"],
    "rnbqkb1r/ppp1pppp/5n2/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR w KQkq": ["c1f4"],
    "rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/2N5/PPP2PPP/R2QKBNR b KQkq": ["c5", "g6", "e6"],
    "r1bqkb1r/ppp1pppp/2n2n2/3p4/3P1B2/2N5/PPP1PPPP/R2QKBNR w KQkq": ["c3b5"],
    "r1bqkb1r/ppp2ppp/2n2n2/1N1pp3/3P1B2/8/PPP1PPPP/R2QKBNR w KQkq": ["d4e5"],
    "r1bqkb1r/ppp2ppp/2n5/1N1pP3/5Bn1/8/PPP1PPPP/R2QKBNR w KQkq": ["d1d5"],
    "r1b1kb1r/ppp2ppp/2n5/1N1qP3/5Bn1/8/PPP1PPPP/R3KBNR w KQkq": ["b5c7"],
    "r1bqkb1r/ppp2ppp/2n5/1N1pP2n/5B2/8/PPP1PPPP/R2QKBNR w KQkq": ["dxd4"],
    "r1bqkb1r/ppp2ppp/2n5/1N1pP2n/5B2/8/PPP1PPPP/R2QKBNR w KQkq": ["bxc7"],

    # 4.e3 Nc6 5.Nb5
    "r1bqkb1r/ppp1pppp/2n2n2/1N1p4/3P1B2/2N1P3/PPP2PPP/R2QKBNR b KQkq": ["cxd4", "a6", "e5"],

    # 5...a6 6.Nc7+ Kd7
    "r1bq1b1r/ppn1pppp/8/3p4/3P1B2/2N1P3/PPP2PPP/R2QKBNR w KQ": ["Nc3", "Bd3", "Qf3"],

    # 6.Bd3 e6 7.Nf3 Bd6 8.Ne5+
    "r1bqkb1r/pp2pppp/2n1b3/4N3/3P1B2/2N1P3/PPP2PPP/R2QK2R b KQkq": ["Bxe5", "Nxe5", "Qe7"],

    # 8...Bxe5 9.dxe5 Ng8 10.Qg4 g6
    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["h4", "0-0", "O-O"],

    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["h4", "h5", "h6"],
    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["Qg3", "Qh3", "Qf3"],

    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["Bd3", "Be2", "Qd2", "O-O"],

    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R b KQkq": ["Nh5", "h5", "Nc6"],
    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["h5", "Qh6", "0-0"],

    # Kingside pressure
    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["Bh6", "e4", "g4"],

    "r1bqk2r/pp2ppbp/6p1/4P3/6Q1/2N1P3/PPP3PP/R3K2R w KQkq": ["O-O-O", "Qh6", "g5"]
}


ENGLISH = {
    "r1bqkbnr/pppp1ppp/2n5/4p3/2P5/2N5/PP1P1PPP/R1BQKBNR w KQkq": ["Bg2", "Nf3"],
    "r1bqkbnr/pppp1pp1/2n3p1/4p3/2P5/2N5/PP1P1PPP/R1BQKBNR w KQkq": ["Bg2", "Nf3"],
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2P5/2N5/PP1P1PPP/R1BQKBNR w KQkq": ["Bg2", "Nf3", "Bg2"]
}


ITALIAN = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["e2e4"],
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq": ["e7e5"],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq": ["g1f3"],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq": ["b8c6"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq": ["f1c4"],

    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq": ["g8f6"],
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq": ["f3g5"],
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq": ["b2b4"],
    "r1bqk1nr/pppp1ppp/2n5/4p3/1bB1P3/5N2/P1PP1PPP/RNBQK2R w KQkq": ["c2c3"]
}

SICILIAN_NAJDORF = {
    # Main line
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq": ["d7d6"],
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["e2e4"],
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq": ["c7c5"],
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq": ["g1f3"],
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq": ["d7d6"],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq": ["d7d6"],
    "rnbqkbnr/pp2pppp/3p4/8/3NP3/8/PPP2PPP/RNBQKB1R b KQkq": ["g8f6"],
    "rnbqkb1r/pp2pppp/3p1n2/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq": ["g7g6", "a7a6"],

    # Scheveningen setup
    "rnbqkbnr/pp1p1ppp/2p1p3/8/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq": ["d2d4"],

    # Flexible branching
    "rnbqkbnr/pp1p1ppp/2p1p3/8/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq": ["c5d4", "Nc6"],

    # Another key pointing to same main idea (open center)
    "rnbqkbnr/pp1p1ppp/2p1p3/8/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq": ["a6"],  # Najdorf typical idea
}

SICILIAN_DRAGON = {
    # Main line
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["e2e4"],
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq": ["c7c5"],
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq": ["g1f3"],
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq": ["d7d6"],

    # Dragon setup
    "rnbqkbnr/pp1pp1pp/2p2p2/8/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq": ["d2d4"],
    "rnbqkbnr/pp1pp1pp/2p2p2/8/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq": ["c5xd4"],

    # Flexible Dragon key
    "rnbqkbnr/pp1pp1pp/2p2p2/8/3P4/2N2N2/PPP2PPP/R1BQKB1R b KQkq": ["g8f6"],

    # Yugoslav Attack example
    "rnbqkb1r/pp1pp1pp/2p2pn1/8/3P4/2N2N2/PPP2PPP/R1BQKB1R w KQkq": ["f1c4", "Bc4"],

    # Covering Alapin e4 c3
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/2P5/PP1P1PPP/RNBQKBNR b KQkq": ["d7d6"],
    "rnbqkbnr/pp1ppppp/2p2n2/8/4P3/2P5/PP1P1PPP/RNBQKBNR w KQkq": ["g1f3"],

    # Covering Open Sicilian lines (Nc3 instead of Nf3)
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/2N5/PPP2PPP/R1BQKBNR b KQkq": ["d7d6"],
    "rnbqkbnr/pp1ppppp/2p2n2/8/4P3/2N5/PPP2PPP/R1BQKBNR w KQkq": ["g1f3"],

    # Generic fallback positions
    "rnbqkb1r/pp1ppppp/2p2n2/8/3PP3/2N5/PPP2PPP/R1BQKB1R b KQkq": ["g8f6", "e6", "a6"],
    "rnbqkb1r/pp1ppppp/2p2n2/8/3PP3/2N2N2/PPP2PPP/R1BQKB1R b KQkq": ["g8f6", "e6", "a6"],
}



QUEENS_GAMBIT = {
    # Queen's Gambit Declined
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["d2d4"],
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq": ["d7d5"],
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq": ["c2c4"],

    # Queen's Gambit Accepted
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["d2d4"],
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq": ["d7d5"],
    "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq": ["c2c4"],
    "rnbqkbnr/ppp2ppp/8/3p4/2PP4/8/PP3PPP/RNBQKBNR b KQkq": ["d5c4"],
}

CARO_KANN = {
    # 1.e4 c6
    "rnbqkbnr/pp1ppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq": ["d5"],

    # 2.d4 d5
    "rnbqkbnr/pp1ppppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq": ["exd5", "Nc3", "e5"],

    # 3.exd5 cxd5
    "rnbqkbnr/pp1ppppp/8/3p4/8/8/PPPP1PPP/RNBQKBNR w KQkq": ["Nc3", "Nf3", "c4"],

    # Classical Variation
    "rnbqkbnr/pp1ppppp/2n5/3p4/8/2N2N2/PPPP1PPP/R1BQKB1R w KQkq": ["Be2", "Bb5", "h3"],
    "rnbqkb1r/pp1ppppp/2n5/3p4/3P4/2N2N2/PPP1BPPP/R1BQK2R b KQkq": ["e6", "Bg4"],

    # Tartakower
    "rnbqkb1r/pp1p1ppp/4pn2/3P4/8/2N5/PPP2PPP/R1BQKBNR w KQkq": ["Nf3", "Be3", "h4"],
    "rnbqkb1r/pp1p1ppp/4p3/3P4/3P4/2N5/PPP2PPP/R1BQKBNR b KQkq": ["Bg6", "Nd7"],

    # Panov-Botvinnik Attack
    "rnbqkb1r/pp1ppppp/5n2/2b5/2P5/5N2/PP1P1PPP/RNBQKB1R w KQkq": ["Bxc4", "Qa4+"],
    "rnbqkb1r/pp1ppppp/5n2/2b5/2B5/5N2/PP1P1PPP/RNBQK2R b KQkq": ["e6", "Bg6"],

    # Advance Variation
    "rnbqkb1r/pp1p1ppp/4p3/4P3/8/5N2/PPP1BPPP/RNBQ1RK1 w KQkq": ["Be3", "Nh4", "h3"],
    "rnbqkb1r/pp1p1ppp/4p3/4P3/8/4BN2/PPP2PPP/RNBQ1RK1 b KQkq": ["Nd7", "Be7"],

    # Fantasy Variation
    "rnbqkb1r/pp1ppppp/8/3pB3/4P3/2N5/PPP2PPP/R1BQK1NR w KQkq": ["g5", "Be3"],
    "rnbqkb1r/pp1ppppp/8/3pB3/4P3/2N5/PPP2PPP/R1BQK1NR b KQkq": ["Qh4+", "h5"],

    # Modern Variation
    "rnbqk1nr/pp1pppbp/5np1/8/3PP3/3B1N2/PPP2PPP/RNBQK2R w KQkq": ["c3", "0-0"],
    "rnbqk1nr/pp1pppbp/5np1/8/3PP3/3B1N2/PPP2PPP/RNBQK2R b KQkq": ["Bg4", "Nd5"],

    "rnbqk1nr/pp1pppbp/5np1/8/3PP3/3B1N2/PPP2PPP/RNBQK2R w KQkq": ["c3", "0-0", "Be3", "Qe2"],
    "rnbqk1nr/pp1pppbp/5np1/8/3PP3/3B1N2/PPP2PPP/RNBQK2R b KQkq": ["Bg4", "Nd5", "Nxe3", "Be7"],
}



KINGS_INDIAN = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq": ["d2d4"],
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq": ["g8f6"],
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq": ["c2c4"],
    "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP3PPP/RNBQKBNR b KQkq": ["g7g6"],
    "rnbqkb1r/ppppp1pp/5pn1/8/2PP4/8/PP3PPP/RNBQKBNR w KQkq": ["g1f3"],
}

WHITE_LIBRARY = {
    "W Daniel Naroditsky": JOBAVA_LONDON,
    "London": LONDON,
    "English": ENGLISH,
    "Queens Gambit": QUEENS_GAMBIT,
    "Italian": ITALIAN,
}

BLACK_LIBRARY = {
    "Kings Indian": KINGS_INDIAN,
    "Caro-Kann": CARO_KANN,
    "Sicilian Najdorf": SICILIAN_NAJDORF,
    "Sicilian Dragon": SICILIAN_DRAGON,
}

# Chess engine constants
INF = float('inf')
MAX_DEPTH = 5
QUIESCENCE_MAX_DEPTH = 2

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

eval_cache = {}

CENTER_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]
PIECE_SQUARE_TABLES = {
    chess.PAWN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10,-20,-20, 10, 10, 5,
        5, -5,-10, 0, 0,-10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5,10,25,25,10, 5, 5,
        10,10,20,30,30,20,10,10,
        50,50,50,50,50,50,50,50,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20, 0, 5, 5, 0,-20,-40,
        -30, 5,10,15,15,10, 5,-30,
        -30, 0,15,20,20,15, 0,-30,
        -30, 5,15,20,20,15, 5,-30,
        -30, 0,10,15,15,10, 0,-30,
        -40,-20, 0, 0, 0, 0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10, 0, 0, 0, 0, 0, 0,-10,
        -10, 0, 5,10,10, 5, 0,-10,
        -10, 5, 5,10,10, 5, 5,-10,
        -10, 0,10,10,10,10, 0,-10,
        -10,10,10,10,10,10,10,-10,
        -10, 5, 0, 0, 0, 0, 5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0,-5,
        -5, 0, 0, 0, 0, 0, 0,-5,
        -5, 0, 0, 0, 0, 0, 0,-5,
        -5, 0, 0, 0, 0, 0, 0,-5,
        -5, 0, 0, 0, 0, 0, 0,-5,
        5,10,10,10,10,10,10,5,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    chess.QUEEN: [0]*64,
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30,10, 0, 0,10, 30, 20
    ]
}

TT = {}
EXACT, LOWERBOUND, UPPERBOUND = 0, 1, 2


# Helper functions
def fen_key(board):
    return " ".join(board.fen().split(" ")[:4])


def material_score(board, color):
    score = 0
    for piece, value in PIECE_VALUES.items():
        score += value * (len(board.pieces(piece, color)) - len(board.pieces(piece, not color)))
    return score


def game_phase(board):
    total_pieces = len(board.piece_map())
    halfmoves = board.fullmove_number * 2 - (0 if board.turn == chess.WHITE else 1)

    if halfmoves <= 20:
        return "opening"
    elif total_pieces <= 10:
        return "endgame"
    else:
        return "middlegame"


def development_score(board, color):
    score = 0

    for sq in board.pieces(chess.KNIGHT, color):
        if chess.square_rank(sq) not in (0, 7):
            score += 20

    for sq in board.pieces(chess.BISHOP, color):
        if chess.square_rank(sq) not in (0, 7):
            score += 20

    king_sq = board.king(color)
    if color == chess.WHITE and king_sq in [chess.G1, chess.C1]:
        score += 40
    elif color == chess.BLACK and king_sq in [chess.G8, chess.C8]:
        score += 40

    king_sq = board.king(color)
    if color == chess.WHITE and king_sq in (chess.G1, chess.C1):
        score += 40
    elif color == chess.BLACK and king_sq in (chess.G8, chess.C8):
        score += 40

    return score


def endgame_bonus(board, engine_color):
    score = 0
    king_sq = board.king(engine_color)
    if king_sq is not None:
        rank = chess.square_rank(king_sq)
        file = chess.square_file(king_sq)
        score += 10 * (4 - abs(rank - 3.5))
        score += 10 * (4 - abs(file - 3.5))

    for sq in board.pieces(chess.PAWN, engine_color):
        rank = chess.square_rank(sq)
        if engine_color == chess.WHITE:
            score += rank * 10
        else:
            score += (7 - rank) * 10
    return score


def middlegame_bonus(board, engine_color):
    score = 0
    enemy_king_sq = board.king(not engine_color)
    if enemy_king_sq is not None:
        attackers = board.attackers(engine_color, enemy_king_sq)
        score += len(attackers) * 50

    for rook_sq in board.pieces(chess.ROOK, engine_color):
        file = chess.square_file(rook_sq)
        if all(board.piece_at(chess.square(file, r)) is None for r in range(8)):
            score += 20

    score += 2 * len(list(board.legal_moves)) if any(board.piece_at(sq).piece_type == chess.QUEEN for sq in board.pieces(chess.QUEEN, engine_color)) else 0
    return score


def trading_bonus(board, engine_color):
    material = material_score(board, engine_color)
    enemy_material = material_score(board, not engine_color)
    if material > enemy_material:
        for move in board.legal_moves:
            if board.is_capture(move) and board.piece_at(move.from_square).piece_type != chess.PAWN:
                return 20
    return 0


def queen_early_penalty(board, color):
    queen_sq = next(iter(board.pieces(chess.QUEEN, color)), None)
    if queen_sq is None:
        return 0

    if game_phase(board) == "opening" and chess.square_rank(queen_sq) not in (0, 7):
        return -40

    return 0


def pawn_structure(board, color):
    score = 0
    pawns = board.pieces(chess.PAWN, color)
    files = {}

    for sq in pawns:
        f = chess.square_file(sq)
        files.setdefault(f, []).append(sq)

    for f, squares in files.items():
        if len(squares) > 1:
            score -= 15 * (len(squares) - 1)

        for sq in squares:
            if f - 1 not in files and f + 1 not in files:
                score -= 10

    return score


def center_control(board, color):
    score = 0
    weight = 30 if game_phase(board) == "opening" else 10

    for sq in CENTER_SQUARES:
        score += weight * (
            len(board.attackers(color, sq)) -
            len(board.attackers(not color, sq))
        )

    return score


def evaluate(board, engine_color):
    game_phase(board)
    fen = board.fen()
    if fen in eval_cache:
        return eval_cache[fen]

    if board.is_checkmate():
        score = -100000 if board.turn == engine_color else 100000
        eval_cache[fen] = score
        return score

    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        for sq in board.pieces(piece_type, engine_color):
            score += value
            score += PIECE_SQUARE_TABLES[piece_type][sq]

        for sq in board.pieces(piece_type, not engine_color):
            score -= value
            score -= PIECE_SQUARE_TABLES[piece_type][sq]

    score += development_score(board, engine_color)
    score -= development_score(board, not engine_color)

    score += pawn_structure(board, engine_color)
    score -= pawn_structure(board, not engine_color)

    score += center_control(board, engine_color)
    score -= center_control(board, not engine_color)

    score += queen_early_penalty(board, engine_color)
    score -= queen_early_penalty(board, not engine_color)

    king_sq = board.king(engine_color)
    if king_sq:
        score -= 30 * len(board.attackers(not engine_color, king_sq))

        phase = game_phase(board)
    if game_phase(board) == "opening":
        pass
    elif game_phase(board) == "middlegame":
        score += middlegame_bonus(board, engine_color)
    elif game_phase(board) == "endgame":
        score += endgame_bonus(board, engine_color)
    eval_cache[fen] = score
    return score


def ordered_moves(board):
    moves = list(board.legal_moves)
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)
    return moves


def quiescence(board, alpha, beta, engine_color, depth=0):
    if depth >= QUIESCENCE_MAX_DEPTH:
        return evaluate(board, engine_color)
    stand_pat = evaluate(board, engine_color)
    if stand_pat >= beta: return beta
    if alpha < stand_pat: alpha = stand_pat
    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence(board, -beta, -alpha, engine_color, depth+1)
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


def fen_key_for_book(board):
    parts = board.fen().split(" ")
    piece_placement = parts[0]
    active_color = parts[1]
    castling = parts[2]
    ep_square = parts[3] if parts[3] != '-' else ''

    key = f"{piece_placement} {active_color} {castling}"
    if ep_square:
        key += f" {ep_square}"

    return key


def find_best_move(board, engine_color):
    key = fen_key_for_book(board)
    print("Board FEN:", board.fen())
    print("Engine color:", "white" if engine_color==chess.WHITE else "black")
    print("Book key:", repr(key))

    library = WHITE_LIBRARY if engine_color == chess.WHITE else BLACK_LIBRARY

    for opening_name, opening_book in library.items():
        if key in opening_book:
            move = random.choice(opening_book[key])
            print(f"Book hit ({'White' if engine_color==chess.WHITE else 'Black'}) - {opening_name}: {move}")

            time.sleep(0.8)

            return move

    TT.clear()
    eval_cache.clear()
    best_move = None
    best_score = -INF
    for move in ordered_moves(board):
        board.push(move)
        score = -minimax(board, engine_color, 2)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    if best_move is None:
        return None
    print("Search chose:", best_move.uci(), "score:", best_score)
    return best_move.uci()


def check_game_over(board, session_id, position_history):
    if board.is_checkmate(): return True, "checkmate"
    if board.is_stalemate(): return True, "stalemate"
    history = position_history.get(session_id, [])
    if history.count(fen_key(board)) >= 3: return True, "threefold_repetition"
    return False, None


class ChessSessionManager:
    def __init__(self):
        self.active_boards = {}
        self.position_history = {}
        self.resigned_sessions = set()
        self.engine_colors = {}

    def start_session(self, session_id, engine_color):
        """Start a new chess session"""
        # Clean up any existing session
        self.end_session(session_id)

        # Create new board and initialize history
        self.active_boards[session_id] = chess.Board()
        self.position_history[session_id] = [fen_key(self.active_boards[session_id])]
        self.engine_colors[session_id] = engine_color

        return {"ok": True}

    def get_board(self, session_id):
        """Get the board for a session, or None if resigned"""
        if session_id in self.resigned_sessions:
            return None
        if session_id not in self.active_boards:
            self.active_boards[session_id] = chess.Board()
            self.position_history[session_id] = [fen_key(self.active_boards[session_id])]
        return self.active_boards[session_id]

    def end_session(self, session_id):
        """End a session and clean up resources"""
        self.active_boards.pop(session_id, None)
        self.position_history.pop(session_id, None)
        self.resigned_sessions.discard(session_id)
        self.engine_colors.pop(session_id, None)
        if len(eval_cache) > 20000:
            eval_cache.clear()

    def resign(self, session_id):
        """Handle resignation"""
        self.resigned_sessions.add(session_id)
        self.end_session(session_id)
        return {"game_over": True, "reason": "resignation"}

    def make_move(self, session_id, human_move=None, engine_color=None):
        """Process a move and return the game state"""
        board = self.get_board(session_id)
        if board is None:
            return {"game_over": True, "reason": "resignation"}

        # Set engine color if not already set
        if session_id not in self.engine_colors and engine_color is not None:
            self.engine_colors[session_id] = engine_color

        current_engine_color = self.engine_colors.get(session_id, chess.WHITE)

        # Apply human move if provided
        if human_move:
            try:
                board.push_uci(human_move)
                self.position_history[session_id].append(fen_key(board))
                print(f"Human move applied: {human_move}")
            except ValueError:
                print(f"Illegal human move received: {human_move}")
                return {"move": None, "fen": board.fen()}

        print("Board FEN after human move:", board.fen())
        print("Board turn:", "white" if board.turn == chess.WHITE else "black")
        print("Engine color:", "white" if current_engine_color == chess.WHITE else "black")

        # Check if it's engine's turn
        if board.turn != current_engine_color:
            print("EARLY RETURN: not engine's turn")
            return {"move": None, "fen": board.fen()}

        # Find and make engine move
        move = find_best_move(board, current_engine_color)
        if move:
            board.push_uci(move)
            self.position_history[session_id].append(fen_key(board))
            print("Engine move added:", move)

        # Check if game is over
        over, reason = check_game_over(board, session_id, self.position_history)
        if over:
            self.end_session(session_id)

        return {
            "move": move,
            "fen": board.fen(),
            "game_over": over,
            "reason": reason
        }
