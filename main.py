"""
Your days are numbered

This is a rogue-like deck builder that aims to teach people math. 
"""
from __future__ import annotations
from random import shuffle
from tkinter import *

class Card:
    # class variable here 
    operations_table = {
        "+": lambda currentValue, cardValue: currentValue + cardValue,
        "-": lambda currentValue, cardValue: currentValue - cardValue,
        "*": lambda currentValue, cardValue: currentValue * cardValue,
        "//": lambda currentValue, cardValue: currentValue // cardValue
    }

    def __init__(self, operation: str, value: int, cost: int) -> None:
        """Card objects have a value and operation. Cost is used during buy phase only."""
        #  check if operation is valid (in operations_table.keys)
        self.operation: str = operation
        self.value: int = value
        self.cost: int = cost 

    def __str__(self) -> str:
        return f"Operation: {self.operation} Value: {self.value} Cost: {self.cost}"

    def use(self, currentValue: int) -> int: 
        """Returns new current value after card is played"""
        return self.operations_table[self.operation](currentValue, self.value)

class Player:
    def __init__(self) -> None:
        """Handles player actions"""
        # create a copy of mainDeck to play 
        self.main_deck: list = []
        self.temp_deck: list = []

        self.hand: list = []
        self.hand_size = 5
        self.cargo: int = 0

        self.current_number: int = 0 
        self.objective_number: int = 0

        self.win: bool = False
    
    # play phase functions
    def reset_deck(self) -> None:
        """"""
        self.temp_deck = self.main_deck.copy()
        shuffle(self.temp_deck)
        self.win = False

    def draw(self) -> None:
        """Add cards to your hand. Check lose condition."""
        if len(self.temp_deck) == 0:
            pass # lose 
        card = self.temp_deck.pop()
        self.hand.append(card) 
        
    def play_card(self, position: int) -> None:
        """Player plays a card and update current number. Check win condition."""
        card: Card = self.hand[position]
        self.current_number = card.use(self.current_number)
        self.is_win()
        
    def update_cargo(self, number: int) -> None:
        """Updates cargo, used at the end of turn and during buy phase"""
        self.cargo += number

    def end_turn(self) -> None:
        """Call end of turn actions."""
        self.update_cargo(number = -1)
        while len(self.hand) < 5:
            self.draw() 
    
    def cards_left(self) -> int:
        """Returns number of cards left in the deck"""
        return len(self.temp_deck)

    def is_win(self):
        """Check win condition."""
        self.win = self.current_number == self.objective_number
        return self.win

    # buy phase functions
    def add_to_deck(self, card: Card) -> None:
        """Called when player successfully buys card. Adds card to mainDeck"""
        pass 

    def next_level(self, reward: int, newObjective: int) -> None:
        """"""
        self.cargo += reward
        self.objective_number = newObjective

def main():
    """Whole game logic here"""
    # game setup here 
    # root = Tk()
    player = Player()
    run = False
    turn = 1
    over_bool = False

    player.main_deck = load_cards_csv().copy()
    player.reset_deck()
    player.objective_number = 5

    # turn starts here 
    for _ in range(player.hand_size):
        player.draw() 
    render_turn(player, turn)

    valid_inputs = list(range(-1,player.hand_size))
    # card playing loop
    while True:
        render_hand(player, valid_inputs)
        player_choice = get_player_action(valid_inputs)
        
        if player_choice == -1:
            print("ending turn...")
            break 
        else:
            player.play_card(player_choice) 
            # prevent same card from playing
            valid_inputs.remove(player_choice)

            # end turn if no cards left
            if valid_inputs == [-1]:
                print("ending turn...")
                break 
    # WORK IN PROGRESS HERE 

        

    
    # gameStates: menu, play, buy
    gameState = "play"

    while run:
        if gameState == "menu":
            pass
        elif gameState == "play":
            # draw 5 cards 


            # when card gets clicked, card disappears, number changes 

            # click end turn 

            # all cards get inserted to bottom of deck

            # cargo - 1  

            pass 
        elif gameState == "buy":
            pass 

    # last line here 
    # root.mainloop()

def load_cards_csv() -> list[Card]:
    """
    csv headings: operation,value,cost
    returns a list of card objects
    """
    with open("cards.csv") as f:
        # [1:] to exclude the heading 
        card_info: list[str] = f.read().split()[1:]
        cards = []
        for i in card_info:
            card_operation, card_value, card_cost = tuple(i.split(sep=","))
            new_card = Card(card_operation, int(card_value), int(card_cost)) 
            cards.append(new_card)
    return cards

def render_hand(player: Player, valid_inputs: list[int]):
    """Prints out all relevant info per card play"""
    print("-"*10)
    print(f"Objective number: {player.objective_number}")
    print(f"Current Number: {player.current_number}")
    print("-"*10)

    # print hand 
    print(f"Hand (playable cards)")
    for i in valid_inputs[1:]:
        print(f"Position {i} {player.hand[i]}")

def render_turn(player: Player, turn: int):
    """Only runs at the start of each turn"""
    print(f"Turn: {turn}")
    print(f"Cargo: {player.cargo}")
    print(f"Cards in deck: {player.cards_left()}")

def get_player_action(valid_inputs: list[int]) -> int:
    """Get player action and return card position. -1 to indicate end turn"""
    while True:
        player_action = input("Input the position of card you wish to play. Input -1 to end turn. Input: ")
        if player_action.isdigit() or player_action == "-1":
            player_action = int(player_action)
        else:
            print("Invalid input")
            continue
        if player_action in valid_inputs:
            break
        else:
            print("Invalid input")
    return int(player_action)

if __name__ == "__main__":
    main()
