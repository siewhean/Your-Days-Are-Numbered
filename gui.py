from __future__ import annotations
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20
import tkinter as tk
from tkinter import messagebox
import random
from main import *

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
# panel = tk.Label(root, bg="black")
# panel.pack(side="bottom", fill="both", expand="yes")
# Maximise Window on Run
root.state('zoomed')

def create_player():
    root.destroy()
    main_cmd()

def shop():
    root.destroy()

def clicked(cards, index):
    print("Index" + str(index))
    cards.state = 'disabled'
    cards['state'] = 'disabled'

def next_turn(cards):
    for i in range(len(cards)):
        cards[i]['state'] = 'normal'

def level_number():
    number = "placeholder" #INSERT LEVEL NUMBER HERE
    return number

player:Player = None

def show_frame(frame, player):
    if frame == end_screen:
        # reroll death message
        Death_message.config(text=random.choice(Death_list))
        print("deleted player")
        del player
    frame.tkraise()

###################################################### Variables ######################################################
main_menu_y_padding_from_top_window = 100
main_menu_deck_box_height = 150
main_menu_font_size_offset = 5
main_menu_back_button_height = 50
main_menu_back_button_y_offset = 10

game_screen_y_padding_from_top_window = 30
game_screen_deck_box_width = 900
game_screen_deck_box_height = 150
game_screen_font_size_offset = 5
game_screen_home_button_height = 50
game_screen_home_button_y_offset = 10
game_screen_card_padx = 8
game_screen_cards:list[tk.Button] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]

shop_screen_y_padding_from_top_window = 0
shop_screen_deck_box_height = 180
shop_screen_font_size_offset = 5
shop_screen_back_button_height = 50
shop_screen_back_button_y_offset = 10
shop_screen_card_padx = 8
shop_screen_cards_button: list[tk.Button] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]
shop_screen_cards_cost: list[tk.Button] = ["cards_cost_1", "cards_cost_2", "cards_cost_3", "cards_cost_4", "cards_cost_5"]

end_screen_y_padding_from_top_window = 100

############################################## Switching Between Windows ##############################################
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main_menu = tk.Frame(root)
main_menu.configure(background='black')
game_screen = tk.Frame(root)
game_screen.configure(background='black')
shop_screen = tk.Frame(root)
shop_screen.configure(background='black')
end_screen = tk.Frame(root)
end_screen.configure(background='black')

for frame in (main_menu, game_screen, shop_screen, end_screen):
    frame.grid(row=0,column=0,sticky='nsew')

panel = tk.Label(main_menu, bg="black")
panel.pack(side="bottom", fill="both", expand="yes")

###################################################### MAIN MENU ######################################################

##################################################### Insert Title #####################################################
Title = tk.Label(main_menu, text='YOUR DAYS ARE\nNUMBERED', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(main_menu_y_padding_from_top_window, 0))
Title.pack(fill='both', expand=True)

################################################## Insert Play Button ##################################################
Play_Button = tk.Button(main_menu, text="PLAY", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white",
                        command=lambda: start_game())
Play_Button.pack()

def start_game() -> None:
    globals()["player"]:Player = main_play_button()
    print("player created")
    initiate_level(player)

##################################################### GAME SCREEN #####################################################

def update_headings(player:Player, new_level:bool = False) -> None:
    """updates the target and current headings"""
    head_dict = player.read_headings()
    if new_level:
        Target_Heading.config(text=str(head_dict["target"]))
    Current_Heading.config(text=str(head_dict["current"]))

def update_turn_info(player:Player, new_level:bool = False) -> None:
    """updates the turn, cargo, level, and cards left"""
    turn_dict = player.read_turn_info()
    if new_level:
        Level.config(text=str(f'LEVEL: {turn_dict["level"]}'))
    Turn.config(text=str(f'TURN: {turn_dict["turn"]}'))
    Cargo_Left.config(text=str(f'CARGO LEFT: {turn_dict["cargo"]}'))
    Cards_Left.config(text=str(f'CARDS LEFT: {turn_dict["cards left"]}'))

