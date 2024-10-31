import asyncio
from .flow import GameFlow

class Nodes():
	def run_game(self, state):
		print(f"## Run a new game, the init state is {state}")
		print("game number + 1...")

		state.game_number += 1
		print(f"after added 1, the new state is {state}")
  
		flow = GameFlow(state)
		asyncio.run(flow.kickoff())
  
		print(f"After the game run, the output is {state}")
		return flow.state

	def check_if_need_more_round(self, state):
		print(f"CHECK if we need continue. The current status is {state}!!!")
		if state.game_number > 3:
			print("## max round reached")
			return "end"
		else:
			print("## need more round")
		return "continue"

	# def announce_winner(self, state):
	# 	print("!!!Winner!!!")
	# 	print(str(state))

