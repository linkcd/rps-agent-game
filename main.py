from src.graph import GraphBuilder
from src.state import GameState, RoundState, JudgeResult

app = GraphBuilder().app
app.invoke(GameState(
            current_round_number=0,  # Start with round number 0
            round_history={}   # Empty dictionary for game round results
    ))