def waithere(duration:int):
    '''stalls the window for <x> milliseconds'''
    var = tk.IntVar()
    root.after(duration, lambda: var.set(value=1))
    print("waiting...")
    root.wait_variable(var)

def update_hand(player:Player, stall:bool=False) -> None:
    '''updates the filepaths for the cards in hand'''
    for i in range(len(game_screen_cards)):
        game_screen_cards[i].config(state="disabled", image=card_back)
    if stall:
        Next_Turn.config(state="disable")
        waithere(450)
        Next_Turn.config(state="normal")
    card_path_str = player.read_hand_filepath()
    print(card_path_str)
    for i, string in enumerate(card_path_str):
        #tkinter only can access global variables
        globals()["_image"+str(i)] = tk.PhotoImage(file= string)
        game_screen_cards[i].config(image= globals()["_image"+str(i)], state= "normal")

def initiate_level(player:Player) -> None:
    """updates all values on game start"""
    update_turn_info(player, new_level= True)
    print("turn info loaded...")
    update_headings(player, new_level= True)
    print("headings loaded...")
    update_hand(player)
    print("hand loaded...")
    game_screen.tkraise()

############################################# Insert Target Heading Value #############################################
Target_Heading_Title = tk.Label(game_screen, text='TARGET\nHEADING', font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                                padx=-10)
Target_Heading_Title.pack(pady=(game_screen_y_padding_from_top_window, 0))
Target_Heading = tk.Label(game_screen, text=str(99), font=("LoRes 9 Plus OT Wide", 40 + game_screen_font_size_offset), fg="white",
                          bg="black")
Target_Heading.pack()

############################################# Insert Current Heading Value #############################################
Current_Heading_Title = tk.Label(game_screen, text='CURRENT\nHEADING', font=("LoRes 9 Plus OT Wide", 18), fg="white",
                                 bg="black", padx=-10)
Current_Heading_Title.pack()
Current_Heading = tk.Label(game_screen, text=str(34), font=("LoRes 9 Plus OT Wide", 45 + game_screen_font_size_offset), fg="white",
                           bg="black")
Current_Heading.pack()

################################################# Insert Descriptions ##################################################
description_button_frame = tk.Frame(game_screen)
description_button_frame.configure(bg="black")
description_button_frame.pack()

Level = tk.Label(description_button_frame, text="LEVEL: 1", font=("LoRes 9 Plus OT Wide", 14),
                      fg="white", bg="black")
Level.grid(row=0, column=0, padx=(0, game_screen_deck_box_width/5-15), pady=(20, 0))

Turn = tk.Label(description_button_frame, text="TURN 1", font=("LoRes 9 Plus OT Wide", 14), fg="white",
                bg="black")
Turn.grid(row=0, column=1, padx=(0, (game_screen_deck_box_width/5)-15), pady=(20, 0))

Cargo_Left = tk.Label(description_button_frame, text="CARGO LEFT: 1", font=("LoRes 9 Plus OT Wide", 14),
                      fg="white", bg="black")
Cargo_Left.grid(row=0, column=2, padx=(0, game_screen_deck_box_width/5-15), pady=(20, 0))

################################################## Insert Next Button ##################################################
next_button_frame = tk.Frame(description_button_frame)
next_button_frame.grid(row=0, column=3)

Next_Turn = tk.Button(next_button_frame, text="NEXT TURN", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                      command=lambda: pass_turn(player))
Next_Turn.grid(row=0, column=0)

