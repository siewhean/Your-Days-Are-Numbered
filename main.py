"""
Your days are numbered
This is a rogue-like deck builder that aims to teach people basic python operators.
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
        "%" : lambda currentValue, cardValue: currentValue %  cardValue
    }

    # generate cost for shop phase
    cost_tiers = {
        "+" : 1, "-" : 1, "*" : 2, "//": 2, "**": 3, "%" : 3
    }

    card_back_path = "assets/Cards/back.png"

    def __init__(self, operation: str, value: int, filepath: str, cost: int = None, ) -> None:
        """
        Card class contain all card logic.
    
        **Args:**

        `operation`: Python operation.

        `value`: An integer value.

        `filepath`: Used to display the image file of the card.

        `cost`: Used only in buy phase. 
        """

        self.operation: str = operation
        self.value: int = value
        self.usable: bool = True

        self._filepath: str = filepath

        # find cost and function
        self.cost: int = self.value*self.cost_tiers[self.operation] if cost == None else cost
        self._function: function = self.operations_table[self.operation]

    def __str__(self) -> str:
        return f"Operation: {self.operation} Value: {self.value} Cost: {self.cost}"

    def alt_str(self) -> str:
        return f"{self.operation}{self.value}"

    def use(self, currentValue: int) -> int:
        """Returns new current value after card is played."""
        self.void()
        return self._function(currentValue, self.value)

    def void(self):
        """Makes card unselectable in shop phase."""
        self.usable = False

    def _copy(self) -> Card:
        """Returns a duplicate of the card."""
        return Card(self.operation, self.value, self.get_filepath(), self.cost)

    def get_filepath(self) -> str:
        return self._filepath

class Player:
    def __init__(self) -> None:
        """All game variables are defined here. Handles player input."""

        ## Game Variables
        self.main_deck: list[Card] = []
        # create a copy of mainDeck to play
        self.temp_deck: list[Card] = []

        self.hand: list[Card] = []
        self.hand_size = 5

        self.cargo: int = 10
        self.current_number: int = 0
        self.target_number: int = 10
        self.difficulty: int = 8

        self.turn_state: str = 'continue'
        self.level: int = 1
        self.turn: int = 1

        ## Shop Variables
        self.shop_choices: list[Card] = []
        self.shop_size: int = 5

    # play phase functions
    def reset_player(self) -> None:
        """Resets the player at the start of the game."""

        self.main_deck = load_dan_cards_csv("Starter Deck.csv")
        self.temp_deck: list[Card] = []

        self.hand: list[Card] = []
        self.hand_size = 5

        self.cargo: int = 10
        self.current_number: int = 0
        self.target_number: int = 10
        self.difficulty: int = 8

        self.turn_state: str = 'continue'
        self.level: int = 1
        self.turn: int = 1

        self.shop_choices: list[Card] = []
        self.shop_size: int = 5

    def create_temp_deck(self) -> None:
        """Makes copies of all cards from `main_deck` and put them into `temp_deck`."""

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

    def draw_hand(self) -> None:
        """Draw until 5 cards, or draw all remaining cards."""

        while len(self.hand) < 5:
            try:
                self.draw()
            except:
                break

    def start_level(self):
        """Called when each level starts."""
        self.reset_deck()
        self.draw_hand()

    def play_card(self, position: int) -> None:
        """Checks if card is usable, then plays the card and update current number."""

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
        return self.current_number == self.target_number

    def is_dead(self) -> bool:
        """Checks if player is out of cards."""
        return 0 == self.cards_left()

    def end_turn(self) -> None:
        """Call end of turn actions. If last turn, draw remaining."""
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

    def update_turn_state(self) -> None:
        """
        Checks game state at the end of the turn. 
        Possible game states: `'win'`, `'last'`, `'dead'`, `'continue'`
        """

        if self.is_win():
            self.turn_state = 'win'
        elif self.is_dead() or self.turn_state == 'last':
            self.turn_state = 'dead'
        else:
            self.turn_state = 'continue'

    def check_last_turn(self) -> bool:
        """
        Checks if it is last turn, sets `turn_state` to `'last'`. 
        Check if player is dead.
        """

        if self.is_dead():
            self.turn_state = 'last'
        return self.is_dead()

    def any_cards_left(self) -> bool:
        """Returns `True` if there are any cards left in hand."""

        for card in self.hand:
            if card.usable:
                return True
        return False

    def cards_left(self) -> int:
        """Returns number of cards left in the deck."""
        return len(self.temp_deck)

    def debug_print(self, deck):
        """Prints cards in hand or temp_deck."""
        for i in deck:
            print(i)

    # buy phase functions
    def buy_card(self, index: int) -> None:
        """Checks if player successfully buys card. 
        Adds card to `main_deck` if possible. buying duplicates are not allowed."""

        card: Card = self.shop_choices[index]
        assert card.cost <= self.cargo, "insufficient funds!"
        self.cargo -= card.cost
        self.main_deck.append(card._copy())
        self.shop_choices[index].void()

    def populate_shop(self) -> None:
        """Fills shop with items based on how much cargo player has."""

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

        # make choices unique in memory, not aliases
        self.shop_choices: list[Card] = [card._copy() for card in self.shop_choices]

    def next_level(self, reward: int) -> None:
        """Generates a new level. Randomly generate next level objective."""

        self.shop_choices.clear()
        self.update_cargo(reward)
        self.level += 1

        # new objective is a math function that takes the current value and level
        # and generates a numerical difference in the + or - direction. target is never negative for now.

        base_modifier: int = self.level*self.difficulty
        random_modifier: int = randint(0, base_modifier//2)

        modify_objective: int = base_modifier + random_modifier

        is_increase: bool = choice([True, False]) or modify_objective > self.target_number

        if is_increase:
            self.target_number += modify_objective
        else:
            self.target_number -= modify_objective

    ########################## READING FUNCTIONS ##########################

    def read_headings(self) -> dict:
        """Returns the target and current numbers."""

        return {
            "target" : self.target_number,
            "current": self.current_number
        }

    def read_hand_filepath(self) -> list[str]:
        """Returns the filepath of cards in hand of the player."""

        return [card.get_filepath() for card in self.hand]

    def read_turn_info(self) -> dict:
        """Returns the level, turn, cargo, and cards left in `temp_deck`."""

        return {
            "level"     : self.level,
            "turn"      : self.turn,
            "cargo"     : self.cargo,
            "cards left": len(self.temp_deck)
        }

    def read_shop_info(self) -> dict:
        """Returns the shop choices, cargo, and cards in `main_deck`."""

        return {
            "choices"    : [card.get_filepath() for card in self.shop_choices],
            "costs"      : [card.cost for card in self.shop_choices],
            "cargo"      : self.cargo,
            "deck length": len(self.main_deck)
        }

    def read_level(self) -> int:
        """Called on death to read the level of death."""

        return self.level

    def read_deck_qty(self) -> str:
        """Returns a string showing the cards in the maindeck sorted by operation and value, divided into quantity."""

        card_dict: dict = {
            '+1': 0, '+2': 0, '+3': 0, '+4': 0, '+5': 0, '+6': 0, '+7': 0, '+8': 0, '+9': 0,
            '-1': 0, '-2': 0, '-3': 0, '-4': 0, '-5': 0, '-6': 0, '-7': 0, '-8': 0, '-9': 0,
            '*2': 0, '*3': 0, '*4': 0, '*5': 0,
            '//2': 0, '//3': 0, '//4': 0, '//5': 0,
            '**2': 0, '**3': 0,
            '%10': 0, '%50': 0, '%100': 0
        }
        deck_str = [card.alt_str() for card in self.main_deck]
        for alt_str in deck_str:
            card_dict[alt_str] += 1
        
        maindeck_str_ls: list[str] = [f"{v}× [{k}]" for k,v in card_dict.items() if v != 0]
        length = 9
        maindeck_str_split_ls = [(' '*5).join(maindeck_str_ls[i:i+length]) for i in range(0,len(maindeck_str_ls), length)]
        maindeck_str = '\n'.join(maindeck_str_split_ls)
        return maindeck_str

############################################# BUTTON INPUTS ##########################################

def load_dan_cards_csv(directory: str) -> list[Card]:
    """
    csv headings: operation,value,cost,filepath
    
    **Args:**

    `directory`: Path to csv file.

    **Returns:**
    
    A list of card objects.
    """
    with open(directory) as f:
        # [1:] to exclude the heading
        card_info: list[str] = f.read().split()[1:]
        cards = []
        for i in card_info:
            card_operation, card_value, card_cost, filepath = tuple(i.split(sep=","))
            if card_cost == '':
                new_card = Card(card_operation, int(card_value), filepath=filepath)
            else:
                new_card = Card(card_operation, int(card_value), filepath=filepath, cost= int(card_cost))
            cards.append(new_card)
    return cards
