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

## License
This project is released under the MIT License.
