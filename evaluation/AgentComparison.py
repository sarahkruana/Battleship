import matplotlib.pyplot as plt

from model.Board import Board
from model.Ship import createShips
from model.MonteCarloAgent import MonteCarloAgent
from evaluation.RandomAgent import RandomAgent
from model.AIPlayer import AIPlayer

class AgentComparison:
    
    '''
    Contructor to run sims to compare the Monte Carlo agent to just a standard randomized agent
    To make it standardized the size of the board will be 10.
    '''
    def __init__(eval):
        pass


    '''
    Simulates one single game from start to finish. Both agents will randomly place fleet and take
    turns attacking until one is the winner. Returns (dict) with the # of shots taken and the hit rate
    @param agent represents the agent being tested
    '''
    def runSingleGame(eval, agent):
        board = eval.buildBoard()
        shots = 0
        hits = 0

        while not board.allSunk():
            unsunk = [ship for ship in board.ships if not ship.isSunk()]
            row, col = agent.chooseAttack(board, unsunk)
            
            result = board.attacked(row, col)
            shots += 1
            if result == "hit":
                hits += 1
            if result == "sunk":
                hits += 1

        return {
            "shots": shots,
            "hitRate": hits / shots
        }
    

    '''
    Runs many games to test the agent and returns avg shots/hit rate. Retruns (dict) 
    represnting avg shots/hit rate, min/max shots, all shot rates, and all hit rates
    @param agent represents the agent being tested
    @param numGames (int) represents how many games that get played
    '''
    def runTrials(eval, agent, numGames = 500):
        allShots = []
        allHitRates = []

        for _ in range (numGames):
            result = eval.runSingleGame(agent)
            allShots.append(result["shots"])
            allHitRates.append(result["hitRate"])

        avgShots = sum(allShots) / len(allShots)
        avgHitRate = sum(allHitRates) / len(allHitRates)

        return {
            "avgShots": avgShots,
            "avgHitRate": avgHitRate,
            "minShots": min(allShots),
            "maxShots": max(allShots),
            "allShots": allShots,
            "allHitRates": allHitRates
        }
    
    '''
    Builds a board of the given size with randomly placed ships. Returns (board)
    with all the ships placed
    '''
    def buildBoard(eval):
        player = AIPlayer("agent", 10)
        player.placeShipsRand()
        
        return player.board
