from typing import Annotated, TypedDict, Dict, List, Literal
import operator

class PlayersMove(TypedDict):
    player_name: str
    move: Literal["rock", "paper", "scissors"]

class JudgeResult(TypedDict):
    winner: str

class RoundState(TypedDict):
    round_number: int
    players_moves: List[PlayersMove]
    judge_result: JudgeResult

class GameState(TypedDict):
    current_round_number: int
    current_round_state: RoundState
    round_history: Dict[str, RoundState]
