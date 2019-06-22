import unittest
from Player_file import Player
from Player_file import Gambler


class TestPlayer(unittest.TestCase):

    def setUp(self):
        players = []
        self.dealer = Gambler('Dealer')
        self.player1 = Player('John')
        self.player2 = Player('Arya')
        self.player3 = Player('Sansa')

        players.append(self.dealer)
        players.append(self.player1)
        players.append(self.player2)
        players.append(self.player3)

        for player in players:
            player.blackjack = False
            player.hand = []
            player.doublehand = []
            player.score = 0
            player.doublescore = 0
            player.bust = False
            player.doublebust = False
            player.init_count = True
            player.bet = 0
            player.doublebet = 0
            player.split = False
            player.insured = False

    def test_count_scores(self):

        self.player1.hand = ['Ah', '10c']
        self.player2.hand = ["Ah", "8c", "2c"]
        self.player2.init_count = False
        self.player3.doublehand = ['10c', '2c', '10h']
        self.dealer.hand = ['Ac', '8c', '10c']

        self.player1.count_scores()
        self.player2.count_scores()
        self.player3.count_scores(True)
        self.dealer.count_scores()

        self.assertEqual(self.player1.score, 21)
        self.assertEqual(self.player2.score, 21)
        self.assertEqual(self.player3.doublescore, 22)
        self.assertEqual(self.dealer.score, 19)
        self.assertEqual(self.player1.blackjack, True)
        self.assertEqual(self.player2.blackjack, False)

    def test_draw_a_card(self):
        deck = ['Ah', 'Jc', '5h']
        self.player1.draw_a_card(deck)
        self.player2.draw_a_card(deck, True)

        self.assertEqual(self.player1.hand, ['Ah'])
        self.assertEqual(self.player2.doublehand, ['Jc'])
        self.assertEqual(deck, ['5h'])
        

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()


