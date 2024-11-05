from crewai import Agent, LLM
from textwrap import dedent



class AgentFactory():
	#llm=LLM(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0", temperature=0.1), 
	def create_player(self, player_name, llm):
		return Agent(
			llm=llm,
			role=f'Player {player_name}',
			goal='Play rock paper scissors games against other players to win',
			backstory=dedent("""\
				You are a professional rock paper scissors player. You analysis other players pattern,
    			and find a best strategy to win base on your best prediction of others.
				You listen to the game managers order.
				The previous players moves are in {round_history}, use it wisely.
       			"""),
			verbose=True,
			allow_delegation=False
		)

	def create_judge(self, llm):
		return Agent(
			llm=llm, 
			role='Judge',
			goal='Based on the {players_moves}, decide the winner of the game',
			backstory=dedent("""\
				You are a good judge. You study the game rules carefully, and before you make the decision, you always double check to make sure that your result is following the game rules.
       			"""),
			verbose=True,
			allow_delegation=False
   		)
  

	# def agent_manager(self):
	# 	return Agent(
	# 		llm=self.llm,
	# 		role='Game manager',
	# 		goal='You the game manager to ensure the rock paper scissors game goes smoothly by talking to players and judge',
	# 		backstory=dedent("""\
	# 			You are a good game manager. You make sure all players participate the game, then let the judge to decide who is the winner. You never play the game or judge the game.
	# 			You make sure that you pass all info of the moves to the judge
    #    			"""),
	# 		verbose=True,
	# 		allow_delegation=True
   	# 	)
		