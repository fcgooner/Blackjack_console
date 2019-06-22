from Player_file import Gambler
from Player_file import Player
import random
import time


# shuffling the cards
def shuffling(cards):
    random.shuffle(cards)
    return cards


# delay for printouts
sleep_time = 0.6
# an original play deck to restore each round
origin_deck = ["Ah", "Ad", "Ac", "As",
               "Kh", "Kd", "Kc", "Ks",
               "Qh", "Qd", "Qc", "Qs",
               "Jh", "Jd", "Jc", "Js",
               "10h", "10d", "10c", "10s",
               "9h", "9d", "9c", "9s",
               "8h", "8d", "8c", "8s",
               "7h", "7d", "7c", "7s",
               "6h", "6d", "6c", "6s",
               "5h", "5d", "5c", "5s",
               "4h", "4d", "4c", "4s",
               "3h", "3d", "3c", "3s",
               "2h", "2d", "2c", "2s"]

cpu_name_pool = ["John Marston", "Charles Smith", "Arthur Morgan"]
cpu_pool = []       # cpu players pool
players = []        # all players pool
players_wd = []     # players pool without dealer
input_error = "Incorrect value. Please, type the correct amount of CPU players." \
              "\n 0 to play alone" \
              "\n 1 for one CPU player" \
              "\n 2 for two CPU players" \
              "\n 3 for three CPU players."

# initiate dealer and user objects
dealer = Gambler("Dealer")

while True:
    user_player = Player(input("Enter your name: "))
    if not user_player.name:
        print("Your name cannot be empty. Please, enter your name.")
    elif len(user_player.name) < 2 or len(user_player.name) > 15:
        print("Your name has to be minimum 2 and maximum 15 characters long. Please, try again.")
    elif not user_player.name.isalpha():
        print("Name must contain letters only. Please, try again.")
    else:
        players.append(user_player)
        players_wd.append(user_player)
        print("Hello, " + user_player.name + "!\n")
        time.sleep(sleep_time)
        break

# Initiate players
while True:
    num_of_cpu = input("Enter a number of CPU players: \n"
                       "minimum 0 \n"
                       "maximum 3\n")

    try:
        if 0 <= int(num_of_cpu) <= 3:
            num_of_cpu = int(num_of_cpu)
            # create cpu players
            for cpu in range(0, num_of_cpu):
                cpu_pool.append(Player(cpu_name_pool[cpu]))
                players.append(cpu_pool[cpu])
                players_wd.append(cpu_pool[cpu])
            players.append(dealer)
            break
        else:
            time.sleep(sleep_time / 2)
            print(input_error)

    # if user input contains non integers
    except ValueError:
        time.sleep(sleep_time / 2)
        print(input_error)


# START GAME
play_deck = []
exit_game = False
while not exit_game:
    # deck for dealing cards
    play_deck = origin_deck.copy()
    play_deck = shuffling(play_deck)

    # place bets
    for player in players_wd:
        if player.name == user_player.name:
            while True:
                time.sleep(sleep_time)
                bet = input("Place a bet (minimum bet is 2): ")
                if not bet:
                    print("You must place a bet. Please, try again.")
                elif not bet.isdigit():
                    print("Wrong input. The bet must be numeric value. Please, try again")
                else:
                    break
            player.place_bet(int(bet), user_player.name)
        else:
            bet = random.randint(2, 10)
            player.place_bet(int(bet))

    # deal cards
    i = 0
    while i < 2:
        for player in players:
            player.draw_a_card(play_deck)
        i += 1

    # count players scores:
    for player in players:
        player.count_scores()

    # print the table
    for player in players_wd:
        if player.name == user_player.name:
            player.print_dealer(False, False, True)
        else:
            player.print_dealer(False, False)
    dealer.print_dealer(True)

    # place insurance bet
    if dealer.hand[0] == "Ah" or dealer.hand[0] == "Ad" or dealer.hand[0] == "As" or dealer.hand[0] == "Ac":
        if user_player.money - user_player.bet / 2 >= 0:
            while True:
                print("The dealer has Ace. Do you want to place an insurance bet?")
                time.sleep(sleep_time)
                ins = input("y or n: ")
                if ins == 'y':
                    players_wd[0].insurance(user_player.name)
                    break
                elif ins == 'n':
                    break
                else:
                    print("Incorrect input. Please, enter y for YES or n for NO")
        else:
            print("Dealer has an Ace, but you have no money to place an insurance bet.")

        for i in range(1, len(players_wd)):
            if players_wd[i].money - players_wd[i].bet / 2 > 0:
                pos_answer = random.randint(0, 100)
                if pos_answer >= 80:
                    players_wd[i].insurance(user_player.name)
