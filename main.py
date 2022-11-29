"""
Your days are numbered
This is a rogue-like deck builder that aims to teach people math. 
"""

from __future__ import annotations
from random import shuffle, seed, randint, choice, choices
import tkinter as tk
from tkinter import messagebox

class Card:

    # class variable here 
    operations_table = {
        "+" : lambda currentValue, cardValue: currentValue +  cardValue,
        "-" : lambda currentValue, cardValue: currentValue -  cardValue,
        "*" : lambda currentValue, cardValue: currentValue *  cardValue,
        "//": lambda currentValue, cardValue: currentValue // cardValue,
        "**": lambda currentValue, cardValue: currentValue ** cardValue,
        "%" : lambda currentValue, cardValue: currentValue %  cardValue if currentValue >= 0 else -(abs(currentValue) % cardValue)
    }

    # generate cost for shop phase
    cost_tiers = {
        "+" : 1, "-" : 1, "*" : 2, "//": 2, "**": 3, "%" : 3
    }

    def __init__(self, operation: str, value: int, cost: int = None) -> None:
        """Card objects have a value and operation. Cost is used during buy phase only."""
        #  check if operation is valid (in operations_table.keys)
        self.operation: str = operation
        self.value: int = value
        self.usable: bool = True
        # find cost and function
        self.cost: int = self.value*self.cost_tiers[self.operation] if cost == None else cost
        self._function: function = self.operations_table[self.operation]

    def __str__(self) -> str:
        return f"Operation: {self.operation} Value: {self.value} Cost: {self.cost}"

    def alt_str(self) -> str:
        return f"{self.operation}{self.value}"

    def use(self, currentValue: int) -> int: 
        """Returns new current value after card is played"""
        self.void()
        return self._function(currentValue, self.value)

    def void(self):
        """makes unselectable in shop phase"""
        self.usable = False

    def _copy(self) -> Card:
        """returns a duplicate of the card"""
        return Card(self.operation, self.value, self.cost)

