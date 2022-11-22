from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
import tkinter as tk


###################################################### Variables ######################################################
y_padding_from_top_window = 0
deck_box_height = 200
font_size_offset = 5
back_button_height = 50
back_button_y_offset = 10
card_padx = 8
cards = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]



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

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(root, width=900, height=deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.place(x=200, y=140 - deck_box_height + y_padding_from_top_window + (2 * font_size_offset) + back_button_height + (3 * back_button_y_offset))

deck_button_frame = tk.Frame(root)
deck_button_frame.configure(bg="black")
deck_button_frame.place(x=260 + (card_padx * 5), y=y_padding_from_top_window + (2 * font_size_offset) + back_button_height + (3 * back_button_y_offset))

#################################################### Create Buttons ####################################################
cards[0] = tk.Button(deck_button_frame, text="Card 1", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx, pady=60,
                   command=lambda: clicked(cards[0], 1))
cards[0].grid(row=0, column=0, padx=10)

cards[1] = tk.Button(deck_button_frame, text="Card 2", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx, pady=60,
                    command=lambda: clicked(cards[1], 2))
cards[1].grid(row=0, column=1, padx=10)

cards[2] = tk.Button(deck_button_frame, text="Card 3", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx, pady=60,
                   command=lambda: clicked(cards[2], 3))
cards[2].grid(row=0, column=2, padx=10)

cards[3] = tk.Button(deck_button_frame, text="Card 4", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx, pady=60,
                   command=lambda: clicked(cards[3], 4))
cards[3].grid(row=0, column=3, padx=10)

cards[4] = tk.Button(deck_button_frame, text="Card 5", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx, pady=60,
                   command=lambda: clicked(cards[4], 5))
cards[4].grid(row=0, column=4, padx=10)

################################################## Insert Next Button ##################################################
next_button_frame = tk.Frame(root)
next_button_frame.pack(pady=350)

Next_Turn = tk.Button(next_button_frame, text="NEXT TURN", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                      command=lambda: next_turn(cards))
Next_Turn.grid()

def back():
    root.destroy()
    import main_menu

root.mainloop()