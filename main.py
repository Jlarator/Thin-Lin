''' This game is called "tien len", its a vietnamese card game. 
 Rules for the Game
 https://www.pagat.com/climbing/thirteen.html'''

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import random


# Decision variables
initialize = 0
player_action = 0
test = 0
first_turn = True
new_round = False
bomb_played = False
most_bitching_play = None

# Game variables
players = []
cards = []
selected_cards = []
selected_tiles = []
played_set = None
current_play = None
set_tiles = []
turn = None
main_deck = None
turn_player = None
lower_card = None

# Ranks or values are ranked from lowest to highest. Three is the lowest value and 2 is the highest.
values = {'Three': ['Three', 3], 'Four': ['Four', 4],'Five': ['Five', 5], 'Six': ['Six', 6],
          'Seven': ['Seven', 7], 'Eight': ['Eight', 8],'Nine': ['Nine', 9], 'Ten': ['Ten', 10],
          'Jack': ['Jack', 11], 'Queen': ['Queen', 12], 'King': ['King', 13], 'Ace': ['Ace', 14], 'Two': ['Two', 15]}

# The suits are ranked from lowest to highest: Spades being the lowest and hearts the highest
suits = [['Spades', 4], ['Clubs', 3], ['Diamonds', 2], ['Hearts', 1]]
imge = [' ']

# Main frame (window)
window = Tk()
window.title('Tien Len')

# These are the variables for the panel that will be in the main window.
# they are initialized at the modular level so they can be used throughout
# anywhere in the code.
panel_1 = None # submition field (top of the screen)
panel_2 = None # selection field (mid screen)
panel_3 = None # player field (bottom of the screen)


class Card:
    def __init__(self, suit, value, pic, score):
        '''
        THis is a card in the game.
        :param suit: card suit
        :param value: card rank or value
        :param pic: the picture that corresponds to this card. the pictures should be
        in a file called 'images' in this project file.
        :param score: The score a card has. the lowest card is 3 of spades, and the highest 2 of hearts
        '''
        self.suit = suit
        self.value = value
        self.pic = pic
        self.score = score

    def __str__(self):
        return str(self.value[0]) + ' of ' + str(self.suit[0])

    def describe(self):
        print('Describing')
        return str(self.value[0]) + ' of ' + str(self.suit[0])

    def get_suit(self):
        return self.suit[1]

    def get_value(self):
        return self.value[1]

    def get_score(self):
        return self.score

    def set_pic(self, image):
        self.pic = image

    def get_pic(self):
        return self.pic


class Player:
    def __init__(self, number):
        """
        this will be used to represent the human players.
        each player has a deck of cards. a deck of tiles that are
        used to represent the cards as physical items in the screen.
        - Skip_turn: if the player decided to skip his turn
        - played_bomb: if player played a bomb. This is helps
            see if the player can earn back his turn after skipping it.(See Rules for the game)
        :param number: what number player it is. this facilitates
        changing turns and finding the winner.
        """
        self.deck = []
        self.tiles = []
        self.number = number
        self.skipped_turn = False
        self.played_bomb = False

    def present_cards(self):
        """
        This is only used to present the cards onto
        the player field (The lowest part of the scree)
        :return: nothing
        """

        x = 80
        y = 80
        for card in self.deck:
            game_card = Tile(x, y, card)
            game_card.set_panel(panel_3)
            game_card.set_field_string('Panel 3')
            game_card.draw_faceside()
            self.tiles.append(game_card)
            x += 100

    def get_bomb(self):
        return self.played_bomb

    def has_bomb(self):
        self.played_bomb = True

    def no_bomb(self):
        self.played_bomb = False

    def get_skipper(self):
        return self.skipped_turn

    def skip_turn(self):
        self.skipped_turn = True

    def gain_turn(self):
        self.skipped_turn = False

    def add_card(self, card):
        self.deck.append(card)

    def remove_card(self, card):
        self.deck.remove(card)

    def get_player_num(self):
        return self.number

    def check_win(self):
        if len(self.deck) == 0:
            return True
        else:
            return False

    def __str__(self):
        return 'Player ' + str(self.number)


