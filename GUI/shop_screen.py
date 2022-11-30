from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
import tkinter as tk

def game_screen():
    root.destroy()


def clicked(cards, index):
    print("Index" + str(index))
    cards.state = 'disabled'
    cards['state'] = 'disabled'


###################################################### Variables ######################################################
y_padding_from_top_window = 0
deck_box_height = 180
font_size_offset = 5
back_button_height = 50
back_button_y_offset = 10
card_padx = 8
cards_button = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]
cards_cost = ["cards_cost_1", "cards_cost_2", "cards_cost_3", "cards_cost_4", "cards_cost_5"]


##################################################### Import Font #####################################################
def loadfont(fontpath, private=True, enumerable=True):
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA

    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW

    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


font = loadfont("LoRes.ttf")
root = tk.Tk()
root.title("YOUR DAYS ARE NUMBERED")
root.configure(background='black')
panel = tk.Label(root, bg="black")
# panel.pack(side="bottom", fill="both", expand="yes")
# Maximise Window on Run
root.state('zoomed')


class Cards:
    def __init__(self, index, state, cost):
        self.cost = cost
        self.index = index
        self.state = state


for i in range(5):
    cards_button[i] = Cards(i, "normal", "4")

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(root, width=900, height=deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.create_rectangle(0, 0, 200, 140 - deck_box_height + y_padding_from_top_window + (
        2 * font_size_offset) + back_button_height + (3 * back_button_y_offset))
# deck_box.pack(x=200, y=140 - deck_box_height + y_padding_from_top_window + (2 * font_size_offset) + back_button_height + (3 * back_button_y_offset))
deck_box.pack(pady=(60, 10))

deck_button_frame = tk.Frame(root)
deck_button_frame.configure(bg="black")
deck_button_frame.place(x=260 + (card_padx * 5),
                        y=y_padding_from_top_window + (2 * font_size_offset) + back_button_height + (
                                3 * back_button_y_offset))

#################################################### Create Buttons ####################################################
description_button_frame = tk.Frame(root)
description_button_frame.configure(bg="black")
description_button_frame.pack()

cards_button[0] = tk.Button(deck_button_frame, text="Card 1", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
                            pady=60,
                            command=lambda: clicked(cards_button[0], 1))
cards_button[0].grid(row=0, column=0, padx=10)

cards_button[1] = tk.Button(deck_button_frame, text="Card 2", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
                            pady=60,
                            command=lambda: clicked(cards_button[1], 2))
cards_button[1].grid(row=0, column=1, padx=10)

cards_button[2] = tk.Button(deck_button_frame, text="Card 3", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
                            pady=60,
                            command=lambda: clicked(cards_button[2], 3))
cards_button[2].grid(row=0, column=2, padx=10)

cards_button[3] = tk.Button(deck_button_frame, text="Card 4", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
                            pady=60,
                            command=lambda: clicked(cards_button[3], 4))
cards_button[3].grid(row=0, column=3, padx=10)

cards_button[4] = tk.Button(deck_button_frame, text="Card 5", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
                            pady=60,
                            command=lambda: clicked(cards_button[4], 5))
cards_button[4].grid(row=0, column=4, padx=10)

##################################################### Insert Cost #####################################################
for i in range(5):
    cards_cost[i] = tk.Label(description_button_frame, text="COST:" + "4",
                             font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
    cards_cost[i].grid(row=0, column=i, padx=36)

################################################## Insert Cargo Value ##################################################
cargo_left = tk.Label(description_button_frame, text="CARGO LEFT: " + "13",
                      font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
cargo_left.grid(row=1, column=2, pady=(10,0))

################################################## Insert Next Button ##################################################
next_button_frame = tk.Frame(root)
next_button_frame.pack(pady=100)

Next_Turn = tk.Button(next_button_frame, text="NEXT LEVEL", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black", width=10, bd="15", highlightbackground="white",
                      command=lambda: game_screen())
Next_Turn.grid()


def back():
    root.destroy()


root.mainloop()
