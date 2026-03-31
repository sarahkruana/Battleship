# Battleship Project
# Sarah Ruana and Shweta Pattanaik

# Overview
Battleship is a game with two agents. Each agent is able to see their board along with a model of the opposing agents board. At the start of the game, each player places a set of ships onto their board (a grid based system) without revealing the locations. Then, at the start of each turn, each player takes turns guessing the coordinates of the opposing player's ships. The end goal is to find, hit and sink the opponents ships.

# Implementation
Our game will have a model, a controller, and a view. Each agent (ai or human) will have their own controller which will handle inputs from the view and pass it through to the model. After each input gets passed to the controller, the view will refresh and switch players. 

Model:
The model will handle the game mechanics.
- starting the game
- ending the game
- placing the target (and determining validity)
- determining the winner
- keeping score
- etc (will be updated as we continue making the game)
to note:
- the red player will start first, you cannot place any ships after the game has been started, you cannot attack if the game has not been started yet

Controller:
The controller will handle user input and pass it to the model
- determining validity of inputs
- passing inputs into the model
- refresshing the view
- etc (will be updated as we continue making the game)

View:
The textual view will represent both the human players board along with a model of the opposing players view
- output of human players board
- output of blank model of the ai players board
- etc (will be updated as we continue making the game)

# File Path Structure
+- Battleship/

| +- main/

| +- controller/

| +- model/

| +- view/

| +- test/

|| +- controller/

|| +- model/

|| +- view/