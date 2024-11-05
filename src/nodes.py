from .state import PlayersMove, JudgeResult, RoundState, GameState
from crewai import LLM
from .crew.crew import PlayerCrew, JudgeCrew
from langsmith import traceable

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
		player_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
		#player_llm = LLM(model="bedrock/mistral.mistral-7b-instruct-v0:2", temperature=0.1)
		player_crew = PlayerCrew("claude-3-haiku", player_llm)
  
		pr = player_crew.crew.kickoff(inputs={"round_history": state["round_history"]}).pydantic.model_dump()
		print("player 2: ", pr)
		state["current_round_state"]["players_moves"].append(pr)

	@traceable 
	def judge(self, state: GameState) -> GameState:
		print(f"judge input state: {state}")
		judge_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
		judge_crew = JudgeCrew(judge_llm)
		jr = judge_crew.crew.kickoff(inputs={"players_moves": state["current_round_state"]}).pydantic.model_dump()

		round_number = state["current_round_number"]
		state["current_round_state"]["judge_result"] = jr

		# Add the current round state to the round history
		state["round_history"][round_number] = state["current_round_state"]

	def check_if_need_more_round(self, state):
		print(f"condition check input state: {state}")
		if state["current_round_number"] > 10:
			print("## max round reached")
			return "end"
		else:
			print("## need more round")
		return "continue"

	def announce_winner(self, state: GameState):
		print("!!!Winner!!!")
		print(str(state))