class Deck:
    """
    This will hold the card representations.
    this does not produces a shuffled deck,
    the shuffle deck has to be called on a
    Deck instance
    """
    def __init__(self):
        self.deck = []

    def __str__(self):
        for i in self.deck:
            return i.describe()

    def make_deck(self):
        print('Building deck')
        score = 1
        for value in values:
            for suit in suits:
                file_name = values[value][0][0:2].upper() + suit[0][0]
                img = ImageTk.PhotoImage(Image.open('images//' + file_name + '.jpg'))
                card = Card(suit, values[value], img, score)
                self.deck.append(card)
                score += 1
        print('Deck built')

    def shuffle_deck(self):
        random.shuffle(self.deck)
        print('Deck shuffled')

    def deal(self):
        return self.deck.pop()

    def deal_to_players(self, player_list):
        print('\nDealing cards to players')
        n = 1
        tn = len(player_list)
        for player in player_list:
            print('Dealing to {} out of {} players'.format(n, tn))
            for i in range(0,13):
                player.add_card(self.deal())
            n += 1
        print('\n')

    def clear_deck(self):
        self.deck.clear()


class Tile:
    def __init__(self, x, y, card):
        """
        This what will be used to represent cards onto the screen.
        :param x: The x coordinate on the panel that the tile will be placed
        :param y: The y coordinate on the panel that the tile will be placed
        :param card: The card the the tile will represent
        - Panel: the Tk panel where the tile will be placed
        - Field String: a string representation of the panel that is in
        - Card Label: A Tk label that will show the card image associated with the tile.
        - Tile: a window in which to present the card label.
        """
        self.x = x
        self.y = y
        self.card = card
        self.panel = None
        self.field_string = None
        self.card_label = None
        self.window = None

    def draw_faceside(self):
        self.card_label = Label(self.panel, image=self.card.get_pic())
        self.card_label.pack()
        self.window = self.panel.create_window(self.x, self.y, width=80, height=120,
                                               window=self.card_label, tags=self.card)

    def set_field_string(self, p_string):
        self.field_string = p_string

    def get_field_string(self):
        return self.field_string

    def set_panel(self, panel):
        self.panel = panel

    def get_panel(self):
        return self.panel

    def get_widget(self):
        return self.card_label

    def get_card(self):
        return self.card

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class PlayType:
    def __init__(self, card_set):
        """
        based on the cards passed as a parameter: this examines
        if the play is a valid play, and what type of play it is.
        a play that consists of only one card is always a valid play.
        It also, sorts, and finds the highest valued card in the play.
        :param card_set: The cards that the player wants to play
        """

        self.card_set = card_set
        self.length = len(card_set)
        self.same_suit = True
        self.same_rank = True
        self.highest_card = None
        self.sequential = True
        self.sequential_pair = True
        self.pairs = 0
        self.single_pair = False
        self.all_ace = True
        self.is_valid = True

        iteration = len(card_set) - 1

        # Checks to see if the card set is full of the same suit
        # or if they are of the same rank, or if they are all aces.
        for i in range(0, iteration):
            next_card = i + 1
            if self.card_set[i].get_value != 14 and self.card_set[next_card].get_value()!= 14:
                self.all_ace = False
            if self.card_set[i].get_suit() != self.card_set[next_card].get_suit():
                self.same_suit = False
            if self.card_set[i].get_value() != self.card_set[next_card].get_value():
                self.same_rank = False

        # Organizes the deck by card value and finds the highest value card
        for i in range(0,len(self.card_set)):
            n = i + 1
            for o in range(0, iteration):
                temp_card = self.card_set[o]
                nex = o + 1
                if self.card_set[o].get_value() > self.card_set[nex].get_value():
                    self.card_set[o] = self.card_set[nex]
                    self.card_set[nex] = temp_card
        self.highest_card = self.card_set[-1]

        # Finds if the cards in the deck are pairs, triplets, or quadruplets
        same_in_a_row = [] # if there are cards that are the same in a row, they will be appended to this.
        pairs = 0
        triplets = 0
        quadruplets = 0
        for t in range(0, iteration):
            n = t + 1
            if self.card_set[t].get_value() == self.card_set[n].get_value():
                # if the current card has the same value as the next card
                # 'same' will be set to True
                same = True
            else:
                same = False

            if same:
                same_in_a_row.append(self.card_set[n])
                if self.card_set[t] not in same_in_a_row:
                    # if the current and next values are the same, and the
                    # cards are not in the 'same in a row' list, it will add
                    # the cards to it
                    same_in_a_row.append(self.card_set[t])

            if not same or t == iteration - 1:
                # if current and next cards are not the same, or if it reaches the end
                # of the list.
                print('the same length is {}'.format(len(same_in_a_row)))
                if len(same_in_a_row) == 2:
                    # if there were 2 in a row, pairs will be increased by one
                    pairs += 1
                    print('Pairs added')
                    same_in_a_row.clear()
                elif len(same_in_a_row) == 3:
                    # if there were 3 in a row, triplets will be added.
                    triplets += 1
                    print('Triplet added')
                    same_in_a_row.clear()
                elif len(same_in_a_row) == 4:
                    # same as above, but for 4 in a row.
                    quadruplets += 1
                    print('Quadruplet added')
                    same_in_a_row.clear()

        print('the highest card is {}'.format(self.highest_card))
        print('\n')

        print('There are {} pairs, and there are {} cards'.format(pairs, self.length))
        if self.length > 1:
            print('More than ONe')
            # plays of one card are valid. If longer they have to be checked
            if pairs * 2 != self.length:
                self.sequential_pair = False
            if self.length == 2:
                if pairs == 1:
                    # If the play is 2 cards. and they are a pair,
                    # it is a valid play.
                    print('The play is a single pair')
                    self.sequential_pair = False
                    self.same_suit = False
                    self.sequential = False
                    self.single_pair = True
            if self.length > 2:
                # If there 3 or more pairs, they have to be sequential
                # to be a valid play.
                if pairs == 2:
                    if not self.same_suit:
                        self.sequential_pair = False
                if pairs >= 3:
                    ind = 1
                    for crd in range(0, iteration):
                        nxt = ind + 2
                        print('Finding if sequential, ind: {}\n nxt:{}\n iteration{}'.format(ind, nxt, iteration))

                        if self.card_set[ind].get_value() + 1 != self.card_set[nxt].get_value():
                            self.sequential_pair = False
                if self.sequential_pair:
                    print('The play is a sequential pair')
                if not self.sequential_pair:
                    print('It is not a sequential pair')

        for ind in range(0, iteration):
            nxt = ind + 1
            if self.card_set[ind].get_value() + 1 != self.card_set[nxt].get_value():
                self.sequential = False

        if self.same_suit:
            print('cards are all the same suit')
        else:
            print('cards do not match suit')
        if self.same_rank:
            print('Cards are the same rank')
        else:
            print('cards don\'t have the same value')
        if self.sequential:
            print('card are sequential')
        else:
            print('cards are not sequential')

        if self.length == 2:
            if not self.single_pair:
                # if 2 cards and they are not a pair,
                # play is not valie
                self.is_valid = False
        elif self.length == 3:
            if not self.sequential and not self.same_rank:
                # if cards are an odd number,
                # they have to be sequential.
                self.is_valid = False
        elif self.length == 4:
            if not self.sequential and not self.same_rank:
                # if 4 cards, they have to be sequential or the
                # same rank
                self.is_valid = False
        elif self.length == 5:
            if not self.sequential:
                self.is_valid = False
        elif self.length >= 6:
            if not self.sequential and not self.sequential_pair:
                # if 6 or more cards, they have to be sequential or
                # sequential pairs.
                self.is_valid = False

    def __str__(self):
        if self.is_valid:
            return "Current play is valid"
        else:
            return "This play is dog crap"

    def find_card(self, target):
        return target in self.card_set

    def get_cards(self):
        return self.card_set

    def get_length(self):
        return self.length

    def same_suit(self):
        return self.same_suit

    def same_rank(self):
        return self.same_rank

    def get_highest(self):
        return self.highest_card

    def is_sequential(self):
        return self.sequential

    def is_pair_sequential(self):
        return self.sequential_pair

    def get_pairs(self):
        return self.pairs

    def is_single_pair(self):
        return self.single_pair

    def is_play_valid(self):
        return self.is_valid


