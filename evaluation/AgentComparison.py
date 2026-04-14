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
            row, col = agent.chooseAttack(board,unsunk)
            
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
    def runTrials(eval, agent, numGames):
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


    '''
    Runs all of the trials and displays/saves the three graphs
    '''
    def showResults(eval):
        monte = MonteCarloAgent()
        rand = RandomAgent()

        monteResults = eval.runTrials(monte, 500)
        randResults = eval.runTrials(rand, 500)

        eval.showShotResults(monteResults, randResults)
        eval.showAvgs(monteResults, randResults)
        eval.showShotsPerGame(monteResults, randResults, 500)

    
    '''
    Shows a histogram of the # of shots to win for both agents
    @param monteResults (dict) represents the results from the Monte Carlo trials
    @param randResults (dict) represent the results from the Randome trials
    '''
    def showShotResults(eval, monteResults, randResults):
        
        plt.figure()
        plt.hist(monteResults["allShots"], bins=20, alpha=0.6, label="Monte Carlo", color="blue")
        plt.hist(randResults["allShots"], bins=20, alpha=0.6, label="Random", color="red")
        
        plt.title("Number of Shots to Win")
        plt.xlabel("Shots")
        plt.ylabel("Games")
        plt.legend()
        
        plt.savefig("shotResults.png")
        plt.show()

    '''
    Shows a bar chart for both the avg shots and the avg hit rate for both agents
    @param monteResults (dict) represents the results from the Monte Carlo trials
    @param randResults (dict) represent the results from the Randome trials
    '''
    def showAvgs(eval, monteResults, randResults):
        agents = ["Monte Carlo", "Random"]

        plt.figure()
        plt.bar(agents, [monteResults["avgShots"], randResults["avgShots"]], 
                color=["blue", "red"], alpha=0.6)
        
        plt.title("Avg Shots to Win")
        plt.ylabel("Shots")
        plt.savefig("avgShots.png")
        plt.show()

        plt.figure()
        plt.bar(agents, [monteResults["avgHitRate"] * 100, randResults["avgHitRate"] * 100], 
                color=["blue", "red"], alpha=0.6)
        plt.title("Avg Hit Rate")
        plt.ylabel("Hit Rate (%)")
        plt.savefig("avgHitRate.png")
        plt.show()

    '''
    Shows a line graph that represnts the shots per game over time for both agents
    @param monteResults (dict) represents the results from the Monte Carlo trials
    @param randResults (dict) represent the results from the Randome trials
    @param num (int) represents how many games were played
    '''
    def showShotsPerGame(eval, monteResults, randResults, num):
        numGames = list(range(1, num + 1))

        plt.figure()
        plt.plot(numGames, monteResults["allShots"], alpha=0.5, label="Monte Carlo", color="blue")
        plt.plot(numGames, randResults["allShots"], alpha=0.5, label="Random", color="red")
        
        plt.title("Shots Per Game")
        plt.xlabel("Game")
        plt.ylabel("Shots")
        plt.legend()
        plt.savefig("shotsPerGame")
        plt.show()
    