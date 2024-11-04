from crewai import Crew, Process, LLM
from .agents import AgentFactory
from .tasks import GameTasks


class PlayerCrew():
	def __init__(self, player_name, llm):
		gameAgents = AgentFactory()
		self.player = gameAgents.create_player(player_name, llm)

		gameTasks = GameTasks()

		self.crew = Crew(
				agents=[self.player],
				tasks=[
					gameTasks.play_game(self.player),
				],
				verbose=False,
				# process=Process.sequential,
				# memory=True, #(by default it is using open ai so need api key for it)
				# embedder={
				# 	"provider": "aws_bedrock",
				# 	"config":{
				# 	"model": "amazon.titan-embed-text-v2:0",
				# 	"vector_dimension": 1024
				# 	}
				# }
			)
  
class JudgeCrew():
	def __init__(self, llm):
		gameAgents = AgentFactory()
		self.judge = gameAgents.create_judge(llm)
  
		gameTasks = GameTasks()
		self.crew = Crew(
			agents=[self.judge],
			tasks=[
				gameTasks.judge_game(self.judge),
			],
			verbose=False,
			# memory=True, #(by default it is using open ai so need api key for it)
			# embedder={
			# 	"provider": "aws_bedrock",
			# 	"config":{
			# 	"model": "amazon.titan-embed-text-v2:0",
			# 	"vector_dimension": 1024
			# 	}
			# }
		)
		
		