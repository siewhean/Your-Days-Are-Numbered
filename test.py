from main import Card
from PIL import Image

def new_csv_reader(directory: str) -> list[Card]:
    """
    create card obj that has operator value, cost is optional
    """
    with open(directory) as f:
        # [1:] to exclude the heading 
        card_info: list[str] = f.read().split()[1:]
        cards = []
        for i in card_info:
            card_operation, card_value, card_cost, filepath = tuple(i.split(sep=","))
            if card_cost == '':
                new_card = Card(card_operation, int(card_value), filepath)
            else:
                new_card = Card(card_operation, int(card_value), filepath, int(card_cost)) 
            cards.append(new_card)
        return cards

csv_path = "Starter Deck.csv"
a = new_csv_reader(csv_path)
def hand_filepath(a):
    return [i.get_filepath() for i in a]

print(hand_filepath(a))
# Image.open(a[0].filepath).show()