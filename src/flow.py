
import warnings
warnings.filterwarnings('ignore')

import asyncio
import json

from crewai.flow.flow import Flow, listen, start, router, and_
from crewai import LLM
from .crew.crew import PlayerCrew, JudgeCrew
from .state import GameState


class GameFlow(Flow[GameState]):
    
    # Todo: need find a way to pass the initial state to a flow. the code in below does not work as i hoped
    def __init__(self, initial_state) -> None:
        super().__init__()
        self.initial_state = initial_state
        print(f"MEMEMEMEM: {self.initial_state}")
        print(f"MEMdddddddEMEMEM: {self.state}")
    
    def store_player_result(self, game_number: int, player_result: dict):
        """
        Store a player's result in self.state.game_results dictionary.
        
        Args:
            game_number (int): The game number to store the result for
            player_result (dict): A dictionary containing player_name and move
                {
                    "player_name": str,
                    "move": str
                }
        """
        # If game number doesn't exist, create new game result
        if game_number not in self.state.game_results:
            self.state.game_results[game_number] = {
                "game_number": game_number,
                "player_results": []
            }
        
        # Add player result to the player_results array
        self.state.game_results[game_number]["player_results"].append(player_result)

    def store_judge_result(self, game_number: int, judge_result: dict):
        if game_number not in self.state.game_results:
            raise ValueError(f"Game number {game_number} does not exist in game_results")

        self.state.game_results[game_number]["judge_result"] = judge_result

    @start()
    def start_game(self):
        print(f"starting the game..., the current game number is {self.state.game_number}")
        
    @listen(start_game)
    def player1(self):
        player_llm = LLM(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0", temperature=0.1)
        player_crew = PlayerCrew("claude-3-sonnet", player_llm)
        
        result = player_crew.crew.kickoff().pydantic.model_dump()
        print("player 1: ", result)
        
        self.store_player_result(self.state.game_number, result)
        
    @listen(start_game)    
    def player2(self):
        
        player_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
        #player_llm = LLM(model="bedrock/mistral.mistral-7b-instruct-v0:2", temperature=0.1)
        
        player_crew = PlayerCrew("claude-3-haiku", player_llm)
        
        result = player_crew.crew.kickoff().pydantic.model_dump()
        print("player 2: ", result)   

        self.store_player_result(self.state.game_number, result)

    # have to wait for all 3 methods to finish before we can call the judge
    # if only wait for play1 and play2 but not the start_game, this judge_game method will NOT be called
    @listen(and_(start_game, player1, player2))
    def judge_game(self):
        game_number = self.state.game_number
        player_results = self.state.game_results[game_number]["player_results"]
                
        judge_llm = LLM(model="bedrock/anthropic.claude-3-haiku-20240307-v1:0", temperature=0.1)
        judge_crew = JudgeCrew(judge_llm)
        judge_result = judge_crew.crew.kickoff(inputs={"player_results": player_results}).pydantic.model_dump()

        self.store_judge_result(game_number, judge_result)

        # print("JUDGE DONE")
        # print(json.dumps(self.state.game_results[game_number]))
        
        # print("ALL HISTORY")
        # print(json.dumps(self.state.game_results))

    # @router(judge_game)
    # def game_next_step(self):
    #     if self.state.game_number <= 3:
    #         self.state.game_number += 1
    #         return "more_game"
    #     else:
    #         return "finish_game"
    
    # @listen("more_game")
    # def more_game(self):
    #     print("start a new round of game")
    #     #self.start_game()

    # @listen("finish_game")
    # def finish_all_games(self):
    #     print("ALL GAME FINISHED")
    #     print("ALL HISTORY")
    #     print(json.dumps(self.state.game_results))


# async def plot_flow():
#     """
#     Plot the flow.
#     """
#     flow = GameFlow()
#     flow.plot()

# def plot():
#     asyncio.run(plot_flow())

# async def run_flow():
#     """
#     Run the flow.
#     """
#     flow = GameFlow()
#     await flow.kickoff()

# def main():
#     asyncio.run(run_flow())

# if __name__ == "__main__":
#     # use plot to generate flow diagram html file
#     #plot()
    
#     main()