# if dealer.hand[0] == "Ah" or dealer.hand[0] == "Ad" or dealer.hand[0] == "As" or dealer.hand[0] == "Ac":
        if dealer.blackjack:
            time.sleep(sleep_time)
            print("Dealer has Blackjack!")
            for player in players_wd:
                time.sleep(sleep_time)
                if player.insured:
                    player.money += player.bet
                    if player.name == user_player.name:
                        print("You broke even. You have " + str(player.money) + "$ left.")
                    else:
                        print(player.name + " broke even. " + player.name + " has " + str(player.money) + "$ left.")
                else:
                    if player.name == user_player.name:
                        print("You've lost " + str(player.bet) + "$. You have " + str(player.money) + "$ left.")
                    else:
                        print(player.name + " has lost " + str(player.bet) + "$. " + player.name + " has " + str(
                            player.money) + "$ left.")
        else:
            time.sleep(sleep_time)
            print("Dealer has no Blackjack!")
            for player in players_wd:
                time.sleep(sleep_time)
                if player.insured:
                    if player.name == user_player.name:
                        print("You have lost your insurance bet.")
                    else:
                        print(player.name + " has lost insurance bet.")
                    player.bet -= player.bet / 3

    if not dealer.blackjack:
        # start players turns
        for player in players_wd:
            if player.name == user_player.name:
                print("\nYour turn.")
            else:
                print("\n" + player.name + " turn.")
            if not player.blackjack:
                player.player_actions(play_deck, dealer.hand, user_player.name)
            if player.split:
                player.player_actions(play_deck, dealer.hand, user_player.name, False, True)

        all_busted = 0
        all_split = 0
        for player in players_wd:
            if player.bust or player.doublebust:
                all_busted += 1
            else:
                break
            if player.split:
                all_split += 1

        if all_busted != len(players_wd) + all_split:
            print("\nDealer turn.")
            dealer.player_actions(play_deck, dealer.hand, "skip", True)

        # comparing cards
        if not dealer.bust:
            for player in players_wd:
                if player.name == user_player.name:
                    player.comparing(dealer.score, True)
                else:
                    player.comparing(dealer.score)
                if player.split:
                    if player.name == user_player.name:
                        player.comparing(dealer.score, True, True)
                    else:
                        player.comparing(dealer.score, False, True)
        else:
            for player in players_wd:
                if player.name == user_player.name:
                    player.comparing(dealer.score, True, False, True)
                else:
                    player.comparing(dealer.score, False, False, True)
                if player.split:
                    if player.name == user_player.name:
                        player.comparing(dealer.score, True, True, True)
                    else:
                        player.comparing(dealer.score, False, True, True)

    for player in players_wd:
        if player.name == user_player.name:
            player.print_dealer(False, False, False)
        else:
            player.print_dealer()
    dealer.print_dealer(True, True)

#  check if player has money to continue
    for player in players_wd:
        if player.money == 0:
            time.sleep(sleep_time)
            if player.name == user_player.name:
                print("You lost all your money. Better luck next time!")
                exit_game = True
            else:
                print(player.name + " has lost all money.")
            players.remove(player)
            players_wd.remove(player)
            del player

# reset all attributes for new turn

    for player in players:
        player.clear_turn(dealer.name)

# exit game check

    if not exit_game:
        time.sleep(sleep_time)
        print("\nDo you want to continue?\n"
              "Y for YES\n"
              "N for NO")
        while True:
            cont = input(": ")
            if cont == 'Y' or cont == 'y':
                break
            elif cont == 'N' or cont == 'n':
                exit_game = True
                break
            else:
                print("Incorrect input. Please, enter a correct answer.")

    time.sleep(sleep_time)
    if exit_game:
        print("Thanks for playing. See you next time!")
    else:
        print("Preparing the table for the next round. Get ready...")
    time.sleep(sleep_time * 2)
