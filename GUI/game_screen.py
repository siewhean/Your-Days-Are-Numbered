from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
import tkinter as tk


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
panel.pack(side="bottom", fill="both", expand="yes")
# Maximise Window on Run
root.state('zoomed')


def clicked(cards, index):
    print("Index" + str(index))
    cards.state = 'disabled'
    cards['state'] = 'disabled'


def next_turn(cards):
    for i in range(len(cards)):
        cards[i]['state'] = 'normal'

def home():
    root.destroy()
    import main_menu

############################################### Insert Background Image ###############################################
# bg = tk.PhotoImage(file="")
# # Create a Label
# my_label = tk.Label(root, image=bg)
# my_label.place(x=0, y=0, relwidth=1, relheight=1)

###################################################### Variables ######################################################
y_padding_from_top_window = 0
deck_box_height = 150
font_size_offset = 5
home_button_height = 50
home_button_y_offset = 10
card_padx = 8
cards = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]

################################################ Create Class for Cards ################################################
class Cards:
    def __init__(self, index, state):
        self.index = index
        self.state = state

    # @staticmethod
    # def generate_buttons(index, root):
    #     deck_button_frame = tk.Frame(root)
    #     deck_button_frame.configure(bg="black")
    #     deck_button_frame.place(x=260 + (card_padx * 5), y=390 + y_padding_from_top_window + (2 * font_size_offset))
    #
    #     cards[index] = tk.Button(deck_button_frame, text="Card 1", font=("LoRes 9 Plus OT Wide", 18), padx=card_padx,
    #                              pady=60,
    #                              command=lambda: clicked(cards[index], 1))
    #     cards[index].grid(row=0, column=0, padx=10)


for i in range(5):
    cards[i] = Cards(i, "normal")
    # cards[i].generate_buttons(i, root)

################################################## Insert Home Button ##################################################
home_button_frame = tk.Frame(root)
home_button_frame.configure(bg="black")
home_button_frame.pack()

download_icon = tk.PhotoImage(file='home_icon.png')
Home = tk.Button(home_button_frame, image=download_icon, command=home)
Home.grid(row=0, column=0, padx=(0, 1000), pady=home_button_y_offset)

############################################# Insert Target Heading Value #############################################
Target_Heading_Title = tk.Label(root, text='TARGET\nHEADING', font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                                padx=-10)
Target_Heading_Title.pack(pady=(y_padding_from_top_window, 0))
Target_Heading = tk.Label(root, text=str(99), font=("LoRes 9 Plus OT Wide", 35 + font_size_offset), fg="white",
                          bg="black")
Target_Heading.pack()

############################################# Insert Current Heading Value #############################################
Current_Heading_Title = tk.Label(root, text='CURRENT\nHEADING', font=("LoRes 9 Plus OT Wide", 18), fg="white",
                                 bg="black", padx=-10)
Current_Heading_Title.pack()
Current_Heading = tk.Label(root, text=str(34), font=("LoRes 9 Plus OT Wide", 40 + font_size_offset), fg="white",
                           bg="black")
Current_Heading.pack()

################################################# Insert Descriptions ##################################################
description_button_frame = tk.Frame(root)
description_button_frame.configure(bg="black")
description_button_frame.pack()

Turn = tk.Label(description_button_frame, text="TURN " + str(3), font=("LoRes 9 Plus OT Wide", 14), fg="white",
                bg="black")
Turn.grid(row=0, column=0, padx=(15, 60), pady=(30, 0))

Cargo_Left = tk.Label(description_button_frame, text="CARGO LEFT: " + str(13), font=("LoRes 9 Plus OT Wide", 14),
                      fg="white", bg="black")
Cargo_Left.grid(row=0, column=1, padx=(250, 270), pady=(30, 0))

################################################## Insert Next Button ##################################################
next_button_frame = tk.Frame(description_button_frame)
next_button_frame.grid(row=0, column=2)

Next_Turn = tk.Button(next_button_frame, text="NEXT TURN", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                      command=lambda: next_turn(cards))
Next_Turn.grid(row=0, column=0)

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(root, width=900, height=deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.place(x=200, y=520 - deck_box_height + y_padding_from_top_window + (2 * font_size_offset) + home_button_height + (3 * home_button_y_offset))

deck_button_frame = tk.Frame(root)
deck_button_frame.configure(bg="black")
deck_button_frame.place(x=260 + (card_padx * 5), y=390 + y_padding_from_top_window + (2 * font_size_offset) + home_button_height + (3 * home_button_y_offset))

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

root.mainloop()
