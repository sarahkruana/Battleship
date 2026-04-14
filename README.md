# Battleship Project
# Sarah Ruana and Shweta Pattanaik


# Overview
In this Battleship, one user is able to play against a trained Monte Carlo ai agent. The user at each turn will be able to see both their and the agent's board, as well as the status of both their and the agents fleet. At the start of the game, the user will pick their name, the size of the board (5-10), and place their ships onto the board. Then, at the start of each turn, each player takes turns guessing the coordinates of the opposing player's ships. The end goal is to find, hit and sink the opponents ships.

# Implementation
Our game is based on a model-view-controller structure where the the controller will send updates from either the user or the ai agent to the model, then the model will update the game state and send it back to the controller, and then the controller will update the view. This repeats until the game is over. 

# Quick Notes:
- to run the game type "python Main.py" into the terminal
- to run the comparison type "python -m evaluation.runComparison" (warning: it will take a really long time)
- to quit the game type "quit" (cannot type 1,quit it needs to be its own token)
- enter coordinates in the system as row,col row,col (eg: 1,1 1,2 1,3)

# Structure:
Model:
The model will handle the game mechanics.
- starting the game
- ending the game
- placing the target (and determining validity)
- determining the winner
- keeping score
- etc

to note:
- the red player will start first, you cannot place any ships after the game has been started, you cannot attack if the game has not been started yet

Controller:
The controller will handle user input and pass it to the model
- determining validity of inputs
- passing inputs into the model
- refresshing the view
- etc 

View:
The textual view will represent both the human players board along with a model of the opposing players view
- output of human players board
- output of model of the ai players board (hiding the ships)
- output of the state of the human players fleet
- output of the state of the ai agents fleet

Evaluation:
This is to test that the Monte Carlo agent actually outperforms a randomized simple agent
- agent that picks cells at random
- graph representing the average hit rate of both agents
- graph representing the average shots to win of both agents
- graph representing the number of shots to win for both agents
- graph representing the shots per game for both agents


# File Path Structure
+- Battleship/

| +- controller/

|  | +- __init__.py

|  | +- GameController.py

| +- evaluation/

|  | +- __init__.py

|  | +- AgentComparison.py

|  | +- RandomAgent.py

|  | +- runComparison.py

|  | +- avgHitRate.png

|  | +- avgShots.png

|  | +- shotResults.png

|  | +- shotsPerGame.png

| +- model/

|  | +- __init__.py

|  | +- AIPlayer.py
 
|  | +- BattleshipGame.py

|  | +- Board.py

|  | +- MonteCarloAgent.py

|  | +- Player.py

|  | +- Ship.py

| +- view/

|  | +- __init__.py

|  | +- TextualView.py

| +- test/

|  | +- controller/

|  |  | +- TestGameController.py

|  | +- evaluation/

|  |  | +- TestRandomAgent.py

|  | +- model/

|  |  | +- TestAIPlayer.py

|  |  | +- TestBoard.py

|  |  | +- TestGameModel.py

|  |  | +- TestMonteAgent.py

|  |  | +- TestPlayer.py

|  |  | +- TestShip.py

|  | +- view/

|  |  | +- TestGameView.py

| +- README.md

| +- Main.py