const game = new Chess();
let moveHistory = [game.fen()];
let historyPointer = 0;

let bottomWhite=true

const files = ['a','b','c','d','e','f','g','h'];
const ranks = ['8','7','6','5','4','3','2','1'];

const pieceImageMap = {
    r:'chess_images/br.png', n:'chess_images/bn.png',
    b:'chess_images/bb.png', q:'chess_images/bq.png',
    k:'chess_images/bk.png', p:'chess_images/bp.png',
    R:'chess_images/wr.png', N:'chess_images/wn.png',
    B:'chess_images/wb.png', Q:'chess_images/wq.png',
    K:'chess_images/wk.png', P:'chess_images/wp.png'
};

function generateSessionId() {
    return crypto.randomUUID();
}
let sessionId = null;

let boardOrientation = 'white';
let engine_color = null;
let humanColor = null;

let vsBot = false;
let selectedSquare = null;
let engineThinking = false;

const backendURL = "http://127.0.0.1:5000";

function startGameAsPlayer(){
    vsBot=false;
    document.getElementById('mainMenu').style.display='none';
    document.getElementById('gameArea').style.display='block';
    playNewGame();
}

function startGameAsBot(){
    vsBot=true;
    document.getElementById('mainMenu').style.display='none';
    document.getElementById('gameArea').style.display='block';
    playNewGame();
}

function goToHome(){ location.reload(); }

async function playNewGame(){
    game.reset();
    moveHistory=[game.fen()];
    historyPointer=0;
    selectedSquare=null;
    engineThinking=false;
    sessionId=generateSessionId();
    randomizeOrientation();
    createChessboard();
    closeModal();
    if (vsBot) {
        await fetch(`${backendURL}/start-session`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
    },
    body: JSON.stringify({
        sessionId: sessionId,
        engineColor: engine_color
    })
});

    }
    if (vsBot && game.turn() === engine_color) {
    await maybeEngineMove();
    }
}

function currentTurnColor() {
    return game.turn();
}

function canHumanMove() {
    if (!vsBot) return true;
    return game.turn() === humanColor;
}


function canSelectPiece(piece) {
    if (!piece) return false;

    if (!vsBot) {
        return piece.color === game.turn();
    }

    return piece.color === humanColor;
}

function randomizeOrientation() {
    bottomWhite = Math.random() < 0.5;
    boardOrientation = bottomWhite ? 'white' : 'black';

    if (vsBot) {
        humanColor = bottomWhite ? 'w' : 'b';
        engine_color = humanColor === 'w' ? 'b' : 'w';
    } else {
        humanColor = null;
        engine_color = null;
    }
}


function createChessboard(forceBottomWhite = null) {
    const board = document.getElementById('chessboard');
    board.innerHTML = '';

    const boardState = game.board();

    const orientation = forceBottomWhite !== null ? forceBottomWhite : bottomWhite;

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const sq = document.createElement('div');
            sq.className = 'square';
            
            let rankIndex, fileIndex;
            if (orientation) {
                rankIndex = i;
                fileIndex = j;
            } else {
                rankIndex = 7 - i;
                fileIndex = 7 - j;
            }

            const pos = files[fileIndex] + ranks[rankIndex];
            sq.dataset.position = pos;
            sq.style.backgroundColor = (i + j) % 2 === 0 ? '#f0d9b5' : '#b58863';

            const piece = boardState[rankIndex][fileIndex];
            if (piece) {
                const letter = piece.color === 'w' ? piece.type.toUpperCase() : piece.type.toLowerCase();
                const img = document.createElement('img');
                img.src = pieceImageMap[letter];
                img.style.width = '55px';
                img.style.height = '55px';
                sq.appendChild(img);
            }

            board.appendChild(sq);
        }
    }
    updateStatus();
}






