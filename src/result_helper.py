import json
import io
import os
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from matplotlib.font_manager import FontProperties
import math

def capitalize_first(string):
    if not string:  # Handle empty string
        return string
    return string[0].upper() + string[1:].lower()

def json_to_csv(json_string):
    # Parse the JSON string
    data = json.loads(json_string)
    
    # Extract rounds and organize moves by player
    # Convert round numbers to integers for proper sorting
    rounds = sorted(data.keys(), key=int)  # Changed this line
    players_moves = {}

    # Initialize dictionary to hold moves for each player
    for round_num in rounds:
        for move in data[round_num]["players_moves"]:
            player_name = move.get("player_name", "Unknown")
            player_move = capitalize_first(move.get("move", "Unknown"))
            
            if player_name not in players_moves:
                players_moves[player_name] = []
            players_moves[player_name].append(player_move)

    # Use StringIO to capture the CSV output as a string
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=';')
    
    # Write the header row with round numbers
    header_row = ["Round #"] + rounds
    csv_writer.writerow(header_row)
    
    # Write each player's moves
    for player, moves in players_moves.items():
        row = [player] + moves
        csv_writer.writerow(row)

    # Get the CSV string
    csv_string = output.getvalue()
    output.close()
    
    return csv_string

def plot_rock_paper_scissors_results(csv_string, file_name):
    # Load CSV data into a DataFrame
    df = pd.read_csv(StringIO(csv_string), delimiter=';')
    df = df.set_index('Round #')

    # ====== Display Configuration Parameters ======
    # Font sizes
    HEADER_FONT_SIZE = 7      # Size for Round # and column headers
    CONTENT_FONT_SIZE = 7     # Size for moves (Rock/Paper/Scissors)
    PLAYER_FONT_SIZE = 7      # Size for player names

    # Cell dimensions
    ROUNDS_PER_GROUP = 10     # Maximum rounds per row
    ROUND_CELL_WIDTH = 0.6    # Width of each round cell
    CELL_HEIGHT = 0.25        # Height of each cell
    PLAYER_NAME_MULTIPLIER = 0.1  # Multiplier for player name column width
    PLAYER_NAME_PADDING = 0.2     # Additional padding for player name column
    GROUP_VERTICAL_GAP = 0.3  # Gap between groups

    # Margins and spacing
    MARGIN_SIZE = 0.05        # Margin around the entire plot
    
    # Colors
    WIN_COLOR = "green"
    LOSE_COLOR = "tomato"
    TIE_COLOR = "gray"

    # ====== Helper Functions ======
    def determine_winner(move1, move2):
        if move1 == move2:
            return "tie"
        elif (move1 == "Rock" and move2 == "Scissors") or \
             (move1 == "Scissors" and move2 == "Paper") or \
             (move1 == "Paper" and move2 == "Rock"):
            return "player1"
        else:
            return "player2"

    # ====== Layout Calculations ======
    total_rounds = len(df.columns)
    num_groups = math.ceil(total_rounds / ROUNDS_PER_GROUP)
    player_names = list(df.index) + ["Round #"]
    player_cell_width = max(len(name) for name in player_names) * PLAYER_NAME_MULTIPLIER + PLAYER_NAME_PADDING

    # Calculate figure height based on number of groups
    group_height = CELL_HEIGHT * 3  # Height of one group (including header)
    total_height = (group_height * num_groups) + (GROUP_VERTICAL_GAP * (num_groups - 1))
    
    # Initialize plot
    fig, ax = plt.subplots(figsize=(ROUNDS_PER_GROUP * ROUND_CELL_WIDTH + player_cell_width, total_height))

    def draw_group(start_round, num_rounds, vertical_offset):
        # Draw header row
        header_rect = plt.Rectangle((0, vertical_offset + CELL_HEIGHT * 2), 
                                  player_cell_width, CELL_HEIGHT, 
                                  facecolor='white', edgecolor='black')
        ax.add_patch(header_rect)
        ax.text(player_cell_width/2, vertical_offset + CELL_HEIGHT * 2.5, "Round #", 
                ha='center', va='center', fontsize=HEADER_FONT_SIZE, fontweight='bold')

        # Draw round numbers
        for col in range(num_rounds):
            round_num = start_round + col + 1
            round_rect = plt.Rectangle((player_cell_width + col * ROUND_CELL_WIDTH, 
                                      vertical_offset + CELL_HEIGHT * 2), 
                                     ROUND_CELL_WIDTH, CELL_HEIGHT, 
                                     facecolor='white', edgecolor='black')
            ax.add_patch(round_rect)
            ax.text(player_cell_width + col * ROUND_CELL_WIDTH + ROUND_CELL_WIDTH/2, 
                    vertical_offset + CELL_HEIGHT * 2.5, str(round_num), 
                    ha='center', va='center', fontsize=HEADER_FONT_SIZE, fontweight='bold')

        player1, player2 = df.index

        # Draw game results
        for col in range(num_rounds):
            move1 = df.iloc[0, start_round + col]
            move2 = df.iloc[1, start_round + col]
            result = determine_winner(move1, move2)

            color1 = WIN_COLOR if result == "player1" else LOSE_COLOR if result == "player2" else TIE_COLOR
            color2 = WIN_COLOR if result == "player2" else LOSE_COLOR if result == "player1" else TIE_COLOR

            rect1 = plt.Rectangle((player_cell_width + col * ROUND_CELL_WIDTH, 
                                 vertical_offset + CELL_HEIGHT), 
                                ROUND_CELL_WIDTH, CELL_HEIGHT, 
                                facecolor=color1, edgecolor='black')
            rect2 = plt.Rectangle((player_cell_width + col * ROUND_CELL_WIDTH, 
                                 vertical_offset), 
                                ROUND_CELL_WIDTH, CELL_HEIGHT, 
                                facecolor=color2, edgecolor='black')
            ax.add_patch(rect1)
            ax.add_patch(rect2)

            ax.text(player_cell_width + col * ROUND_CELL_WIDTH + ROUND_CELL_WIDTH/2, 
                    vertical_offset + CELL_HEIGHT * 1.5, move1, 
                    va='center', ha='center', color='black', fontsize=CONTENT_FONT_SIZE)
            ax.text(player_cell_width + col * ROUND_CELL_WIDTH + ROUND_CELL_WIDTH/2, 
                    vertical_offset + CELL_HEIGHT/2, move2, 
                    va='center', ha='center', color='black', fontsize=CONTENT_FONT_SIZE)

        # Draw player names
        player_rect1 = plt.Rectangle((0, vertical_offset + CELL_HEIGHT), 
                                   player_cell_width, CELL_HEIGHT, 
                                   facecolor='white', edgecolor='black')
        player_rect2 = plt.Rectangle((0, vertical_offset), 
                                   player_cell_width, CELL_HEIGHT, 
                                   facecolor='white', edgecolor='black')
        ax.add_patch(player_rect1)
        ax.add_patch(player_rect2)
        
        ax.text(player_cell_width/2, vertical_offset + CELL_HEIGHT * 1.5, player1, 
                va='center', ha='center', fontsize=PLAYER_FONT_SIZE, fontweight='bold')
        ax.text(player_cell_width/2, vertical_offset + CELL_HEIGHT/2, player2, 
                va='center', ha='center', fontsize=PLAYER_FONT_SIZE, fontweight='bold')

        # Draw outer border
        outer_rect = plt.Rectangle((0, vertical_offset), 
                                 player_cell_width + num_rounds * ROUND_CELL_WIDTH, 
                                 CELL_HEIGHT * 3, 
                                 fill=False, edgecolor='black', linewidth=1.5)
        ax.add_patch(outer_rect)

    # Draw each group
    for group in range(num_groups):
        start_round = group * ROUNDS_PER_GROUP
        remaining_rounds = total_rounds - start_round
        rounds_in_group = min(ROUNDS_PER_GROUP, remaining_rounds)
        vertical_offset = (group_height + GROUP_VERTICAL_GAP) * (num_groups - 1 - group)
        draw_group(start_round, rounds_in_group, vertical_offset)

    # Set plot limits
    ax.set_xlim(-MARGIN_SIZE, ROUNDS_PER_GROUP * ROUND_CELL_WIDTH + player_cell_width + MARGIN_SIZE)
    ax.set_ylim(-MARGIN_SIZE, total_height + MARGIN_SIZE)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('off')

    # Save and close the plot
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    plt.close()