class Player:
    def __init__(self) -> None:
        """Handles player actions"""
        ## Game Variables
        # create a copy of mainDeck to play 
        self.main_deck: list[Card] = []
        self.temp_deck: list[Card] = []

        self.hand: list[Card] = []
        self.hand_size = 5

        self.cargo: int = 10
        self.current_number: int = 0 
        self.objective_number: int = 10
        self.difficulty: int = 8
        
        self.turn_state: str = 'continue'
        self.level: int = 1
        self.turn: int = 1

        self.state: str = "game"

        ## Shop Variables
        self.shop_choices: list[Card] = []
        self.shop_size: int = 5
    
    # play phase functions

    def to_game(self) -> None:
        """denotes game mode == game"""
        self.state = "game"

    def to_shop(self) -> None:
        """denotes game mode == shop"""
        self.state = "shop"

    def to_deathscreen(self) -> None:
        """denotes game mode == death"""
        self.state = "death"

    def is_game(self) -> bool:
        """checks game mode == game"""
        return self.state == "game"

    def is_shop(self) -> bool:
        """checks game mode == shop"""
        return self.state == "shop"

    def create_temp_deck(self) -> None:
        """makes copies of all cards from main_deck into temp_deck."""
        self.temp_deck.clear()
        for card in self.main_deck:
            self.temp_deck.append(card._copy())

    def reset_deck(self) -> None:
        """Fill temp deck. Empty hand."""
        self.create_temp_deck()
        shuffle(self.temp_deck)
        self.hand.clear()

        self.turn: int = 1
        self.turn_state: str = 'continue'

    def draw(self) -> None:
        """Add cards to your hand. Check lose condition."""
        assert len(self.temp_deck) > 0
        card = self.temp_deck.pop()
        self.hand.append(card) 
        
    def play_card(self, position: int) -> None:
        """Player plays a card and update current number. Check win condition."""
        card: Card = self.hand[position]
        assert card.usable
        self.current_number = card.use(self.current_number)
        
    def update_cargo(self, number: int) -> None:
        """Updates cargo, used at the end of turn. Lowest cargo is 0."""
        self.cargo += number
        if self.cargo < 0:
            self.cargo = 0

    def is_win(self) -> bool:
        """Check win condition."""
        return self.current_number == self.objective_number

    def is_dead(self) ->bool:
        """Checks if player is out of cards"""
        return 0 == self.cards_left()

    def end_turn(self) -> None:
        """Call end of turn actions. if last turn, draw remaining"""
        # put usable cards from hand to bottom of deck
        for _ in self.hand:
            card: Card = _
            if card.usable:
                self.temp_deck.insert(0, card)
        self.hand.clear()
        self.update_turn_state()
        if self.turn_state != "win":
            self.update_cargo(number= -1)
            self.turn += 1
        
    def draw_hand(self) -> None:
        """draw until 5 cards, or draw all remaining"""    
        while len(self.hand) < 5:
            try:
                self.draw()
            except:
                break

    def update_turn_state(self) -> None:
        """checks game state at the end of the turn. uses 'win', 'last', 'dead', 'continue'"""
        if self.is_win():
            self.turn_state = 'win'
        elif self.is_dead() or self.turn_state == 'last':
            self.turn_state = 'dead'
        else:
            self.turn_state = 'continue'

    def check_last_turn(self) -> bool:
        """checks if it is last turn, flags "last" on self.turnstate"""
        if self.is_dead():
            self.turn_state = 'last'
        return self.is_dead()

    def any_cards_left(self) -> bool:
        '''returns True if there are any cards left in hand'''
        for card in self.hand:
            if card.usable:
                return True
        return False
    
    def cards_left(self) -> int:
        """Returns number of cards left in the deck"""
        return len(self.temp_deck)

    def debug_print(self, deck):
        """Prints cards in hand or temp_deck"""
        for i in deck:
            print(i)

    # buy phase functions
    def buy_card(self, index: int) -> None:
        """Checks if player successfully buys card. Adds card to mainDeck if possible. buying dupes is not allowed"""
        card: Card = self.shop_choices[index]
        assert card.cost <= self.cargo, "insufficient funds!"
        self.cargo -= card.cost
        self.main_deck.append(card._copy())
        self.shop_choices[index].void()
        print(f"{card.alt_str()} added to deck!")

    def populate_shop(self) -> None:
        """fills shop with items based on how much cargo player has"""
        all_cards: list[Card] = load_dan_cards_csv("Card Data.csv")
        # pulls all cards that cost less that self.cargo
        if self.cargo != 0:
            possible_cards: list[Card] = list(filter(lambda x: x.cost <= self.cargo, all_cards))
            # cheaper cards are more likely to be drawn, caps at 5 times the odds of most expensive card.
            draw_odds: list[int] = [min([self.cargo - card.cost + 1, 5]) for card in possible_cards]
        else:
            # if cargo = 0, just generate any cards
            possible_cards = all_cards
            draw_odds = [1 for _ in range(len(possible_cards))]

        self.shop_choices: list[Card] = choices(possible_cards, weights=draw_odds , k=5)
        
        # make choices unique in id()
        self.shop_choices: list[Card] = [card._copy() for card in self.shop_choices]

    def next_level(self, reward: int) -> None:
        """generates a new level"""
        self.shop_choices.clear()
        self.update_cargo(reward)
        self.level += 1

        # new objective is a math function that takes the current value and level 
        # and generates a numerical difference in the + or - direction. target is never negative for now.

        base_modifier: int = self.level*self.difficulty
        random_modifier: int = randint(0, base_modifier//2)

        modify_objective: int = base_modifier + random_modifier

        is_increase: bool = choice([True, False]) or modify_objective > self.objective_number

        if is_increase:
            self.objective_number += modify_objective
        else:
            self.objective_number -= modify_objective

    

############################################# BUTTON INPUTS ##########################################
def turn_start(player:Player):
    """called when turn starts"""
    player.draw_hand()
    if player.check_last_turn():
        # tkinter.messagebox
        messagebox.showinfo("Warning", "This is your final turn!")
        print("This is your final turn!")
        print("-"*15)

def start_level(player: Player):
    """called when each level starts"""
    player.reset_deck()
    player.to_game()
    turn_start(player)

def main_play_button():
    """called on the menu to start the game"""
    player = create_player()
    start_level(player)
    return player

def card_button(player: Player, button_index: int):
    """called when card button is clicked in play phase"""
    try:
        player.play_card(button_index)
    except:
        messagebox.showinfo("Invalid!", "you already played this card.")
    if player.is_win():
        # tkinter.messagebox
        messagebox.showinfo('Level Clear!', 'End your turn to proceed to the card shop.')
        print("-"*15)
        print("you win! end your turn to proceed to shop.")
    
def next_turn_button(player: Player):
    """called when next turn is clicked"""
    player.end_turn()

    if player.turn_state == "win":
        player.populate_shop()
        player.to_shop()
    elif player.turn_state == "dead":
        player.turn_state = "dead"
        player.to_deathscreen()
    else:
        turn_start(player)

def buy_button(player: Player, button_index: int):
    """called when card is clicked in shop phase"""
    try:
        player.buy_card(button_index)
    except:
        # tkinter.messagebox
        messagebox.showinfo("Insufficient Cargo!", "This card is too expensive!")
        print("Card is too expensive!")

def done_shopping(player: Player):
    """called when player is done shopping"""
    player.next_level(reward= 10)
    start_level(player)

def sim_input(player: Player) -> int:
    '''simulated button clicks, accepts 0, 1, 2, 3, 4, -1, 'quit' '''
    while True:
        play_input = input("enter: ")
        if not play_input in ['0','1','2','3','4', '-1', 'quit']:
            print("invalid input")
            continue

        if play_input == '-1':
            return -1

        if play_input == 'quit':
            return 5
        
        return int(play_input)

        


def main_adp():
    player = None
    start = True
    home_screen_cmd()
    while True:
        root = tk.Tk()
        root.withdraw()
        choice = sim_input(player)
        if start:
            player:Player = main_play_button()
            render_turn(player)
            render_hand(player)
            start = False
        elif choice == 5:
            render_death(player)
            print("quitting...")
            del player
            return
        elif player.is_game():
            if choice == -1:
                render_end_turn()
                next_turn_button(player)

                ## GRAPHICS
                if player.is_game():
                    render_turn(player)
                    render_hand(player)
                elif player.is_shop():
                    render_end_game_report(player)
                    render_shop(player)
                elif player.turn_state == "dead":
                    render_death(player)
                    del player
                    return
                ## ---------
            else:
                card_button(player, choice)
                render_hand(player)
        elif player.is_shop():
            if choice == -1 :
                done_shopping(player)
                render_shop_exit(player)
                render_turn(player)
                render_hand(player)
            else:
                buy_button(player, choice)
                render_shop(player)


def play_phase(player: Player) -> Player:
    """Play Phase logic"""
    player.reset_deck()
    while True:
        turn_running = True
        player.draw_hand()

        if player.is_dead():
            last_turn = True
            print("This is your final turn!")
            print("-"*15)
        else:
            last_turn = False

        render_turn(player,turn)
        #card play loop
        while turn_running:
            render_hand(player)
            player_choice = get_player_action(player)
            
            if player_choice == -1:
                render_end_turn()
                turn_running = False
            else:
                player.play_card(player_choice) 
                # end turn if no cards left
                if all([not card.usable for card in player.hand]):
                    render_end_turn()
                    turn_running = False
        
        #end turn, check for win
        player.end_turn()
        
        if player.turn_state == "win":
            render_end_game_report(player)
            break
        elif player.turn_state == "dead" or last_turn:
            player.turn_state = "dead"
            render_death(player)
            break

    return player

def shop_phase(player: Player) -> Player:
    """shop menu operation"""
    # when shop is called, populate shop
    player.populate_shop()
    shopping = True
    while shopping:
        render_shop(player)
        # get input
        player_choice = get_shop_action(player)
        print("-"*15)
        # buy card
        if player_choice == -1:
            shopping = False
        else:
            try:
                player.buy_card(player_choice)
            except:
                print("Card is too expensive!")
        # terminate loop when done shopping 
    player.next_level(10)
    render_shop_exit(player)
    return player

def home_screen_cmd() -> None:
    """just a lil something for the title card"""
    print("""_   _ ____ _  _ ____    ___  ____ _   _ ____    ____ ____ ____    _  _ _  _ _  _ ___  ____ ____ ____ ___  
 \_/  |  | |  | |__/    |  \ |__|  \_/  [__     |__| |__/ |___    |\ | |  | |\/| |__] |___ |__/ |___ |  \ 
  |   |__| |__| |  \    |__/ |  |   |   ___]    |  | |  \ |___    | \| |__| |  | |__] |___ |  \ |___ |__/ 
                                                                                                         
                   ----- coded by Jean, Daniel, Ee Song, Saif, Siew Hean, Kaelen -----""")
    print("type '0' to start game")

def create_player() -> Player:
    """creates a player with the starting hand"""
    player = Player()
    player.main_deck = load_dan_cards_csv("Starter Deck.csv")
    return player

def main_cmd():
    """Whole game logic here"""
    home_screen_cmd()
    input()
    # game setup here
    player = create_player() 
    while True:
        player = play_phase(player)
        if player.turn_state == "dead":
            break
        player = shop_phase(player)

def load_dan_cards_csv(directory: str) -> list[Card]:
    """
    csv headings: operation,value,cost
    returns a list of card objects
    """
    with open(directory) as f:
        # [1:] to exclude the heading 
        card_info: list[str] = f.read().split()[1:]
        cards = []
        for i in card_info:
            card_operation, card_value, card_cost = tuple(i.split(sep=","))
            if card_cost == '':
                new_card = Card(card_operation, int(card_value))
            else:
                new_card = Card(card_operation, int(card_value), int(card_cost)) 
            cards.append(new_card)
    return cards

def render_hand(player: Player):
    """Prints out all relevant info per card play"""
    print("-"*15)
    print(f" TARGET HEADING: {player.objective_number}")
    print(f"CURRENT HEADING: {player.current_number}")
    print("-"*15)
    # print hand 
    print(f"Hand (playable cards)")
    for i,_ in enumerate(player.hand):
        card:Card = _
        if card.usable:
            print(f"Position {i} : {card.alt_str()}")

def render_shop_exit(player:Player):
    print(f"starting new level... Target: {player.objective_number}. You recieve 10 more cargo!")
    print("-"*15)

def render_turn(player: Player):
    """Only runs at the start of each turn"""
    print(f"     LEVEL: {player.level}")
    print(f"      TURN: {player.turn}")
    print(f"     CARGO: {player.cargo}")
    print(f"CARDS LEFT: {player.cards_left()}")

def render_end_turn():
    print("-"*15)
    print("ending turn...")
    print("-"*15)

def render_end_game_report(player: Player):
    """Runs after play phase, before buy phase"""
    print("-"*15)
    print("You have reached the next spaceport!")
    print(f"Turns taken: {player.turn}")
    print(f"Cargo: {player.cargo}")
    print(f"Cards left in deck: {player.cards_left()}")
    print("-"*15)

def render_shop(player: Player):
    """Runs during shop phase"""
    print("-"*15)
    print("<THE SHOP>")
    for i, card in enumerate(player.shop_choices):
        if card.usable:
            print(f"Position {i} {card}")
    print()
    print(f"you have {player.cargo} cargo to spend,")
    print(f"you have {len(player.main_deck)} cards in your deck")

def render_death(player: Player):
    """runs on endgame"""
    print("-"*15)
    print("Game Over")
    print("you have run out of cards!")
    print(f"Level: {player.level}")
    input("press enter to return to main menu")

def get_player_action(player:Player) -> int:
    """Get player action and return card position. -1 to indicate end turn"""
    while True:
        player_action = input("Input the position of card you wish to play. Input -1 to end turn. Input: ")
        if player_action.isdigit() or player_action == "-1":
            player_action = int(player_action)
        else:
            print("Invalid input")
            continue
        try:
            assert player_action < len(player.hand)
        except:
            print("Invalid input")
            continue
        if (player.hand[player_action]).usable or player_action == -1:
            break
        else:
            print("Invalid input")
    return player_action

def get_shop_action(player:Player) -> int:
    """Get player's shop action and return card position. -1 to indicate done shopping"""
    while True:
        player_action = input("Input the position of card you wish to buy. Input -1 to finish shopping and start next level. Input: ")
        if player_action.isdigit() or player_action == "-1":
            player_action = int(player_action)
        else:
            print("Invalid input")
            continue
        try:
            assert player_action < len(player.shop_choices)
        except:
            print("Invalid input")
            continue
        if (player.shop_choices[player_action]).usable or player_action == -1:
            break
        else:
            print("Invalid input")
    return int(player_action)

if __name__ == "__main__":
    main_adp()
