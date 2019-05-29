import time
import random

delay = 0.6
# dict to count score
origin_deck_dict = {"Ah": 11, "Ad": 11, "Ac": 11, "As": 11,
                    "Kh": 10, "Kd": 10, "Kc": 10, "Ks": 10,
                    "Qh": 10, "Qd": 10, "Qc": 10, "Qs": 10,
                    "Jh": 10, "Jd": 10, "Jc": 10, "Js": 10,
                    "10h": 10, "10d": 10, "10c": 10, "10s": 10,
                    "9h": 9, "9d": 9, "9c": 9, "9s": 9,
                    "8h": 8, "8d": 8, "8c": 8, "8s": 8,
                    "7h": 7, "7d": 7, "7c": 7, "7s": 7,
                    "6h": 6, "6d": 6, "6c": 6, "6s": 6,
                    "5h": 5, "5d": 5, "5c": 5, "5s": 5,
                    "4h": 4, "4d": 4, "4c": 4, "4s": 4,
                    "3h": 3, "3d": 3, "3c": 3, "3s": 3,
                    "2h": 2, "2d": 2, "2c": 2, "2s": 2}


class Gambler(object):
    def __init__(self, name):
        self.name = name
        self.blackjack = False
        self.hand = []
        self.doublehand = []
        self.score = 0
        self.doublescore = 0
        self.bust = False
        self.doublebust = False
        self.init_count = True
        self.bet = 0
        self.doublebet = 0
        self.split = False

    def count_scores(self, split=False):
        score = 0
        if split:
            user_hand = self.doublehand.copy()
            user_hand2 = self.doublehand.copy()
        else:
            user_hand = self.hand.copy()
            user_hand2 = self.hand.copy()

        for i in range(0, len(user_hand)):
            card = user_hand[i]
            if card == "Ah" or card == "Ad" or card == "Ac" or card == "As":
                user_hand2.append(user_hand2.pop(user_hand2.index(card)))

        for i in range(0, len(user_hand2)):
            card = user_hand2[i]
            if card == "Ah" or card == "Ad" or card == "Ac" or card == "As":
                if score + origin_deck_dict[card] > 21:
                    score += 1
                else:
                    score += 11
            else:
                score += origin_deck_dict[card]
        if self.init_count:
            if score == 21:
                self.blackjack = True
            self.init_count = False
        if split:
            self.doublescore = score
        else:
            self.score = score

    def draw_a_card(self, play_deck, split=False):
        if split:
            self.doublehand.append(play_deck[0])
            play_deck.pop(0)
        else:
            self.hand.append(play_deck[0])
            play_deck.pop(0)
        return play_deck

    def player_actions(self, play_deck, dealer_hand, name="not_user", deal=False, split=False):
        if self.name == name:
            print("1. p - Show my hand\n"
                  "2. d - Show dealer's hand\n"
                  "3. h - Hit\n"
                  "4. s - Stand")
            if len(self.hand) == 2 and 9 < self.score < 12 and self.money - self.bet * 2 > 0:
                if self.hand[0][0] == self.hand[1][0]:
                    print("5. do - Double down\n"
                          "6. sp - Split")
                else:
                    print("5. do - Double down\n")
            elif self.hand[0][0] == self.hand[1][0]:
                print("5. sp - Split")
            while True:
                while True:
                    action = input("\nChoose an action: ")
                    if action:
                        break
                    else:
                        print("Incorrect input.")
                time.sleep(delay)
                if action == "Hit" or action == "hit" or action == "h" or action == "H":
                    if split:
                        self.draw_a_card(play_deck, True)
                        self.count_scores(True)
                        score = self.doublescore
                        hand = self.doublehand
                    else:
                        self.draw_a_card(play_deck)
                        self.count_scores()
                        score = self.score
                        hand = self.hand
                    self.print_dealer(False, False, True)
                    print("You've got " + hand[-1] + ".")
                    print("Your current score is " + str(score))
                    time.sleep(delay)
                    if score > 21:
                        if split:
                            self.doublebust = True
                        else:
                            self.bust = True
                        print("You've busted with " + str(score) + ".")
                        break
                    elif score == 21:
                        print("You've got 21!")
                        break
                elif action == "Stand" or action == "stand" or action == "s" or action == "S":
                    print("You've stayed with " + str(self.score) + ".")
                    break
                elif action == "Print" or action == "print" or action == "p" or action == "P":
                    self.print_dealer(True, True)
                elif action == "dealer" or action == "Dealer" or action == "D" or action == "d":
                    print("Dealer hand: " + dealer_hand[0])
                elif action == "Double" or action == "double" or action == 'do':
                    if len(self.hand) == 2 and 9 < self.score < 12 and self.money - self.bet > 0:
                        self.draw_a_card(play_deck)
                        self.count_scores()
                        self.money -= self.bet
                        self.bet *= 2
                        print(self.name + " got " + self.hand[-1] + ".")
                        print(self.name + " stayed with " + str(self.score) + ".")
                        break
                elif action == "Split" or action == "split" or action == "sp":
                    if len(self.hand) == 2 and not self.doublehand and self.hand[0][0] == self.hand[1][0]:
                        self.split = True
                        self.doublehand.append(self.hand[-1])
                        self.hand.pop(-1)
                        self.draw_a_card(play_deck)
                        self.draw_a_card(play_deck, True)
                        self.count_scores()
                        self.count_scores(True)
                        self.money -= self.bet
                        self.doublebet = self.bet
                        self.print_dealer(False, False, True)

                else:
                    print("Incorrect input.")
        else:
            while True:
                time.sleep(delay)
                if len(self.hand) == 2:
                    if 9 < self.score < 12 and self.money - self.bet > 0 and not deal:
                        double_down = random.randint(0, 100)
                        if double_down > 80:
                            self.draw_a_card(play_deck)
                            self.count_scores()
                            print(self.name + " got " + self.hand[-1] + ".")
                            print(self.name + " stayed with " + str(self.score) + ".")
                            break

                if self.score < 17:
                    self.draw_a_card(play_deck)
                    self.count_scores()
                    print(self.name + " got " + self.hand[-1] + ".")
                    print(self.name + " score is " + str(self.score) + ".")
                elif self.score > 21:
                    print(self.name + " got busted with " + str(self.score) + ".")
                    self.bust = True
                    break
                elif self.score == 21:
                    print(self.name + " got 21!")
                    break
                else:
                    print(self.name + " stayed with " + str(self.score) + ".")
                    break

    def print_dealer(self, dealer=False, endgame=False, username=False):
        time.sleep(delay)
        if not username:
            print(self.name + " hand: ")
        else:
            print("Your hand: ")
        if dealer:
            if endgame:
                print(self.hand)
            else:
                print(self.hand[0])
        else:
            if self.split:
                print(self.hand)
                print(self.doublehand)
            else:
                print(self.hand)


