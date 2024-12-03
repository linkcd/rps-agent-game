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

# Use following code for generating graph
# try:
#     graph_png = app.get_graph().draw_mermaid_png()
#     with open("doc/generated_graph.png", "wb") as f:
#         f.write(graph_png)
#     print(f"Graph saved")
# except Exception as e:
#     print(f"Failed to save graph: {e}")
#     pass