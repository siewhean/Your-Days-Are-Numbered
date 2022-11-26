"""
Your days are numbered

This is a rogue-like deck builder that aims to teach people math. 
"""
from __future__ import annotations
from random import shuffle, seed, randint, choice, choices
from tkinter import *

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
        self.usable = False
        return self._function(currentValue, self.value)

    def void_bought(self):
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

        self.level: int = 1

        self.current_number: int = 0 
        self.objective_number: int = 10
        
        self.turn_state: str = 'continue'

        ## Shop Variables
        self.shop_choices: list[Card] = []
        self.shop_size: int = 5
    
    # play phase functions
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
        self.turn_state: str = 'continue'

    def draw(self) -> None:
        """Add cards to your hand. Check lose condition."""
        assert len(self.temp_deck) > 0
        card = self.temp_deck.pop()
        self.hand.append(card) 
        
    def play_card(self, position: int) -> None:
        """Player plays a card and update current number. Check win condition."""
        card: Card = self.hand[position]
        self.current_number = card.use(self.current_number)
        if self.is_win():
            print("-"*15)
            print("you win! end your turn to proceed to shop.")
        
    def update_cargo(self, number: int) -> None:
        """Updates cargo, used at the end of turn and during buy phase"""
        self.cargo += number

    def is_win(self) -> bool:
        """Check win condition."""
        return self.current_number == self.objective_number

    def is_dead(self):
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
        self.update_cargo(number=-1)
        self.update_turn_state()
        
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
        elif self.is_dead():
            self.turn_state = 'dead'
        else:
            self.turn_state = 'continue'
    
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
        self.shop_choices[index].void_bought()
        print(f"{card.alt_str()} added to deck!")

    def populate_shop(self) -> None:
        """fills shop with items based on how much cargo player has"""
        all_cards = load_dan_cards_csv("Card Data.csv")
        # pulls all cards that cost less that self.cargo
        possible_cards = list(filter(lambda x: x.cost <= self.cargo, all_cards))
        # cheaper cards are more likely to be drawn, caps at 5 times the odds of most expensive card.
        draw_odds = [min([self.cargo-i.cost+1, 5]) for i in possible_cards]

        self.shop_choices = choices(possible_cards, weights=draw_odds , k=5)

    def next_level(self, reward: int) -> None:
        """generates a new level"""
        self.shop_choices.clear()
        self.cargo += reward
        self.level += 1

        # new objective is a function that takes the current value and level 
        # and generates a numerical difference in the + or - direction. target is never negative for now.

        _var = 8
        modify_objective = self.level*_var + randint(0, self.level*_var//2)

        if choice([True, False]) or modify_objective > self.objective_number:
            self.objective_number += modify_objective
        else:
            self.objective_number -= modify_objective



def gamestate(player: Player) -> Player:
    turn = 1
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
            render_end_game_report(player, turn)
            break
        elif player.turn_state == "dead" or last_turn:
            player.turn_state = "dead"
            render_death(player)
            break
        else:
            turn += 1
    return player



def shop(player: Player) -> Player:
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
    print(f"starting new level... Target: {player.objective_number}. You recieve 10 more cargo!")
    print("-"*15)
    return player

def home_screen_cmd() -> None:
    """just a lil something for the title card"""
    print("""_   _ ____ _  _ ____    ___  ____ _   _ ____    ____ ____ ____    _  _ _  _ _  _ ___  ____ ____ ____ ___  
 \_/  |  | |  | |__/    |  \ |__|  \_/  [__     |__| |__/ |___    |\ | |  | |\/| |__] |___ |__/ |___ |  \ 
  |   |__| |__| |  \    |__/ |  |   |   ___]    |  | |  \ |___    | \| |__| |  | |__] |___ |  \ |___ |__/ 
                                                                                                         
                   ----- coded by Jean, Daniel, Ee Song, Saif, Siew Hean, Kaelen -----""")
    input("press enter to start game")

def create_player() -> Player:
    """creates a player with the starting hand"""
    player = Player()
    player.main_deck = load_dan_cards_csv("Starter Deck.csv")
    return player

def main_cmd():
    """Whole game logic here"""

    home_screen_cmd()
    # game setup here
    player = create_player() 

    while True:
        player = gamestate(player)
        if player.turn_state == "dead":
            break
        player = shop(player)

    # last line here 

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

def render_turn(player: Player, turn: int):
    """Only runs at the start of each turn"""
    print(f"     LEVEL: {player.level}")
    print(f"      TURN: {turn}")
    print(f"     CARGO: {player.cargo}")
    print(f"CARDS LEFT: {player.cards_left()}")

def render_end_turn():
    print("-"*15)
    print("ending turn...")
    print("-"*15)

def render_end_game_report(player: Player, turn: int):
    """Runs after play phase, before buy phase"""
    print("-"*15)
    print("You have reached the next spaceport!")
    print(f"Turns taken: {turn}")
    print(f"Cargo: {player.cargo}")
    print(f"Cards left in deck: {player.cards_left()}")
    print("-"*15)
    input("press enter to continue")

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
    main_cmd()