def check_play(play_set, new_play):
    '''
    checks to see if the new play beats the play set
    :param play_set: the play that the turn player has to beat and is already set
    :param new_play: the play that the turn player submits
    :return: true if the new play beats the set play. false otherwise.
    '''
    global bomb_played
    output = False

    new_len = new_play.get_length() # how many cards in the new play
    set_len = play_set.get_length() # how many cards in the play already set

    set_high = play_set.get_highest().get_score() # The highest card value in the play already set
    new_high = new_play.get_highest().get_score() # The highest card value in the new play

    ace_in = False
    if set_high == 14:
        ace_in = True
    print(f'the set play highest card is {set_high}\n and the new highest card is {new_high}')

    if set_len == 1:
        # if the set play is a single card
        if new_len == 1:
            if new_high > set_high:
                print('one card plays, new beats old')
                # if the new card value beats the set
                output = True
        elif ace_in and new_len == 4:
            print('Trying to beat an ace with a four of a kind')
            if new_play.same_suit():
                turn_player.has_bomb()
                # if player bombs an Two
                output = True

        elif ace_in and new_len == 6:
            print('Trying to beat an ace with 3 sequential pairs')
            if new_play.is_pair_sequential():
                turn_player.has_bomb()
                # if player bombs a Two
                output = True

    if set_len == 2 and ace_in and play_set.same_rank():
        print('Trying to beat 2 aces with 4 sequential pairs')
        if new_len == 8 and new_play.is_pair_sequential():
            turn_player.has_bomb()
            # if player bombs  a 2 Twos
            output = True

    if set_len == 3 and ace_in and play_set.same_rank():
        print('Trying to beat 3 aces with 5 sequential pairs')
        if new_len == 10 and new_play.is_pair_sequential():
            turn_player.has_bomb()
            # if player bombs a 3 twos
            output = True

    elif 2 <= set_len <= 5:
        print('set len between 2 and 5')
        if set_len == new_len:
            print('Both plays are the same length')
            if new_high > set_high:
                # if both plays are the same length
                # and the highest card in the new play beats the highest in the old play
                output = True

    elif set_len > 5:
        if play_set.is_pair_sequential() and new_play.is_pair_sequetial():
            if new_high > set_high and set_len == new_len:
                # if both plays are six or more and they are sequential pairs ex. (4,4,5,5,6,6,7,7)
                output = True

        elif play_set.is_sequential() and new_play.is_sequential():
            if new_high > set_high and set_len == new_len:
                # if both plays are more than 5 and they are sequential.
                output = True

    print('--THis is in check play---')
    for i in new_play.get_cards():
        print(i)

    return output


