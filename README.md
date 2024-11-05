# Rock Paper Scissors (rps) Agent Game

## Introduction
Have you ever wondered which AI model is the best Rock-Paper-Scissors player? This project will help you find out!

This project demonstrates how to use the [CrewAI](https://www.crewai.com/) and [LangGraph](https://www.langchain.com/langgraph) to build multi-agent systems. It runs fully automated Rock-Paper-Scissors games, where multiple AI agents play against each other. Each AI agent is powered by a different Large Language Model (LLM), allowing you to run games such as OpenAI vs. Meta Llama, or Llama vs. Claude. There are also AI judge agents to compare player agents’ moves and decide the winner.

### Features
- **Multi-Agent System**: Simulate games with multiple AI agents.
- **Diverse AI Models**: Compare different LLMs like OpenAI, Meta Llama, and Claude.
- **Automated Judging**: AI judge agents determine the winner of each round.

## Workflow
It runs multiple rounds of Rock-Paper-Scissors games. 
- In each round, two player agents make their moves independently and in parallel. They have access to the history of previous rounds, allowing them to analyze patterns and decide on the best move.
- After the players make their moves, a judge agent determines the winner of the round.
- The system checks if the criteria for determining the final winner have been met (e.g., reaching the specified number of rounds, or a player winning 3 out of 5 rounds).
	- **Criteria Not Met**: If the criteria are not met, another round begins.
	- **If the criteria are met**: The final winner is announced, and a post-game analysis is performed.

![Workflow graph](doc/graph.png "Graph")

## Building blocks
- CrewAI: For defining the agents and tasks
- LangGraph: For defining the workflow 
- Amazon Bedrock: For LLM hosting
- LangSmith: For debugging and tracking

## Run the project
```bash
python -m venv .venv
pip install -r requirements.txt  

python main.py
```

## A game between llama3-8b-instruct and claude-3-sonnet
The game round result can be found at here [doc/sample_state.json](doc/sample_state.json)

The final announcement and post-game analysis is like 
```
After reviewing the game history, here are my findings:

1. Judge Result Accuracy:
   There is one minor inconsistency in the judge's result terminology. In round 1, the result is listed as "tie" (lowercase), while in other tie rounds (2, 4, and 8), it's listed as "Tie" (capitalized). This doesn't affect the outcome but is worth noting for consistency.

   In round 10, the judge's result format is different from the rest, stating "Player 1, 'llama3-8b-instruct'" instead of just the player name. However, the winner is correctly identified.

2. Game Winner Determination:
   Based on the round-by-round results:
   - claude-3-sonnet won 5 rounds (3, 5, 6, 7, 9)
   - llama3-8b-instruct won 1 round (10)
   - 4 rounds were ties (1, 2, 4, 8)

   Therefore, the overall winner of the game is claude-3-sonnet.

3. Noticeable Patterns:
   a. llama3-8b-instruct:
      - Started with Rock for the first three rounds
      - Showed a preference for Paper, playing it 4 times out of 10 rounds
      - Only played Scissors twice, in rounds 6 and 10

   b. claude-3-sonnet:
      - Showed a strong preference for Paper, playing it 5 times out of 10 rounds
      - Played Rock only twice, in the first two rounds
      - Seemed to adapt its strategy, not repeating the same move more than twice in a row

   c. General Observations:
      - The game had a high number of ties (4 out of 10 rounds)
      - claude-3-sonnet seemed to have a more varied and adaptive strategy compared to llama3-8b-instruct
      - llama3-8b-instruct's moves were more predictable, which might have contributed to its losses

In conclusion, claude-3-sonnet demonstrated a superior strategy and adaptability, leading to its victory in the game.
```

## License
This project is released under the MIT License.
