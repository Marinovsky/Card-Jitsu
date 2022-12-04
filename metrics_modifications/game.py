from QLearning import Game
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

gamma = 0.1

def Menu():
    usr_op = None
    while usr_op != 0:
        print('//-//-//-// Card-Jitsu Menu //-//-//-//')
        print('\nSelect an option to continue: ')
        print('1. Play game vs AI.')
        print('2. Get Strategy Metrics.')
        print('3. Get Random Metrics.')
        print('4. Train Ai Manual.')
        print('5. Train Ai Random.')
        print('0. Exit.')
        
        usr_op = int(input('\n Option selected: '))
        if usr_op == 1:
            Game(gamma)
        elif usr_op == 2:
            get_metrics(is_random = False, train = False, show_game = True)
        elif usr_op == 3:
            get_metrics(is_random = True, train = False, show_game = False)
        elif usr_op == 4:
            get_metrics(is_random = False, train = True, show_game = True)
        elif usr_op == 5:
            get_metrics(is_random = True, train = True, show_game = False, show_metrics = False)
        
        print('\n\n')

def get_metrics(is_random, train, show_game, show_metrics = True):

    history = {
        'Game': [],
        'Round': [],
        'AI': [],
        'Player': [],
        'Winner': [],
        'Game Winner': []
    }

    game = 0
    g = int(input('Numero de juegos a realizar: '))

    while game < g:
        winrecord , winner = Game(gamma, is_random, train, show_game)

        for round in range(len(winrecord)):
            history['Game'].append(game)
            history['Game Winner'].append(winner)
            history['Round'].append(round)
            history['AI'].append(winrecord[round]['AI'])
            history['Player'].append(winrecord[round]['Player'])
            history['Winner'].append(winrecord[round]['Winner'])

        game += 1

    if not show_metrics: return 0

    history = pd.DataFrame.from_dict(history)

    # Histograma de Rondas y juegos
    game_winrate = Counter(list(history['Game Winner']))
    game_winrate = pd.DataFrame.from_dict(game_winrate, orient='index', columns=['Games Won'])
    game_winrate.plot(kind='pie', y='Games Won', autopct='%1.0f%%', explode=(0.01, 0.01), startangle=20)
    plt.title('Frecuency of Games Won')
    plt.ylabel('')
    plt.show()
    
    # Diagrama de Pie de rondas ganadas

    round_winrate = Counter(list(history['Winner']))
    round_winrate = pd.DataFrame.from_dict(round_winrate, orient='index', columns=['Rounds Won'])
    round_winrate.plot(kind='pie', y='Rounds Won', autopct='%1.0f%%', explode=(0.01, 0.01, 0.01), startangle=60)

    plt.title('Frecuency of Rounds Won and Tied')
    plt.ylabel('')
    plt.show()

    # Histograma de cartas
    ai_cardrate = Counter(list(history['AI']))
    ai_cardrate = pd.DataFrame.from_dict(ai_cardrate, orient='index', columns=['AI Cards'])

    player_cardrate = Counter(list(history['Player']))
    player_cardrate = pd.DataFrame.from_dict(player_cardrate, orient='index', columns=['Player Cards'])
    
    hist_cardrate = ai_cardrate.merge(player_cardrate, how='outer', left_index=True, right_index=True).fillna(0)
    hist_cardrate.plot(kind = 'bar')

    plt.title('Frecuency of Cards Used')
    plt.show()

Menu()