def clear_set_play():
    """
    Gets called when a play doesn't get beat by other players.
    this clears the submition panel (the top part of the screen) of any cards
    and makes sure that any players that lost their turns get them back.
    :return: nothing
    """
    global set_tiles
    global played_set
    global players

    for tile in set_tiles:
        tile.get_widget().destroy()

    for p in players:
        p.gain_turn()

    set_tiles.clear()
    played_set = None


def game():
    """
    This runs the game. it uses the previous variables and
    functions to start and run the game.
    :return:
    """
    global turn_player
    global player_action
    global selected_cards
    global selected_tiles
    global set_tiles
    global panel_3
    global panel_2
    global panel_1

    def winner():
        """
        When a player has no cards, that player wins, and this function is called
        :return:
        """
        global window
        global turn_player

        print('Winning function appeared')

        window.destroy()
        winner_win = Tk()
        winner_win.title(f'{turn_player} wins, everyone else sucks!')
        chicken = ImageTk.PhotoImage(Image.open('images//winner.jpg'))
        winner_panel = tk.Label(winner_win, image=chicken)

        winner_panel.pack()
        winner_win.mainloop()

    def submit_play(p_cards):
        """

        :param p_cards: THe play (set of cards) that the current turn player submitted.
        this play beat the previously set play and will be placed on top of the
        screen for the rest of player to beat.
        :return: nothing
        """
        starting_x_index = 800 - len(p_cards) * 85 / 2

        print('\nOrganizing play\n')
        for p_card in p_cards:
            for i in range(0, len(p_cards) - 1):
                temp_card = p_cards[i]
                print('not rearranging')
                if p_cards[i].get_card().get_score() > p_cards[i+1].get_card().get_score():
                    print('rearranging')
                    p_cards[i] = p_cards[i + 1]
                    p_cards[i+1] = temp_card

        for s in p_cards:
            temp_card = s.get_card()
            temp_y = s.get_y()

            s.get_widget().destroy()

            new_tile = Tile(starting_x_index, temp_y, temp_card)
            new_tile.set_field_string('Panel 1')
            set_tiles.append(new_tile)

            new_tile.set_panel(panel_1)
            new_tile.draw_faceside()
            starting_x_index += 85
            keep_playing()

    def change_panel(p_tile, p_player):
        """
        Durint a player turn, if a card is selected,
        this function will alternate the placement of the tile
        in the screen from the selection field (mid screen) to the
        player field (bottom of the screen)
        :param p_tile: The selected tile
        :param p_player: The Turn player that selected the tile
        :return: nothing
        """
        print('The card changing panel is {}'.format(p_tile.get_card()))
        if p_tile.get_field_string() == 'Panel 3':
            p_player.remove_card(p_tile.get_card())
            temp_card = p_tile.get_card()
            temp_x = p_tile.get_x()
            temp_y = p_tile.get_y()

            selected_cards.append(temp_card)
            p_tile.get_widget().destroy()

            new_tile = Tile(temp_x, temp_y, temp_card)
            new_tile.set_field_string('Panel 2')
            selected_tiles.append(new_tile)
            p_player.tiles.append(new_tile)

            new_tile.set_panel(panel_2)
            new_tile.draw_faceside()
            keep_playing()

        elif p_tile.get_field_string() == 'Panel 2':
            p_player.add_card(p_tile.get_card())
            temp_card = p_tile.get_card()
            temp_x = p_tile.get_x()
            temp_y = p_tile.get_y()

            selected_cards.remove(temp_card)
            p_tile.get_widget().destroy()

            new_tile = Tile(temp_x, temp_y, temp_card)
            new_tile.set_field_string('Panel 3')
            selected_tiles.remove(p_tile)
            p_player.tiles.append(new_tile)

            new_tile.set_panel(panel_3)
            new_tile.draw_faceside()
            keep_playing()

    def mouse_clicked(event):
        """
        when the mouse is clicked, this function is called.
        it identifies if a card is clicked.
        :param event:
        :return:
        """
        global test
        global cards

        print('\nMouse clicked')
        print(event.x, event.y)
        test += 1
        clicked = str(event.widget)
        print('The source is {}'.format(event.widget))
        print('Times tested: {}'.format(test))

        for p in players:
            for t in p.tiles:
                tile_string = str(t.get_widget())
                if clicked == tile_string:
                    print('Card selected is {}, and the field string is {}'.format(t.get_card(),
                    t.get_field_string()))
                    change_panel(t, p)

    def key(event):
        print("pressed", repr(event.char))

    def call_back(event):
        print(event.x, event.y)
        print('call back')

    global initialize

    if initialize == 0:

        global window
        global main_deck
        global players

        turn_player = None

        main_deck = Deck()
        print('Initializing game set up')
        question_panel = Canvas(window)
        question_panel.pack()

        def one_player():
            """
            Adds player one to the list of players
            :return:
            """
            print('adding player one')
            player_1 = Player(1)
            players.append(player_1)
            question_panel.destroy()
            global initialize
            initialize = 1
            keep_playing()

        def two_player():
            """Adds player two to the player list"""
            print('adding player two')
            player_2 = Player(2)
            players.append(player_2)
            one_player()

        def three_player():
            """Adds player three to the player list"""
            print('adding player three')
            player_3 = Player(3)
            players.append(player_3)
            two_player()

        def four_player():
            """Adds player four to the player list"""
            print('adding player four')
            player_4 = Player(4)
            players.append(player_4)
            three_player()

        question_prompt = Label(question_panel, text='How many players are there?')
        question_prompt.pack()

        button_panel = Canvas(question_panel)
        button_panel.pack(pady=(10, 10))

        one = Button(button_panel, width=10, text='one', command=one_player)
        one.pack(side=LEFT, padx=(10, 10))

        two = Button(button_panel, width=10, text='two', command=two_player)
        two.pack(side=LEFT, padx=(10, 10))

        three = Button(button_panel, width=10, text='three', command=three_player)
        three.pack(side=LEFT, padx=(10, 10))

        four = Button(button_panel, width=10, text='four', command=four_player)
        four.pack(side=LEFT, padx=(10, 10))

        panel_1 = Canvas(window, bg='green', width=1600, height=280, bd=0, highlightthickness=0, relief='ridge')
        panel_1.pack(fill="both", expand=True)

        panel_2 = Canvas(window, bg='green', width=1600, height=280, bd=0, highlightthickness=0, relief='ridge')
        panel_2.pack(fill="both", expand=True)

        panel_3 = Canvas(window, bg='green', width=1600, height=280, bd=0, highlightthickness=0, relief='ridge')
        panel_3.pack(fill="both", expand=True)

        window.bind("<Key>", key)
        window.bind("<Button-1>", mouse_clicked)
        window.focus_force()
        window.mainloop()

    elif initialize == 1:
        # This initializes the game
        # this iteration finds the lowest card among the players and
        # designates that player as the turn player

        global turn
        global lower_card
        global players
        turn = 0
        turn_player = None
        print('Starting first round')
        print('turn player is set as {}'.format(turn_player))
        main_deck.make_deck()
        main_deck.shuffle_deck()
        main_deck.deal_to_players(players)

        lower_card = Card([None, 5], [None, 16], None, 53)

        print('Finding lowest Card')
        for player in players:
            print(player)
            for i in range(len(player.deck) - 1):
                if player.deck[i].get_score() < lower_card.get_score():
                    lower_card = player.deck[i]
                    turn_player = player

        print('The player with the lowest card is {} and player {} has it.'.format(lower_card, turn_player))
        initialize += 1
        turn += 1
        keep_playing()

    elif initialize == 2:
        # after the game is initialized, the game will run on this
        # iteration.

        global first_turn

        print(f'\nStarting Round {turn}\n')
        print(f' The turn player this round is {turn_player}')

        panel_1.config(height=240)
        panel_2.config(height=240)
        panel_3.config(height=240)

        print(f"Player action is {player_action}")
        move_panel= Canvas(window, bg='Yellow', width=1600, highlightthickness=0) # this is a small banner at the bottom of the screen, and it displays the turn player
        label_1 = Label(window, bg='Yellow', width=1600, text='{} will go first, all else can suck it'.format(turn_player),
                        highlightthickness=0)

        if player_action == 0:
            move_panel.pack()
            label_1.pack()
            player_action += 1

        def skip_turn():
            """if the turn player skips his turn, this function
            returns any cards from the selection field to the player
            and clears the selection and player field of any tiles
            as well as changes the turn
            """
            global current_play
            global turn_player

            print('skipping turn')
            player_button.config(command=show_cards, text='See cards')

            for selected_tile in selected_tiles:
                # removes the tiles from the selection field
                selected_tile.get_widget().destroy()
            selected_tiles.clear()

            for selected_card in selected_cards:
                # returns the selected cards back to the player
                turn_player.add_card(selected_card)
            selected_cards.clear()

            turn_player.skip_turn() # marks the player that skipped

            current_play = None

            pass_button.pack_forget()
            change_turn()

        def show_cards():
            """ displayes the player cards as tiles in the player field"""
            for p in players:
                if turn_player == p:
                    print('This is player {}\'s turn and its presenting cards'.format(p))
                    p.present_cards()
            config_button()

        def change_turn():
            """ Before changing the turn player, it checks if the player won.
                if the player didn't, it clears the player field of any tiles
             """
            global turn_player
            global new_round

            if turn_player.check_win():
                winner()
            else:
                for t in turn_player.tiles:
                    t.get_widget().destroy()

                player_num = int(str(turn_player)[-1])
                if player_num == 1:
                    turn_player = players[0]
                    if turn_player == most_bitching_play:
                        new_round = True
                        clear_set_play()

                elif player_num > 1:
                    for p in players:
                        if p.get_player_num() == player_num -1:
                            turn_player = p
                            if turn_player == most_bitching_play:
                                new_round = True
                                clear_set_play()

                print('the turn player is now {}'.format(turn_player))
                label_1.config(text=f'This is {turn_player}\'s turn')
                keep_playing()

        player_button = Button(move_panel, text='Ready to see cards?', command=show_cards, width=20, height=10)
        pass_button = Button(move_panel, text='Pass', command=skip_turn, width=20, height=10)
        player_button.pack(side='left')

        def submit():
            """When a player selects their cards, and presses the submit button, this function gets
                called. This uses 'Check play' to see if the selected cards beat the already set
                play. If so, it advances to the next turn
            """

            global turn_player
            global turn
            global first_turn
            global new_round
            global current_play
            global played_set
            global most_bitching_play

            def advance_first_round():
                """If its the very first round, this will advance the turn"""
                global played_set
                global most_bitching_play

                submit_play(selected_tiles)
                played_set = current_play
                selected_tiles.clear()
                selected_cards.clear()
                most_bitching_play = turn_player
                player_button.config(command=show_cards, text="See cards")
                change_turn()

            def advance_turn():
                """Advances to the next turn"""
                global played_set
                global most_bitching_play

                submit_play(selected_tiles)
                played_set = current_play
                selected_cards.clear()
                selected_tiles.clear()
                most_bitching_play = turn_player
                player_button.config(command=show_cards, text="See cards")
                pass_button.pack_forget()
                change_turn()

            if len(selected_cards) > 0:
                current_play = PlayType(selected_cards)
                print(current_play)

                if first_turn:
                    print('submitting')
                    if current_play.find_card(lower_card) and current_play.is_play_valid():
                        first_turn = False
                        turn += 1
                        advance_first_round()

                    else:
                        print('lowest class qas not included in the play')

                elif new_round:
                    pass_button.pack_forget()
                    new_round = False
                    turn += 1
                    advance_first_round()

                elif not first_turn and current_play.is_play_valid():
                    print("this is checking the played set, {}".format(played_set))
                    print('not first turn')
                    turn += 1
                    outcome = check_play(played_set, current_play)

                    if outcome and not turn_player.get_skipper():
                        print('\n ---This guy is in a roll---\n ')
                        advance_turn()

                    elif outcome and turn_player.get_skipper():
                        print('THis guy skipped, but he has to bomb and ace')
                        if turn_player.get_bomb():
                            advance_turn()

                    elif not outcome:
                        print('The play you are trying to play sucks')

        def config_button():
            print('Configuring button')
            player_button.config(text='Submit Play', command=submit)
            if not first_turn and not new_round:
                pass_button.pack(side='right')


def keep_playing():
    game()


game()


