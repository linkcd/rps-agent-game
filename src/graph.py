from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from .nodes import Nodes
from .state import GameState


class GraphBuilder():
    
	def __init__(self):
          
		nodes = Nodes()
     
		graph_builder = StateGraph(GameState)

		graph_builder.add_node("start_new_round", nodes.start_new_round)
		graph_builder.add_node("player1", nodes.player1)
		graph_builder.add_node("player2", nodes.player2)
		graph_builder.add_node("judge", nodes.judge)
		graph_builder.add_node("announce_winner", nodes.announce_winner)

		graph_builder.add_edge(START, "start_new_round")
		graph_builder.add_edge("start_new_round", "player1")
		graph_builder.add_edge("start_new_round", "player2")
  
		graph_builder.add_edge("player1", "judge")
		graph_builder.add_edge("player2", "judge")
  
		graph_builder.add_conditional_edges(
				"judge",
				nodes.check_if_need_more_round, 
				{
					"continue": 'start_new_round',
					"end": "announce_winner"
				}
		)
  
		graph_builder.add_edge("announce_winner", END)
		self.app = graph_builder.compile()
  
		