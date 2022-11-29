import csv

# Create Q-Table
def CreateQtable():
    with open("Qtable.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for i in range(59048):
            writer.writerow([0]*9)

cards = ["F1", "A1", "N1", "F2", "A2", "N2", "F3", "A3", "N3"]

# Read Q-Table
def ReadQTable():
    qTable = []
    with open("Qtable.csv") as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            new_row = [int(x) for x in row]
            qTable.append(new_row)
    return qTable

# Save Q-Table
def SaveQtable(qTable):
    with open("Qtable.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for i in range(59048):
            writer.writerow(qTable[i])

# States are represented as a heap
def TransitionModel(s, a, a_prime):
    ia_card = cards[a]
    player_card = cards[a_prime]

    # Fire
    if ia_card[0] == "F" and player_card[0] == "A":
        return 3*s + 3
    elif ia_card[0] == "F" and player_card[0] == "N":
        return 3*s + 1
    elif ia_card[0] == "F" and player_card[0] == "F":
        if int(ia_card[1]) > int(player_card[1]):
            return 3*s + 1
        elif int(ia_card[1]) < int(player_card[1]):
            return 3*s + 3
        else:
            return 3*s + 2

    # Water
    if ia_card[0] == "A" and player_card[0] == "F":
        return 3*s + 1
    elif ia_card[0] == "A" and player_card[0] == "N":
        return 3*s + 3
    elif ia_card[0] == "A" and player_card[0] == "A":
        if int(ia_card[1]) > int(player_card[1]):
            return 3*s + 1
        elif int(ia_card[1]) < int(player_card[1]):
            return 3*s + 3
        else:
            return 3*s + 2
    
    # Snow
    if ia_card[0] == "N" and player_card[0] == "F":
        return 3*s + 3
    elif ia_card[0] == "N" and player_card[0] == "A":
        return 3*s + 1
    elif ia_card[0] == "N" and player_card[0] == "N":
        if int(ia_card[1]) > int(player_card[1]):
            return 3*s + 1
        elif int(ia_card[1]) < int(player_card[1]):
            return 3*s + 3
        else:
            return 3*s + 2

def Reward(s):
    if s % 3 == 1:
        return 1
    elif s % 3 == 2:
        return 0
    elif s % 3 == 0:
        return -1 

def QLearning():
    qTable = ReadQTable()
    s = 0
    for i in range(9):
        a = qTable[0].index(max(qTable[0]))
        a_prime = int(input("selecione su carta: "))
        s_prime = TransitionModel(s, a, a_prime)
        r = Reward(s_prime)
CreateQtable()

