from pydantic import BaseModel

class GameState(BaseModel):
    game_number: int = 0
    game_results: dict = {}