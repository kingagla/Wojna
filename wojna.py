import numpy as np

# # define strength of cards
strength = {f'{i}': i for i in range(1, 11)}
strength['Walet'] = 11
strength['Dama'] = 12
strength['Król'] = 13
strength['As'] = 14


# create and mix cards based on given colors and numbers
def mix_cards(colors, numbers):
    # Create all pack
    allCards = []
    for col in colors:
        for num in numbers:
            allCards.append(num + ' ' + col)

    # shuffled cards
    np.random.shuffle(allCards)
    return allCards


def deal_cards(allCards, n_players):
    game = []
    for i in range(n_players):
        cards = []
        for j in range(len(allCards)):
            if j % n_players == i:
                cards.append(allCards[j])
        game.append(cards)
    return game


# remove player from game
def remove_player(game, players):
    # if player has no more cards is removed from game
    players_to_remove = []
    for card, player in zip(game, players):
        if card == []:
            players_to_remove.append(player)
    for item in players_to_remove:
        players.remove(item)
        game.remove([])
    return game, players


# function which give back cards to owners (used after war ended with dead-heat)
def cards_come_back(game, players, cards_to_take):
    n = len(players)
    for i in range(n):
        for j in range(len(cards_to_take)):
            if j % n == i:
                game[i].append(cards_to_take[j])
    return game


# one round
def one_round(game, players, war):
    """
    :param game: list containing lists of cards for each player
    :param players: list of players - length must be the same as length of game
    :param war: bool - True if current round is the war
    :return: winner, cards which got winner, players, game
    """
    # cards to win
    cards_to_take = []
    round_ = []
    # print players and their cards
    for card, player in zip(game, players):
        print(player, card)

    if war:
        # if round is the war, first card doesn't matter so it goes strictly to cards to win
        for card, player in zip(game, players):
            cards_to_take.append(card[0])
            card.pop(0)
        # if one of players had only one card, remove him from game
        game2, players2 = remove_player(game.copy(), players.copy())

        # if all players were removed, then it is dead-heat
        if len(players2) == 0:
            game = cards_come_back(game, players, cards_to_take)
            return None, cards_to_take, players, game
        # update game and players to state after removing players
        game = game2
        players = players2

    # if only one player stayed, it's winner
    if len(players) == 1:
        return 0, cards_to_take, players, game

    else:
        # choose first card of each player and remove it from cards
        for card, player in zip(game, players):
            round_.append(card[0])
            card.pop(0)
        # scores for cards
        scores = list(map(lambda x: strength[x.split()[0]], round_))
        scores = np.array(scores)
        # maximum score
        max_val = np.max(scores)
        # add cards to cards for winner
        cards_to_take += round_

        # if there is only one max score, we have winner! Otherwise we have war
        if np.sum(scores == max_val) == 1:
            winner = np.argmax(scores)
        else:
            print('wojna')

            # choose players for war and their cards
            players_in_war = [i for i in range(len(scores)) if scores[i] == max_val]
            players_for_war = [players[i] for i in players_in_war]
            print('w wojnie biorą udział gracze', players_for_war)
            game_for_war = [game[i] for i in players_in_war]

            # if any players for war has no more cards, remove him from war
            if [] in game_for_war:
                game_for_war2, players_for_war2 = remove_player(game_for_war, players_for_war)
                # if there is no more players then it is dead-heat, otherwise update players for war and go into war
                if players_for_war2 == []:
                    print('remis - karty wracają do właścicieli')
                    game = cards_come_back(game, players, cards_to_take)
                    return None, [], players, game
                else:
                    game_for_war, players_for_war = game_for_war2, players_for_war2
            winner, cards_to_take_after_war, players_for_war, game_for_war = one_round(
                game_for_war,
                players_for_war,
                war=True)

            # if winer after war is None, it is dead-heat
            if winner is None:
                game = cards_come_back(game, players, cards_to_take)
                return None, [], players, game

            winner = players_in_war[winner]
            cards_to_take += cards_to_take_after_war

        # give cards to winner
        if not war:
            print('zwycięzca to', players[winner])
            print('wygrał', cards_to_take)
            game[winner] += cards_to_take

        # check if there is player with no more cards and remove him/her
        if [] in game:
            game, players = remove_player(game, players)
        return winner, cards_to_take, players, game


if __name__ == '__main__':
    # how many round with no winner to stop game
    n = 10000
    # how many times repeat that
    m = 1
    end = 0
    # min no. of players
    min_players = 2
    # max no. of players
    max_players = 17
    # number of players
    n_players = int(input('Podaj liczbę graczy: '))
    while (n_players < min_players) or (n_players > max_players):
        n_players = int(input(f'Podałeś złą liczbę. Liczba graczy musi być pomiędzy {min_players} a {max_players}: '))
    for j in range(m):
        # define colors and numbers in cards, create and mix them
        colors = ['Kier', 'Karo', 'Trefl', 'Pik']
        numbers = [str(i) for i in range(2, 11)] + ['Walet', 'Dama', 'Król', 'As']
        allCards = mix_cards(colors, numbers)

        # Names of players
        players = [f'Gracz {i + 1}' for i in range(n_players)]

        # dealing cards
        game = deal_cards(allCards, n_players)

        # one game go on till someone win or end if after n rounds there is no winner
        i = 0
        while len(players) > 1 and i < n:
            i += 1

            print('liczba graczy to', len(players))
            winner, cards_to_take, players, game = one_round(game, players, war=False)

        if i == n:
            print('nie skonczyli')
        else:
            print('skonczyli')
            end += 1

    print('Grę skończyli', end, 'razy na', m)