function clearDots(){ document.querySelectorAll('.legal-move-dot').forEach(d=>d.remove()); }
function displayLegalMoves(moves){ moves.forEach(m=>{
    const sq=document.querySelector(`[data-position="${m.to}"]`);
    if(sq){ const dot=document.createElement('div'); dot.className='legal-move-dot'; sq.appendChild(dot);}
}); }
function updateStatus(){
    const status=document.getElementById('status');
    const color=game.turn()==='w'?'White':'Black';
    status.textContent=engineThinking?'Engine thinking...':`${color} to move${game.in_check()?'. Check!':''}`;
}

async function startGame(engineColor) {
    const sessionId = generateSessionId();

    await fetch("http://127.0.0.1:5000/start-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            sessionId: sessionId,
            engineColor: engineColor
        })
    });
    maybeEngineMove(sessionId, engineColor);
}


async function maybeEngineMove() {
    if (!vsBot || engineThinking) return;
    if (game.turn() !== engine_color) return;

    engineThinking = true;
    updateStatus();

    try {
        const res = await fetch(`${backendURL}/engine-move`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sessionId: sessionId,
                engineColor: engine_color,
            })
        });

        const data = await res.json();
        console.log("Engine response:", data);

        if (data.move) {
            game.move({
                from: data.move.slice(0, 2),
                to: data.move.slice(2, 4),
                promotion: 'q'
            });
            recordMove();
            createChessboard();
        }

        if (data.game_over) {
            showGameOverModal(data.reason);
        }
    } catch (err) {
        console.error("Error fetching engine move:", err);
    } finally {
        engineThinking = false;
        updateStatus();
    }
}



document.getElementById('chessboard').addEventListener('click', async e => {
    if (engineThinking || game.game_over()) return;
    if (!canHumanMove()) return;

    let sq = e.target;
    if (sq.tagName === 'IMG') sq = sq.parentElement;
    if (!sq.dataset.position) return;

    const pos = sq.dataset.position;

    if (selectedSquare) {
        const moveObj = game.move({
            from: selectedSquare,
            to: pos,
            promotion: 'q'
        });
        clearDots();
        selectedSquare = null;
        if (moveObj) {
            recordMove();
            createChessboard();
            if (vsBot) {
                engineThinking = true;
                updateStatus();

                let humanMove = moveObj.from + moveObj.to;
                if (moveObj.promotion) humanMove += moveObj.promotion;
                console.log("Sending human move to backend:", humanMove);

                try {
                    const res = await fetch(`${backendURL}/engine-move`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            sessionId: sessionId,
                            engineColor: engine_color,
                            humanMove
                        })
                    });
                    const data = await res.json();
                    console.log("Engine response:", data);

                    if (data.move) {
                        game.move({
                            from: data.move.slice(0, 2),
                            to: data.move.slice(2, 4),
                            promotion: 'q'
                        });
                        recordMove();
                        createChessboard();
                    }

                    if (data.game_over) showGameOverModal(data.reason);
                } catch (err) {
                    console.error("Error fetching engine move:", err);
                } finally {
                    engineThinking = false;
                    updateStatus();
                }
            }
        }
    } else {
        const piece = game.get(pos);
        if (canSelectPiece(piece)) {
            selectedSquare = pos;
            clearDots();
            displayLegalMoves(
                game.moves({ square: pos, verbose: true })
            );
        }
    }
    console.log({
        humanColor,
        turn: game.turn(),
        engineThinking,
        clickedPos: e.target.dataset.position
    });
});




function recordMove(){
    if(historyPointer<moveHistory.length-1) moveHistory=moveHistory.slice(0,historyPointer+1);
    moveHistory.push(game.fen());
    historyPointer=moveHistory.length-1;
}
function goBack(){ if(historyPointer>0){ historyPointer--; game.load(moveHistory[historyPointer]); createChessboard(); } }
function goForward(){ if(historyPointer<moveHistory.length-1){ historyPointer++; game.load(moveHistory[historyPointer]); createChessboard(); } }

function showGameOverModal(msg){ document.getElementById('modalMessage').textContent=msg; document.getElementById('gameOverModal').style.display='flex'; }
function closeModal(){ document.getElementById('gameOverModal').style.display='none'; }
function resignGame(){ if(vsBot) fetch(`${backendURL}/resign`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({sessionId})}); showGameOverModal("You resigned."); }

