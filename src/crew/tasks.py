from crewai import Task
from textwrap import dedent

from pydantic import BaseModel

class PlayerOutput(BaseModel):
    player_name: str
    move: str
    
class JudgeOutput(BaseModel):
    winner: str


class GameTasks:
	def play_game(self, agent):
		return Task(
			description=dedent(f"""\
				Make you move to play Rock paper scissors. 

				The Game Rules:
				- Rock beats Scissors (Rock crushes Scissors)
				- Scissors beat Paper (Scissors cut Paper)
				- Paper beats Rock (Paper covers Rock)
    
				Based on above rules, carefully choose one and only one of the following shapes:
				- Rock
				- Paper
				- Scissors
				"""),
			expected_output=dedent(f"""\
       			The output is a json:
				- player_name: name of the player
				- move: the selected shape
          		"""),
			agent=agent,
   			output_pydantic=PlayerOutput,
			verbose=True,
		)
  
	def judge_game(self, agent):
		return Task(
			description=dedent(f"""\
				Decide who is the winner of the game.

				Here is the game rules:
				- Rock beats Scissors (Rock crushes Scissors)
				- Scissors beat Paper (Scissors cut Paper)
				- Paper beats Rock (Paper covers Rock)
				"""),
			agent=agent,
   			expected_output=dedent(f"""\
				the name of the winner
          		"""),
      		output_pydantic=JudgeOutput,
   			verbose=True,
		)
  

