# Rock Paper Scissors (rps) Agent Game

## 1. Introduction
Have you ever wondered which AI model is the best Rock-Paper-Scissors player? This project will help you find out!

This project demonstrates how to use the [CrewAI](https://www.crewai.com/) and [LangGraph](https://www.langchain.com/langgraph) to build multi-agent systems. It runs fully automated Rock-Paper-Scissors games, where multiple AI agents play against each other. Each AI agent is powered by a different Large Language Model (LLM), allowing you to run games such as OpenAI vs. Meta Llama, or Llama vs. Claude. There are also AI judge agents to compare player agents’ moves and decide the winner.

### Features
- **Multi-Agent System**: Simulate games with multiple AI agents.
- **Diverse AI Models**: Compare different LLMs like OpenAI, Meta Llama, and Claude.
- **Automated Judging**: AI judge agents determine the winner of each round.

## 2. Workflow
It runs multiple rounds of Rock-Paper-Scissors games. 
- In each round, two player agents make their moves independently and in parallel. They have access to the history of previous rounds, allowing them to analyze patterns and decide on the best move.
- After the players make their moves, a judge agent determines the winner of the round.
- The system checks if the criteria for determining the final winner have been met (e.g., reaching the specified number of rounds, or a player winning 3 out of 5 rounds).
	- **Criteria Not Met**: If the criteria are not met, another round begins.
	- **If the criteria are met**: The final winner is announced, and a post-game analysis is performed.

![Workflow graph](doc/graph.png "Graph")

### 2.1. Building blocks
- CrewAI: For defining the agents and tasks
- LangGraph: For defining the workflow 
- Amazon Bedrock: For LLM hosting
- LangSmith: For debugging and tracking

## 3. Some game results
### Game 1: Doreamen vs Llama3 8B Instruct (without memory) 
- Doreamen is a dummy agent who can only play Rocks :)

   ![Doreamen](/doc/game_history/Doraemon.png "")

- AI Agent is based on Llama3 8B Instruct, but has no memory (it means it cannot learn from previous rounds)

![doraemon vs llama3-8b-instruct-without-memory](/doc/game_history/doraemon%20vs%20llama3-8b-instruct-without-memory.png "")

**Game 1 result:**
> The winner of the game is Doraemon. Out of 20 rounds:
>    - Doraemon won 16 rounds
>    - llama3-8b-instruct won 1 round
>    - 3 rounds were ties

> Overall game pattern:
> - The game was heavily dominated by Doraemon due to its consistent "Rock" strategy, which was highly effective against llama3-8b-instruct's preference for "Scissors"
> - llama3-8b-instruct seemed to struggle to adapt to Doraemon's strategy, only managing to win once when it played "Paper" in round 12
> - The game demonstrates the importance of adapting strategies in Rock-Paper-Scissors, as llama3-8b-instruct's failure to do so resulted in a significant loss

### Game 2: Doreamen vs Llama3 8B Instruct (with memory) 
Now we enable the AI agent to have access of previous round history, and that significantly improved its performance.

![doraemon vs llama3-8b-instruct-with-memory](/doc/game_history/doraemon%20vs%20llama3-8b-instruct.png "")

**Game 2 results:**
> The winner of the game is llama3-8b-instruct. Out of 20 rounds:
>   - llama3-8b-instruct won 18 rounds
>   - Doraemon won 1 round
>   - There was 1 tie

> Overall pattern:
>   - After losing in round 2, llama3-8b-instruct seems to have recognized Doraemon's pattern of always playing Rock and adjusted its strategy to consistently play Paper, which beats Rock.
>   - This adaptive strategy allowed llama3-8b-instruct to win 17 consecutive rounds from round 3 to round 20.

This is the same with claude 3 sonnet based agent
- [Doraemon vs claude-3-sonnet without memory](/doc/game_history/doraemon%20vs%20claude-3-sonnet-without-memory.png)

- [Doraemon vs claude-3-sonnet with memory](/doc/game_history/doraemon%20vs%20claude-3-sonnet.png)

### Game 3: Llama3 8B Instruct vs Claude Sonnet 3
Both AI agents have identical prompt and memory capacity. This is purely comparing different models "personality". 

**Game 3 results:**

Within 20 rounds, Llama3 8B Instruct initially performed better. However, as more rounds were played, the Claude Sonnet 3 agent adapted its strategy to counter Llama3-8b-instruct’s preference for Paper, ultimately leading to its decisive victory in the game.

- [20 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%2020%20rounds.txt) : llama3-8b-instruct **8:5** claude-3-sonnet, with 6 ties
![20 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%2020%20rounds.png)

- [50 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%2050%20rounds.txt) : llama3-8b-instruct **16:20** claude-3-sonnet, with 14 ties
![50 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%2050%20rounds.png)

- [100 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%20100%20rounds.txt) : llama3-8b-instruct **29:55** claude-3-sonnet, with 16 ties
![100 rounds](/doc/game_history/llama3-8b-instruct%20vs%20claude-3-sonnet%20100%20rounds.png)

> Noticeable Patterns for the game with 100 rounds:
> 
> a) llama3-8b-instruct:
> - Shows a strong preference for Paper, playing it in 64 out of 100 rounds (64%).
> - Rarely plays Scissors, only 11 times throughout the game.
> - Tends to stick with Paper for long streaks, especially towards the end of the game.
> 
> b) claude-3-sonnet:
> - Demonstrates a clear preference for Scissors, playing it in 58 out of 100 rounds (58%).
> - Adapts its strategy over time, increasing its use of Scissors as it recognizes llama3-8b-instruct's preference for Paper.
> - Plays Rock less frequently, only 19 times throughout the game.
>
> c) Game Progression:
> - The game starts with more varied plays from both players.
> - As the game progresses, it becomes more predictable with llama3-8b-instruct primarily playing Paper and claude-3-sonnet countering with Scissors.
> - The last 30 rounds show an almost complete lock-in of this Paper vs Scissors pattern, heavily favoring claude-3-sonnet.

> In conclusion, claude-3-sonnet appears to have adapted its strategy to counter llama3-8b-instruct's preference for Paper, leading to its decisive victory in the game.


## 5. Run the project
```bash
python -m venv .venv
pip install -r requirements.txt 

# create .env file has correct API keys. the example file is .sample.env

#The execution result will be be 2 files in game_outputs folder
# - 1. game_result_{timestamp}.txt - post game analysis and complete round history: 
# - 2. game_result_{timestamp}.png - game result visualization
python main.py 
```

## License
This project is released under the MIT License.
