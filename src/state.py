from typing import Annotated, Dict, List, Literal #, TypedDict
from typing_extensions import TypedDict # Using typing_extensions.TypedDict on Python < 3.12 python

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
    max_round: int
    current_round_number: int
    current_round_state: RoundState
    round_history: Dict[str, RoundState]
