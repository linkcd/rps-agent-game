import json

from langsmith import traceable
from langchain_core.messages import HumanMessage, AIMessage
from langchain_aws import ChatBedrock
from crewai import LLM

from .state import PlayersMove, JudgeResult, RoundState, GameState
from .crew.crew import PlayerCrew, JudgeCrew
from .result_helper import save_game_result

class Nodes():
	def start_new_round(self, state: GameState) -> GameState:
		print(f"## Before a new game starts, the previous state is {state}")
		round_number = state["current_round_number"] + 1
		state["current_round_number"] = round_number
		state["current_round_state"] = RoundState(
			round_number=round_number,
			players_moves=[],
			judge_result={}
		)
		return state
	
	@traceable 
	def player1(self, state: GameState) -> GameState:
		print(f"p1 input state: {state}")
		player_llm = LLM(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0", temperature=0.1)
		player_crew = PlayerCrew("claude-3-sonnet", player_llm)
        
		pr = player_crew.crew.kickoff(inputs={"round_history": state["round_history"]}).pydantic.model_dump()
		print("player 1: ", pr)
		state["current_round_state"]["players_moves"].append(pr)

	@traceable 
	def player2(self, state: GameState) -> GameState:
		print(f"p2 input state: {state}")
		#player_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
		player_llm = LLM(model="bedrock/meta.llama3-8b-instruct-v1:0", temperature=0.1)
		player_crew = PlayerCrew("llama3-8b-instruct", player_llm)
  
		pr = player_crew.crew.kickoff(inputs={"round_history": state["round_history"]}).pydantic.model_dump()
		print("player 2: ", pr)
		state["current_round_state"]["players_moves"].append(pr)

	def Doraemon(self, state: GameState) -> GameState:
		pr = PlayersMove(
			player_name="Doraemon",
			move="Rock" # Doraemen can only play rock :)
		)
		state["current_round_state"]["players_moves"].append(pr)

	# @traceable 
	# def judge_llm(self, state: GameState) -> GameState:
	# 	print(f"judge input state: {state}")
	# 	judge_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
	# 	judge_crew = JudgeCrew(judge_llm)
	# 	jr = judge_crew.crew.kickoff(inputs={"players_moves": state["current_round_state"]}).pydantic.model_dump()

	# 	round_number = state["current_round_number"]
	# 	state["current_round_state"]["judge_result"] = jr

	# 	# Add the current round state to the round history
	# 	state["round_history"][round_number] = state["current_round_state"]
 
	def judge(self, state: GameState) -> GameState:
		print(f"judge input state: {state}")
		
		# Get the moves from current round state
		players_moves: List[PlayersMove] = state["current_round_state"]["players_moves"]
		
		if len(players_moves) != 2:
			raise ValueError("Rock-Paper-Scissors requires exactly 2 players")
		
		# Correctly access PlayersMove TypedDict fields
		player1_name = players_moves[0]["player_name"]
		player1_move = players_moves[0]["move"].lower()
		player2_name = players_moves[1]["player_name"]
		player2_move = players_moves[1]["move"].lower()
		
		# Define winning combinations (key beats value)
		rules = {
			"rock": "scissors",
			"scissors": "paper",
			"paper": "rock"
		}
		
		# Determine winner
		jr: JudgeResult = {"winner": ""}  # Initialize with empty string
		
		if player1_move == player2_move:
			jr["winner"] = "tie"
		elif rules[player1_move] == player2_move:
			jr["winner"] = player1_name
		else:
			jr["winner"] = player2_name
		
		# Update state with judge result
		round_number = str(state["current_round_number"])  # Convert to string for dict key
		state["current_round_state"]["judge_result"] = jr
		
		# Add the current round state to the round history
		state["round_history"][round_number] = state["current_round_state"]

	def check_if_need_more_round(self, state):
		print(f"condition check input state: {state}")
		if state["current_round_number"] < 20:
			print("## need more round")
			return "continue"
		else:
			print("## max round reached")
			return "end"

	def announce_winner(self, state: GameState):
		history = json.dumps(state["round_history"], indent=2)
		print(f"announce winner input state: {state}")
		llm = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")

		prompt = f"""
			You are a helpful assistant. You are given the history of a game.
			Your tasks:
			1. Double check if there is any mistake of the judge result per round.
			2. You need to determine the winner of the game by reading all rounds history.
			3. Report any noticeable pattern of the players' moves.

			The history is as follows:
			{history}
			"""
		final_result = str(llm.invoke([HumanMessage(prompt)]).content).replace("\\n\\n", "\n\n")
  
		save_game_result(final_result, history)

