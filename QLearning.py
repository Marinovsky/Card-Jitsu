# Card-Jitsu game is represented as a Markov Decision Process (MDP)

# States are represented as "[AI Elements]$[Player Elements]"
# where AI Elements is a string containing "F", "A", "N" meaning
# the elements cards of which the ai has won a round. I.E For
# the first round the game starts at state "$" because anyone has
# already won a round, then if ai selects a fire card (F) and the player a
# snow card (N) then the status will be  "F$". Now, if in the next round
# the player wons with a water card (A) the status is going to be "F$A".
# Finally, if the the ai wons again with any card, say snow, the status
# will be "FN$A", because for both, the ai and the player, the elements
# are stored in alphabetic order (this is made with function ComputeNewState())

# Actions are represented as a string list of possible cards to play

# Rewards are calculated by the function Reward()

# Transition model is implemented in the function TransitionModel()

import json
import random

# Card-Jitsu cards, actions the AI agent and the player can take
cards = ["F1", "A1", "N1", "F2", "A2", "N2", "F3", "A3", "N3"]

# Discounting factor for the AI agent
gamma = 0.4

# Seed to make the experiments reproducible
random.seed(0)

def ReadQTable():
    """
    Description
    -----------
    This funtion loads the Q-table from the .json file, saves it
    into a dictionary and return this dictionary
    """
    f = open("QTable.json")
    qTable = json.load(f)
    return qTable

# Save Q-Table
def SaveQtable(qTable):
    """
    Description
    -----------
    This function updates the file "QTable.json" with the given
    dictionary

    Parameters
    ----------
    qTable : Dictionary of string-(float list)
        The qtable obtained from the function QLearning()
    """
    with open("QTable.json", "w") as outfile:
        json.dump(qTable, outfile)

def ComputeNewState(s, winner, card):
    """
    Description
    -----------
    Given the last state, the winner of the current round, and
    the card with which the winner won the round it computer the
    next state

    Parameters
    ----------
    s : string
        The last state of the game
    winner : string
        "ai" if the AI agent won the round and "player" otherwise
    card : string
        "A" if the winner won with a water card. "F" if the winner
        won with a fire card. "N" if the winner won with a snow card.

    Returns
    -------
    string : The next state of the game based in the last state, the
    winner of the last round and the card with wich it won.
    """
    ai_wins = s.split("$")[0]
    player_wins = s.split("$")[1]

    if winner == "ai":
        temp = ai_wins + card
        new_ai_wins = ''.join(sorted(temp))
        return (new_ai_wins + "$" + player_wins)
    else:
        temp = player_wins + card
        new_player_wins = ''.join(sorted(temp))
        return (ai_wins + "$" + new_player_wins)

def TransitionModel(s, a, a_prime):
    """
    Description
    -----------
    Function representing the transition model of the Markov Decision
    Process (MDP) or the game (Card-Jitsu) logic. Based in the last state,
    the action took by the AI agent and the action took by the player it
    determined the next state.

    Parameters
    ----------
    s : string
        Last state of the MDP or game
    a : int
        Index of the card took by the AI agent, see cards dictionary
    a_prime : int
        Index of the card took by the player, see cards dictionary

    Returns
    -------
    string : New state of the MDP or game
    string : winner of the round, "ai" if the AI agent won and "player"
    otherwise.
    """
    ia_card = cards[a]
    player_card = cards[a_prime]

    # Fire
    if ia_card[0] == "F" and player_card[0] == "A":
        return ComputeNewState(s, "player", "A"), "player"
    elif ia_card[0] == "F" and player_card[0] == "N":
        return ComputeNewState(s, "ai", "F"), "ai"
    elif ia_card[0] == "F" and player_card[0] == "F":
        if int(ia_card[1]) > int(player_card[1]):
            return ComputeNewState(s, "ai", "F"), "ai"
        elif int(ia_card[1]) < int(player_card[1]):
            return ComputeNewState(s, "player", "F"), "player"
        else:
            return s, "draw"

    # Water
    if ia_card[0] == "A" and player_card[0] == "F":
        return ComputeNewState(s, "ai", "A"), "ai"
    elif ia_card[0] == "A" and player_card[0] == "N":
        return ComputeNewState(s, "player", "N"), "player"
    elif ia_card[0] == "A" and player_card[0] == "A":
        if int(ia_card[1]) > int(player_card[1]):
            return ComputeNewState(s, "ai", "A"), "ai"
        elif int(ia_card[1]) < int(player_card[1]):
            return ComputeNewState(s, "player", "A"), "player"
        else:
            return s, "draw"
    
    # Snow
    if ia_card[0] == "N" and player_card[0] == "F":
        return ComputeNewState(s, "player", "F"), "player"
    elif ia_card[0] == "N" and player_card[0] == "A":
        return ComputeNewState(s, "ai", "N"), "ai"
    elif ia_card[0] == "N" and player_card[0] == "N":
        if int(ia_card[1]) > int(player_card[1]):
            return ComputeNewState(s, "ai", "N"), "ai"
        elif int(ia_card[1]) < int(player_card[1]):
            return ComputeNewState(s, "player", "N"), "player"
        else:
            return s, "draw"

