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

import json
import random

cards = ["F1", "A1", "N1", "F2", "A2", "N2", "F3", "A3", "N3"]
random.seed(0)

# Read Q-Table
def ReadQTable():
    f = open("QTable.json")
    qTable = json.load(f)
    return qTable

# Save Q-Table
def SaveQtable(qTable):
    with open("QTable.json", "w") as outfile:
        json.dump(qTable, outfile)

def ComputeNewState(s, winner, card):
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
    if s == "ai":
        return 1
    elif s == "draw":
        return 0
    elif s == "player":
        return -1

def PrintGameStatus(s_prime):
    player = s_prime.split("$")[1]
    ai = s_prime.split("$")[0]
    print("=== MATCH ===")
    print("Player: " + player)
    print("AI: " + ai)
    print("=============")

def CheckIfWinner(s):
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

#epsilon-greedy method with epsilon = 0.01
def SelectAction(list):
    n = random.randint(1, 100)
    if n != 1:
        return list.index(max(list))
    else:
        k = random.randint(0,8)
        return k

def QLearning(gamma):
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

gamma = 0.4
QLearning(gamma)