def save_game_result(final_result, history):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the subfolder if it doesn't exist
    os.makedirs("game_outputs", exist_ok=True)
    
    # Modify the filename to include the subfolder
    filename = os.path.join("game_outputs", f"game_result_{timestamp}.txt")
    csv_filename = os.path.join("game_outputs", f"game_result_{timestamp}.csv")
    img_filename = os.path.join("game_outputs", f"game_result_{timestamp}.png")

    with open(filename, 'w') as file:
        file.write(final_result)
		
    with open(filename, 'a') as file:
        file.write("\n\n")
        file.write("game rounds history:")
        file.write("\n\n")
        file.write(history)

    csv_content = json_to_csv(history)

    # for debugging csv output only    
    # with open(csv_filename, 'w') as file:
    #     file.write(csv_content)

    plot_rock_paper_scissors_results(csv_content, img_filename)
    
def __main__():
    csv_data_5 = """Round #;1;2;3;4;5
    Doraemon;Rock;Rock;Rock;Rock;Rock
    claude-3-sonnet;Rock;Paper;Paper;Scissors;Paper
    """
    plot_rock_paper_scissors_results(csv_data_5, "rock_paper_scissors_result_5.png")

    
    csv_data_10 = """Round #;1;2;3;4;5;6;7;8;9;10
    Doraemon;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock
    claude-3-sonnet;Paper;Scissors;Rock;Scissors;Rock;Paper;Paper;Scissors;Rock;Paper
    """
    plot_rock_paper_scissors_results(csv_data_10, "rock_paper_scissors_result_10.png")
    
    csv_data_15 = """Round #;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15
    Doraemon;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors
    claude-3-sonnet;Paper;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper
    """
    plot_rock_paper_scissors_results(csv_data_15, "rock_paper_scissors_result_15.png")
    
    csv_data_20 = """Round #;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20
    Doraemon;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper
    claude-3-sonnet;Paper;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock
    """
    plot_rock_paper_scissors_results(csv_data_20, "rock_paper_scissors_result_20.png")
    
    csv_data_25 = """Round #;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25
    Doraemon;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock
    claude-3-sonnet;Paper;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors;Rock;Paper;Scissors
    """
    plot_rock_paper_scissors_results(csv_data_25, "rock_paper_scissors_result_25.png")
    
if __name__ == "__main__":
    __main__()