"""
Your days are numbered

This is a rogue-like deck builder that aims to teach people math. 
"""
from __future__ import annotations
from random import shuffle

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
        self.value: int = value
        self.operation: str = operation
        self.cost: int = cost 

    def __str__(self) -> str:
        return f"Card {self.operation} {self.value}"

    def use(self, currentValue: int) -> int: 
        """Returns new current value after card is played"""
        return self.operations_table[self.operation](currentValue, self.value)

class Player:
    def __init__(self) -> None:
        """Handles player actions"""
        # create a copy of mainDeck to play 
        self.mainDeck: list = []
        self.tempDeck: list = []
        self.hand: list = []
        self.cargo: int = 0
        self.currentNumber: int = 0 
        self.objectiveNumber: int = 0
        self.win: bool = False
    
    # play phase functions
    def resetDeck(self) -> None:
        """"""
        self.tempDeck = self.mainDeck[:] 
        shuffle(self.tempDeck)
        self.win = False

    def draw(self) -> None:
        """Add cards to your hand. Check lose condition."""
        if len(self.tempDeck) == 0:
            pass # lose 
        card = self.tempDeck.pop()
        self.hand.append(card) 
        
    def playCard(self, position: int) -> None:
        """Player plays a card and update current number. Check win condition."""
        card: Card = self.hand[position]
        self.currentNumber = card.use(self.currentNumber)
        
    def updateCargo(self, number: int) -> None:
        """Updates cargo, used at the end of turn and during buy phase"""
        self.cargo += number

    def endTurn(self) -> None:
        """Call end of turn actions."""
        self.updateCargo(number = -1)
        while len(self.hand) < 5:
            self.draw() 
    
    def is_win(self):
        """Check win condition."""
        return self.currentNumber == self.objectiveNumber

    # buy phase functions
    def addToDeck(self, card: Card) -> None:
        """Called when player successfully buys card. Adds card to mainDeck"""
        pass 

    def nextLevel(self, reward: int, newObjective: int) -> None:
        """"""
        self.cargo += reward
        self.objectiveNumber = newObjective

def main():
    """Whole game logic here"""
    # init game variable here 
    # load in the csv file, create card objects here 
    player = Player()

    # mycard = Card(operation="*", value=3, cost=1)
    # print(mycard.use(6))
    # print(Card.operations_table["+"](2,2))

    # start play phase here
    # gui 
    # objective number, current number 
    # five cards 
    # turn 1 

    # TO DO HERE 
    # turn loop here 
    # draw 5 cards 
    # when card gets clicked, card disappears, number changes 
    # click end turn 
    # all cards get inserted to bottom of deck
    # cargo - 1  

    # TO DO HERE
    # start buy phase here 
    # buy phase loop

if __name__ == "__main__":
    main()
