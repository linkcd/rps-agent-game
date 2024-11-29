from dotenv import load_dotenv
from src.graph import GraphBuilder
from src.state import GameState, RoundState, JudgeResult
import argparse

load_dotenv()

# Create argument parser
parser = argparse.ArgumentParser(description='Game State Configuration')
parser.add_argument('--max_round', type=int, default=3,
                   help='Maximum number of rounds (default: 3)')

# Parse arguments
args = parser.parse_args()
max_round = args.max_round

input = GameState(
            max_round=max_round,
            current_round_number=0,  # Start with round number 0
            round_history={}   # Empty dictionary for game round results
    )

app = GraphBuilder().app

app.invoke(input, {"recursion_limit": 500})

# for chunk in app.stream(input, stream_mode="debug"):
#     node_name = list(chunk.keys())[0]
#     print(f"---------- Update from node {node_name} ---------")
#     print(chunk)