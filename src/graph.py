from langgraph.graph import StateGraph, START, END

from .nodes import Nodes
from .state import GameState

class WorkFlow():
	def __init__(self):
		nodes = Nodes()
		workflow = StateGraph(GameState)

		workflow.add_node("run_game", nodes.run_game)
	
		workflow.set_entry_point("run_game")
		workflow.add_conditional_edges(
				"run_game",
				nodes.check_if_need_more_round, 
				{
					"continue": 'run_game',
					"end": END
				}
		)
		self.app = workflow.compile()