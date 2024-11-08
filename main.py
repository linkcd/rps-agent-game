from dotenv import load_dotenv
from src.graph import GraphBuilder
from src.state import GameState, RoundState, JudgeResult

load_dotenv()

input = GameState(
            current_round_number=0,  # Start with round number 0
            round_history={}   # Empty dictionary for game round results
    )

app = GraphBuilder().app

app.invoke(input, {"recursion_limit": 500})

# for chunk in app.stream(input, stream_mode="debug"):
#     node_name = list(chunk.keys())[0]
#     print(f"---------- Update from node {node_name} ---------")
#     print(chunk)