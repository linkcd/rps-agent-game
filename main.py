from src.graph import WorkFlow
from src.state import GameState

app = WorkFlow().app
app.invoke(GameState())