class Player(Gambler):
    def __init__(self, name):
        Gambler.__init__(self, name)
        self.money = 300.0
        self.insured = False

    def place_bet(self, bet, uname="CPU"):
        time.sleep(delay)
        if bet < 2:
            if self.name == uname:
                print("Minimum bet is 2. Bet is corrected.")
            self.bet = 2
            self.money -= self.bet
        elif bet > self.money:
            if self.name == uname:
                print("You don't have enough money to place this bet. Bet is corrected.")
            self.bet = self.money
            self.money -= self.bet
        elif bet % 2 == 1:
            if self.name == uname:
                print("Bet should be stepped by 2 (2, 4, 6, 8 etc.). Bet is corrected.")
            self.bet = bet - 1
            self.money -= self.bet
        else:
            self.bet = bet
            self.money -= self.bet
        print(self.name + " bet " + str(self.bet) + "$.")
        print(self.name + " has " + str(self.money) + "$ left. \n")

    def count_win(self, gain):
        self.money += gain

    def insurance(self, name):
        self.money -= self.bet / 2
        if name == self.name:
            print("You've placed " + str(self.bet / 2) + "$ insurance bet.")
        else:
            print(self.name + " has placed " + str(self.bet / 2) + "$ insurance bet.")
        self.bet += self.bet / 2
        self.insured = True

    def comparing(self, dealer_score, user=False, split=False, dealer_bust=False):
        if split:
            bust = self.doublebust
            bet = self.doublebet
            score = self.doublescore
        else:
            bust = self.bust
            bet = self.bet
            score = self.score
        if not bust:
            gain = 0
            if self.blackjack:
                gain = bet * 2 + bet / 2
                self.count_win(gain)
            elif score > dealer_score:
                gain = bet * 2
                self.count_win(gain)
            elif score == dealer_score:
                gain = bet
                self.count_win(gain)
            else:
                if dealer_bust:
                    gain = bet * 2
                    self.count_win(gain)
                else:
                    bust = True
            time.sleep(delay)
            if user:
                if bust:
                    print("You've lost " + str(bet) + "$.")
                elif gain == bet:
                    print("You've broke even.")
                else:
                    print("You've earned " + str(gain) + "$.")
                print("You have " + str(self.money) + "$ in total.")
            else:
                if bust:
                    print(self.name + " has lost " + str(bet) + "$. ")
                elif gain == bet:
                    print(self.name + " has broke even.")
                else:
                    print(self.name + " has earned " + str(gain) + "$.")
                print(self.name + " has " + str(self.money) + "$ in total.")
        else:
            if user:
                print("You've lost " + str(bet) + "$.")
                print("You have " + str(self.money) + "$ in total.")
            else:
                print(self.name + " has lost " + str(bet) + "$.")
                print(self.name + " has " + str(self.money) + "$ in total.")