def pass_turn(player:Player):
    """called on clicking next turn"""
    next_turn_button(player)
    if player.turn_state == "win":
        initiate_shop(player)
    elif player.turn_state == "dead":
        initiate_death(player)
    else:
        update_hand(player, stall=True)
        update_turn_info(player)

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(game_screen, width=game_screen_deck_box_width, height=game_screen_deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.create_rectangle(0, 0, 200, 140 - shop_screen_deck_box_height + shop_screen_y_padding_from_top_window + (
        2 * shop_screen_font_size_offset) + shop_screen_back_button_height + (3 * shop_screen_back_button_y_offset))
deck_box.pack(pady=(10, 0))

deck_button_frame = tk.Frame(game_screen)
deck_button_frame.configure(bg="black")
deck_button_frame.place(x=260 + (game_screen_card_padx * 5), y=390 + game_screen_y_padding_from_top_window + (3 * game_screen_home_button_y_offset))

#################################################### Create Buttons ####################################################
card_back = tk.PhotoImage(file= "assets/Cards/back.png")

def on_card_play(player:Player, index:int) -> None:
    """called on card click"""
    card_button(player, index)
    game_screen_cards[index].config(state="disabled", image=card_back)
    update_headings(player)
    if player.is_win():
        # tkinter.messagebox
        messagebox.showinfo('Level Clear!', 'End your turn to proceed to the card shop.')
        print("-"*15)
        print("you win! end your turn to proceed to shop.")
    

card_play_dict:dict = {
    0: lambda: on_card_play(player, 0),
    1: lambda: on_card_play(player, 1),
    2: lambda: on_card_play(player, 2),
    3: lambda: on_card_play(player, 3),
    4: lambda: on_card_play(player, 4)
}

# why can't you assign the lambda function input in a for loop? @prof

for i in range(len(game_screen_cards)):
    game_screen_cards[i] = tk.Button(deck_button_frame, image= card_back, width=125, height=175, borderwidth=0, bg='black',
                        activebackground= "black", padx=game_screen_card_padx, pady=60, command = card_play_dict[i])
    game_screen_cards[i].grid(row=0, column=i, padx=10)

################################################ Insert Description 2 #################################################
description_2_button_frame = tk.Frame(game_screen)
description_2_button_frame.configure(bg="black")
description_2_button_frame.pack()

Cards_Left = tk.Label(description_2_button_frame, text="CARDS LEFT: " + str(3), font=("LoRes 9 Plus OT Wide", 14), fg="white",
                bg="black")
Cards_Left.grid(row=0, column=0, padx=(0, game_screen_deck_box_width/2+230))

################################################ Insert Concede Button ################################################
concede_button_frame = tk.Frame(description_2_button_frame)
concede_button_frame.configure(bg="black")
concede_button_frame.grid(row=0, column=1)

Concede = tk.Button(concede_button_frame, text="CONCEDE", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg= "black",
                        command=lambda: initiate_death(player))
Concede.grid(row=0, column=1, pady=(20, 0))

######################################################### SHOP #########################################################

def initiate_shop(player:Player) -> None:
    '''called when shop is opened'''
    shop_dict = player.read_shop_info()

    # shop is already populated by next turn button
    # get paths for shop cards
    card_path_str = shop_dict["choices"]
    card_costs = shop_dict["costs"]
    print(card_path_str)
    for i, string in enumerate(card_path_str):
        #tkinter only can access global variables
        globals()["_shopimage"+str(i)] = tk.PhotoImage(file= string)
        shop_screen_cards_button[i].config(image= globals()["_shopimage"+str(i)], state= "normal")
        shop_screen_cards_cost[i].config(text= f"COST:{card_costs[i]}")
    update_cargo(player)
    shop_screen.tkraise()

def update_cargo(player:Player)-> None:
    '''called to update player cargo'''
    shop_cargo_left.config(text= f"CARGO LEFT: {player.cargo}")
    

################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(shop_screen, width=900, height=shop_screen_deck_box_height, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
deck_box.create_rectangle(0, 0, 200, 140 - shop_screen_deck_box_height + shop_screen_y_padding_from_top_window + (
        2 * shop_screen_font_size_offset) + shop_screen_back_button_height + (3 * shop_screen_back_button_y_offset))
# deck_box.pack(x=200, y=140 - deck_box_height + y_padding_from_top_window + (2 * font_size_offset) + back_button_height + (3 * back_button_y_offset))
deck_box.pack(pady=(60, 10))

shop_button_frame = tk.Frame(shop_screen)
shop_button_frame.configure(bg="black")
shop_button_frame.place(x=260 + (shop_screen_card_padx * 5),
                        y=shop_screen_y_padding_from_top_window + (2 * shop_screen_font_size_offset) + shop_screen_back_button_height + (
                                3 * shop_screen_back_button_y_offset))

#################################################### Create Buttons ####################################################
description_button_frame = tk.Frame(shop_screen)
description_button_frame.configure(bg="black")
description_button_frame.pack()

def on_card_buy(player:Player, index:int) -> None:
    '''called when card is bought'''
    try:
        player.buy_card(index)
    except:
        # tkinter.messagebox
        messagebox.showerror("Insufficient Cargo!", "This card is too expensive!")
        disable = False
        print("Card is too expensive!")
        return
    shop_screen_cards_button[index].config(state="disabled", image=card_back)
    update_cargo(player)

card_buy_dict:dict = {
    0: lambda: on_card_buy(player, 0),
    1: lambda: on_card_buy(player, 1),
    2: lambda: on_card_buy(player, 2),
    3: lambda: on_card_buy(player, 3),
    4: lambda: on_card_buy(player, 4)
}

for i in range(len(shop_screen_cards_button)):
    shop_screen_cards_button[i]:tk.Button = tk.Button(shop_button_frame, image= card_back, width=125, height=175, borderwidth=0, bg='black',
                        activebackground= "black", padx = shop_screen_card_padx, pady=60, command = card_buy_dict[i])
    shop_screen_cards_button[i].grid(row=0, column=i, padx=10)

##################################################### Insert Cost #####################################################
for i in range(5):
    shop_screen_cards_cost[i] = tk.Label(description_button_frame, text="COST:" + "0",
                             font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
    shop_screen_cards_cost[i].grid(row=0, column=i, padx=36)

################################################## Insert Cargo Value ##################################################
shop_cargo_left = tk.Label(description_button_frame, text="CARGO LEFT: " + "0",
                      font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
shop_cargo_left.grid(row=1, column=2, pady=(10,0))

################################################## Insert Next Button ##################################################
Next_Level = tk.Button(shop_screen, text="NEXT LEVEL", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black", width=10, bd="15", highlightbackground="white",
                      command=lambda: end_shopping(player))
Next_Level.pack(pady=100)

def end_shopping(player:Player):
    player.next_level(reward= 10)
    start_level(player)
    initiate_level(player)

###################################################### END SCREEN ######################################################

def initiate_death(player:Player) -> None:
    '''kills you cutely'''
    Death_message.config(text=random.choice(Death_list))
    Level_score.config(text= F"YOU LOST ON: LEVEL {player.read_level()}")
    print("deleted player")
    end_screen.tkraise()
    del player

##################################################### Insert Title #####################################################
Title = tk.Label(end_screen, text='GAME OVER', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(end_screen_y_padding_from_top_window, 0))
Title.pack()

##################################################### Insert Level Score ###############################################
Level_score = tk.Label(end_screen, text=F"YOU LOST ON: LEVEL {level_number()}", font=("LoRes 9 Plus OT Wide", 15), fg="white", bg="black",
                 padx=-10)
Level_score.pack(pady=0)
Level_score.pack()

##################################################### Insert Death Message #############################################
R_A = "That's rough, buddy."
R_B = "Too bad!"
R_C = "Your cabbages! :("
R_D = "This is extremely not stonks."
R_E = "Lousiest gameplay of the year award goes to..."
R_F = "Your co-pilot was not the impostor. Oops."
R_G = "It seems that the Force was not with you."
R_H = "You let a DALEK on board?? Why?????"
R_J = "Should we get out and push?\nOh right, we're in space."
R_K = "You seem to have died. Hmm."
R_L = "This is a certified bruh moment"

Death_list = [R_A, R_B, R_C, R_D, R_E, R_F, R_G, R_H, R_J, R_K, R_L]

Death_message = tk.Label(end_screen, text=random.choice(Death_list), font=("LoRes 9 Plus OT Wide", 30), fg="white", bg="black",
                 padx=-10)
Death_message.pack(pady=35)
Death_message.pack()

################################################## Insert Main Menu Button #############################################
button_frame = tk.Frame(end_screen)
button_frame.configure(bg="black")
button_frame.pack(pady=65)

Main_Menu_Button = tk.Button(button_frame, text="Try Again?", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white",
                        command=lambda: show_frame(main_menu, player))
Main_Menu_Button.grid(row=1, column=0, padx=50)

show_frame(main_menu, player)

root.mainloop()