def Reward(s):
    """
    Description
    -----------
    Computes the reward for the AI agent based on the last round.

    Parameters
    ----------
    s : string
        Winner of the last round, "ai" if the AI agent won and
        "player" otherwise.
    
    Returns
    -------
    int : 1 if the AI agent won, -1 if the player won and 0 otherwise.
    """
    if s == "ai":
        return 1
    elif s == "draw":
        return 0
    elif s == "player":
        return -1

def PrintGameStatus(s_prime):
    """
    Description
    -----------
    Prints the game status the inform the player.

    Parameters
    ----------
    s_prime : string
        Current game state
    """
    player = s_prime.split("$")[1]
    ai = s_prime.split("$")[0]
    print("=== MATCH ===")
    print("Player: " + player)
    print("AI: " + ai)
    print("=============")

def CheckIfWinner(s):
    """
    Description
    -----------
    Function to check whether the AI agent or the player has alredy
    won the game.

    Parameters
    ----------
    s : string
        Current status of the MDP or game.
    
    Returns
    -------
    string/int : "ai" if the AI agent won the game, "player" if the player won
    the game and -1 if neither of them has already won the game
    """
    ai = s.split("$")[0]
    player = s.split("$")[1]

    if ("F" in ai) and ("A" in ai) and ("N" in ai):
        return "ai"
    
    if (ai.count("F") == 3) or (ai.count("A") == 3) or (ai.count("N") == 3):
        return "ai"
    
    if ("F" in player) and ("A" in player) and ("N" in player):
        return "player"
    
    if (player.count("F") == 3) or (player.count("A") == 3) or (player.count("N") == 3):
        return "player"
    
    return -1

def SelectAction(list):
    """
    Description
    -----------
    Function to select the next action of the AI agent using
    the epsilon-greedy method, with epsilon = 0.01.

    Parameters
    ----------
    list : list
        float list, where the index represent the Card-Jitsu cards
        and the value of them the Q-Value of them.
    
    Returns
    -------
    int : The action the AI agent took based on the epsilon-greedy method.

    """
    n = random.randint(1, 100)
    if n != 1:
        return list.index(max(list))
    else:
        k = random.randint(0,8)
        return k

def Game(gamma):
    """
    Description
    -----------
    Card-Jitsu game driver to play between a player and the 
    AI agent, represented by the Q-Table. This can also be 
    seen as the Markov Decision Process (MDP) of the Card-Jitsu
    game. This functions allows the user to play with the AI, teaching
    the AI agent how to play in the process.

    Parameters
    ----------
    gamma : float
        The discounting factor for the Q-Learning AI agent
    """
    qTable = ReadQTable()
    s = "$"
    alpha = 1
    k = 1
    match = []
    while (CheckIfWinner(s) == -1):
        print("Round " + str(k))
        alpha = 1/k
        a = SelectAction(qTable[s])
        a_prime = int(input("selecione su carta: "))
        print("AI card: " + cards[a])
        print("Your card: " + cards[a_prime])
        match.append([a, a_prime])
        s_prime, winner = TransitionModel(s, a, a_prime)
        r = Reward(winner)
        if r == 1:
            print("AI wins this round")
        elif r == 0:
            print("Draw")
        else:
            print("Player wins")
        
        if s_prime not in qTable:
            qTable[s_prime] = [0]*9
        
        qTable[s][a] += alpha*(r + gamma*(max(qTable[s_prime])) - qTable[s][a])
        #print("qTable["+str(s)+"]["+str(a)+"]: " + str(qTable[s][a]))
        #print("New state: " + str(s_prime))
        PrintGameStatus(s_prime)
        s = s_prime
        k += 1

    if CheckIfWinner(s) == "ai":
        print("AI wins!")
    else:
        print("Player wins!")
    
    SaveQtable(qTable)
    print(match)

# Start to play
Game(gamma)

