from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

# from main import Player
# from main import main_cmd
import main
from GUI import main_menu

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


font = loadfont("GUI/LoRes.ttf")
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
    main.player.end_turn()

    if main.player.turn_state == "win":
        main.render_end_game_report(main.player, main.turn)
    elif main.player.turn_state == "dead" or main.last_turn:
        main.player.turn_state = "dead"
        main.render_death(main.player)
    else:
        main.turn += 1
        main.player.cargo -= 1
    return main.player

def home():
    root.destroy()
    from GUI import main_menu

def show_frame(frame):
    frame.tkraise


############################################### Insert Background Image ###############################################
# bg = tk.PhotoImage(file="GUI/compass.png")
# # Create a Label
# my_label = tk.Label(root, image=bg)
# my_label.place(x=0, y=0, relwidth=1, relheight=1)

###################################################### Variables ######################################################
game_screen_y_padding_from_top_window = 0
game_screen_deck_box_height = 150
game_screen_deck_box_width = 900
game_screen_font_size_offset = 5
game_screen_home_button_height = 50
game_screen_home_button_y_offset = 10
game_screen_card_padx = 8
game_screen_cards = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]

main_menu = tk.Frame(root)
game_screen = tk.Frame(root)
shop_screen = tk.Frame(root)

################################################ Create Class for Cards ################################################
class Cards:
    def __init__(self, index, state, value):
        self.index = index
        self.state = state
        self.value = value

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


for i, _ in enumerate(main.player.hand):
    card: main.Card = _
    print("card.alt_str(): " + card.alt_str())
    if card.usable:
        print("card.alt_str(): " + card.alt_str())
        game_screen_cards[i] = Cards(i, "normal", card.alt_str())
    # cards[i].generate_buttons(i, root)

################################################## Insert Home Button ##################################################
home_button_frame = tk.Frame(game_screen)
home_button_frame.configure(bg="black")
home_button_frame.pack()

# download_icon = tk.PhotoImage(file='home_icon.png')
download_icon = tk.PhotoImage(file='GUI/home_icon.png')
Home = tk.Button(home_button_frame, image=download_icon, command=home)
Home.grid(row=0, column=0, padx=(0, 1000), pady=game_screen_home_button_y_offset)

############################################# Insert Target Heading Value #############################################
Target_Heading_Title = tk.Label(game_screen, text='TARGET\nHEADING', font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                                padx=-10)
Target_Heading_Title.pack(pady=(game_screen_y_padding_from_top_window, 0))
Target_Heading = tk.Label(root, text=main.player.objective_number, font=("LoRes 9 Plus OT Wide", 35 + game_screen_font_size_offset),
                          fg="white",
                          bg="black")
Target_Heading.pack()

############################################# Insert Current Heading Value #############################################
Current_Heading_Title = tk.Label(game_screen, text='CURRENT\nHEADING', font=("LoRes 9 Plus OT Wide", 18), fg="white",
                                 bg="black", padx=-10)
Current_Heading_Title.pack()
Current_Heading = tk.Label(game_screen, text=main.player.current_number, font=("LoRes 9 Plus OT Wide", 40 + game_screen_font_size_offset),
                           fg="white",
                           bg="black")
Current_Heading.pack()

################################################# Insert Descriptions ##################################################
description_button_frame = tk.Frame(game_screen)
description_button_frame.configure(bg="black")
description_button_frame.pack()

Turn = tk.Label(description_button_frame, text="TURN " + str(main.turn), font=("LoRes 9 Plus OT Wide", 14), fg="white",
                bg="black")
Turn.grid(row=0, column=0, padx=(0, (game_screen_deck_box_width/5)-15), pady=(30, 0))

Cargo_Left = tk.Label(description_button_frame, text="CARGO LEFT: " + str(main.player.cargo), font=("LoRes 9 Plus OT Wide", 14),
                      fg="white", bg="black")
Cargo_Left.grid(row=0, column=1, padx=(0, game_screen_deck_box_width/5-15), pady=(30, 0))

Level = tk.Label(description_button_frame, text="LEVEL: " + str(main.player.level), font=("LoRes 9 Plus OT Wide", 14),
                      fg="white", bg="black")
Level.grid(row=0, column=2, padx=(0, game_screen_deck_box_width/5-15), pady=(30, 0))

################################################## Insert Next Button ##################################################
next_button_frame = tk.Frame(description_button_frame)
next_button_frame.grid(row=0, column=3)

Next_Turn = tk.Button(next_button_frame, text="NEXT TURN", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                      command=lambda: show_frame(shop_screen))
Next_Turn.grid(row=0, column=0)

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(game_screen, width=game_screen_deck_box_width, height=game_screen_deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.place(x=200,
               y=520 - game_screen_deck_box_height + game_screen_y_padding_from_top_window + (2 * game_screen_font_size_offset) + game_screen_home_button_height + (
                           3 * game_screen_home_button_y_offset))

deck_button_frame = tk.Frame(game_screen)
deck_button_frame.configure(bg="black")
deck_button_frame.place(x=260 + (game_screen_card_padx * 5),
                        y=390 + game_screen_y_padding_from_top_window + (2 * game_screen_font_size_offset) + game_screen_home_button_height + (
                                    3 * game_screen_home_button_y_offset))

#################################################### Create Buttons ####################################################
game_screen_cards[0] = tk.Button(deck_button_frame, text=main.Card.alt_str(), font=("LoRes 9 Plus OT Wide", 18), padx=game_screen_card_padx,
                     pady=60,
                     command=lambda: clicked(game_screen_cards[0], 1))
game_screen_cards[0].grid(row=0, column=0, padx=10)

game_screen_cards[1] = tk.Button(deck_button_frame, text="Card 2", font=("LoRes 9 Plus OT Wide", 18), padx=game_screen_card_padx, pady=60,
                     command=lambda: clicked(game_screen_cards[1], 2))
game_screen_cards[1].grid(row=0, column=1, padx=10)

game_screen_cards[2] = tk.Button(deck_button_frame, text="Card 3", font=("LoRes 9 Plus OT Wide", 18), padx=game_screen_card_padx, pady=60,
                     command=lambda: clicked(game_screen_cards[2], 3))
game_screen_cards[2].grid(row=0, column=2, padx=10)

game_screen_cards[3] = tk.Button(deck_button_frame, text="Card 4", font=("LoRes 9 Plus OT Wide", 18), padx=game_screen_card_padx, pady=60,
                     command=lambda: clicked(game_screen_cards[3], 4))
game_screen_cards[3].grid(row=0, column=3, padx=10)

game_screen_cards[4] = tk.Button(deck_button_frame, text="Card 5", font=("LoRes 9 Plus OT Wide", 18), padx=game_screen_card_padx, pady=60,
                     command=lambda: clicked(game_screen_cards[4], 5))
game_screen_cards[4].grid(row=0, column=4, padx=10)

###################################################### Variables ######################################################
main_menu_y_padding_from_top_window = 100
main_menu_deck_box_height = 150
main_menu_font_size_offset = 5
main_menu_back_button_height = 50
main_menu_back_button_y_offset = 10

##################################################### Insert Title #####################################################
Title = tk.Label(main_menu, text='YOUR DAYS ARE\nNUMBERED', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(main_menu_y_padding_from_top_window, 0))
Title.pack()

################################################## Insert Play Button ##################################################
button_frame = tk.Frame(main_menu)
button_frame.configure(bg="black")
button_frame.pack(pady=100)

Play_Button = tk.Button(button_frame, text="PLAY", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white",
                        command=lambda: show_frame(game_screen))
Play_Button.grid(row=0, column=0, padx=50)

root.mainloop()
