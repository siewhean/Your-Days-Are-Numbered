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
    """Loads the desired font for use in the game screens."""
    
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
root.iconbitmap("assets\icon_black.ico")
root.configure(background='black')
root.state('zoomed') # Maximise Window on Run

###################################################### Variables ######################################################

player:Player = Player()
player.reset_player()

game_screen_deck_box_width = 900
game_screen_deck_box_height = 150
game_screen_font_size_offset = 5
game_screen_cards:list[tk.Button] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]
_game_screen_cards_images:list[tk.PhotoImage] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]

shop_screen_cards_button: list[tk.Button] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]
shop_screen_cards_cost: list[tk.Button] = ["cards_cost_1", "cards_cost_2", "cards_cost_3", "cards_cost_4", "cards_cost_5"]
_shop_screen_cards_images:list[tk.PhotoImage] = ["cards_1", "cards2", "cards_3", "cards_4", "cards_5"]
shop_screen_cards_cost_data: list[int] = [0]*5

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
Title_img = tk.PhotoImage(file= "assets/Title_2.png")

Title = tk.Label(main_menu, image= Title_img, fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(100, 0))
Title.pack(fill='both', expand=True)

################################################## Insert Play Button ##################################################
Play_Button = tk.Button(main_menu, text="PLAY", font=("LoRes 9 Plus OT Wide", 28), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white", width=10,
                        command=lambda: start_game(player))
Play_Button.pack(pady= (50,0))

def start_game(player:Player) -> None:
    """Initiates a new player for a new game."""
    player.start_level()
    initiate_level(player)

##################################################### GAME SCREEN #####################################################

def update_headings(player:Player, new_level:bool = False) -> None:
    """Updates the target and current headings."""

    global Target_Heading, Current_Heading
    head_dict = player.read_headings()
    if new_level:
        Target_Heading.config(text=str(head_dict["target"]))
    Current_Heading.config(text=str(head_dict["current"]))

def update_turn_info(player:Player, new_level:bool = False) -> None:
    """Updates the turn, cargo, level, and cards left."""

    global Level, Turn, Cargo_Left, Cards_Left
    turn_dict = player.read_turn_info()
    if new_level:
        Level.config(text=str(f'LEVEL: {turn_dict["level"]}'))
    Turn.config(text=str(f'TURN: {turn_dict["turn"]}'))
    Cargo_Left.config(text=str(f'CARGO LEFT: {turn_dict["cargo"]}'))
    Cards_Left.config(text=str(f'CARDS LEFT: {turn_dict["cards left"]}'))

def wait_here(duration:int):
    """Stalls the window for `duration` milliseconds."""
    global root
    var = tk.IntVar() # dummy variable
    root.after(duration, lambda: var.set(value=1)) # update dummy variable after duration
    root.wait_variable(var) # wait for dummy variable to update
    del var

def update_hand(player:Player, animate:bool=False) -> None:
    """Updates the filepaths for the cards in hand."""

    global game_screen_cards, Next_Turn, _game_screen_cards_images
    if animate:
        for i in range(len(game_screen_cards)):
            game_screen_cards[i].config(state="disabled", image=card_back)
        Next_Turn.config(state="disable")
        wait_here(450)
        Next_Turn.config(state="normal")
    card_path_str = player.read_hand_filepath()
    for i, string in enumerate(card_path_str):
        _game_screen_cards_images[i] = tk.PhotoImage(file= string)
        game_screen_cards[i].config(image= _game_screen_cards_images[i], state= "normal")

def initiate_level(player:Player) -> None:
    """Updates all values on game start."""

    global Concede, Next_Turn, Pop_up_msg, game_screen, root
    update_turn_info(player, new_level= True)
    update_headings(player, new_level= True)
    update_hand(player)
    Concede.config(state= "normal")
    Next_Turn.config(text= "NEXT TURN")
    Pop_up_msg.config(fg= 'black')
    root.after(50, game_screen.tkraise)

############################################# Insert Target Heading Value #############################################
Target_Heading_Title = tk.Label(game_screen, text='TARGET\nHEADING', font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black",
                                padx=-10)
Target_Heading_Title.pack(pady=(30, 0))

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

Next_Turn = tk.Button(next_button_frame, text="NEXT TURN", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black", width=10, 
                      command=lambda: pass_turn(player))
Next_Turn.grid(row=0, column=0)

def pass_turn(player:Player):
    """Called on clicking next turn. Checks player state upon ending turn."""

    player.end_turn()
    if player.turn_state == "win":
        player.populate_shop()
        initiate_shop(player)
    elif player.turn_state == "dead":
        player.turn_state = "dead"
        initiate_death(player)
    else:
        player.draw_hand()
        if player.check_last_turn():
            show_pop_up("FINAL TURN")
        update_hand(player, animate=True)
        update_turn_info(player)
        
################################################### Create Deck Box ###################################################
deck_box = tk.Canvas(game_screen, width=game_screen_deck_box_width, height=game_screen_deck_box_height, bd=30, bg='black')
deck_box.pack(pady=(10, 0))

deck_button_frame = tk.Frame(deck_box, highlightthickness=5, highlightbackground="white")
deck_button_frame.configure(bg="black")
deck_button_frame.grid(row=0, column=0, sticky="ew")
deck_button_frame.grid_columnconfigure(0, minsize=110)
deck_button_frame.grid_columnconfigure(2, minsize=110)

card_anchor:tk.Frame = tk.Frame(deck_button_frame, bg= "black")
card_anchor.grid(row=0, column=1, sticky="ew")

#################################################### Create Buttons ####################################################
card_back = tk.PhotoImage(file= "assets/Cards/back.png")

def on_card_play(player:Player, index:int) -> None:
    """
    Called on card click. Disables card to prevent card from being played twice.
    Checks for win condition after card is played.
    """

    global Concede, Next_Turn, game_screen_cards
    player.play_card(index)
    game_screen_cards[index].config(state="disabled", image=card_back)
    update_headings(player)
    if player.is_win():
        for i in range(len(game_screen_cards)):
            game_screen_cards[i].config(state= "disabled")
        Concede.config(state= "disabled")
        Next_Turn.config(text= "TO SHOP >")
        show_pop_up("LEVEL CLEAR!")

card_play_dict:dict = {
    0: lambda: on_card_play(player, 0),
    1: lambda: on_card_play(player, 1),
    2: lambda: on_card_play(player, 2),
    3: lambda: on_card_play(player, 3),
    4: lambda: on_card_play(player, 4)
}

for i in range(len(game_screen_cards)):
    game_screen_cards[i] = tk.Button(card_anchor, image= card_back, width=125, height=175, borderwidth=0, bg='black',
                        activebackground= "black", command = card_play_dict[i])
    game_screen_cards[i].grid(row=0, column=i, padx=10, pady=15)


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

################################################ Insert Win Message ################################################
Pop_up_msg = tk.Label(game_screen, text="", font=("LoRes 9 Plus OT Wide", 20), fg="black", bg="black")
Pop_up_msg.pack()

def show_pop_up(msg:str):
    """Sets and blinks the pop-up message."""

    global Pop_up_msg, root
    Pop_up_msg.config(fg="black", text= msg)
    blink_pop_up(7)

def blink_pop_up(times:int) -> None:
    """Helper functiont to blink the pop-up message."""

    global Pop_up_msg, root
    if times <= 0:
        Pop_up_msg.config(fg= "white")
    else:
        current_color = Pop_up_msg.cget("fg")
        next_color = "black" if current_color == "white" else "white"
        Pop_up_msg.config(fg=next_color)
        root.after(120, lambda: blink_pop_up(times - 1))

######################################################### SHOP #########################################################
def initiate_shop(player:Player) -> None:
    """Called when shop is opened. Fill the shop with cards and other UI elements."""

    global _shop_screen_cards_images, shop_screen_cards_button, shop_screen_cards_cost_data
    global shop_screen_cards_cost, root, shop_screen
    shop_dict = player.read_shop_info()

    # shop is already populated by next turn button
    card_path_str = shop_dict["choices"] # get paths for shop cards
    card_costs = shop_dict["costs"]
    for i, string in enumerate(card_path_str):
        _shop_screen_cards_images[i] = tk.PhotoImage(file= string)
        shop_screen_cards_button[i].config(image= _shop_screen_cards_images[i], state= "normal")
        shop_screen_cards_cost_data[i] = card_costs[i]
        shop_screen_cards_cost[i].config(text= f"COST:{card_costs[i]}")
    
    random_planet_message()
    update_cargo(player)
    update_deck_contents(player)
    root.after(50, shop_screen.tkraise)

def update_cargo(player:Player)-> None:
    """Called to update player cargo."""

    global Shop_cargo_left
    Shop_cargo_left.config(text= f"CARGO LEFT: {player.cargo}")

def update_deck_contents(player:Player) -> None:
    """Called to update the deck contents."""

    global Txt_deck
    Txt_deck.config(text= f"YOUR DECK CONTAINS:\n{player.read_deck_qty()}")
    update_buyable(player)

def update_buyable(player:Player) -> None:
    """Called to update card clickability in the shop."""

    global shop_screen_cards_cost_data, shop_screen_cards_button
    for i, cost in enumerate(shop_screen_cards_cost_data):
        if cost > player.cargo:
            shop_screen_cards_button[i].config(state="disabled")

############################################### Create Planet Message ##################################################

def random_planet_message():
    """Create a random planet name for buy phase UI."""

    global Planet_message
    systems:list[str] = ['jenso', 'danel', 'eeso', 'saiza', 'sewhen', 'kael', 'tellar', 'nimbus', 'altair', 'alderaan',
                         'coruscant', 'xaryxia', 'bespin', 'gallifrey', 'mondas', 'arrakis', 'krypton', 'xandar',
                         'vulcan', 'andromeda', 'artemis-tau']
    random_planet:str = random.choice(systems) + "-" + str(random.choice(range(1,100)))
    Planet_message.config(text= f"YOU HAVE REACHED {random_planet.upper()}")

Planet_message = tk.Label(shop_screen, text="YOU HAVE REACHED THE NEXT PLANET!", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                 padx=-10)
Planet_message.pack(pady=(25,0))

################################################### Create Deck Box ###################################################
shop_deck_box = tk.Canvas(shop_screen, width=900, height= 180, bd=30, bg='black', highlightthickness=5,
                     highlightbackground="white")
shop_deck_box.pack(pady=(15,10))

shop_button_frame = tk.Frame(shop_deck_box, highlightthickness=5, highlightbackground="white")
shop_button_frame.configure(bg="black")
shop_button_frame.grid(row=0, column=0, sticky="ew")
shop_button_frame.grid_columnconfigure(0, minsize=110)
shop_button_frame.grid_columnconfigure(2, minsize=110)

shop_header = tk.Label(shop_button_frame, text="THE CARD SHOP", font=("LoRes 9 Plus OT Wide", 20), fg="white", bg="black")
shop_header.grid(row=0, column=1, pady=(5,0))

shop_card_anchor:tk.Frame = tk.Frame(shop_button_frame, bg= "black")
shop_card_anchor.grid(row=1, column=1, sticky="ew")

#################################################### Create Buttons ####################################################
description_button_frame = tk.Frame(shop_screen)
description_button_frame.configure(bg="black")
description_button_frame.pack()

description_button_frame.grid_rowconfigure(2, minsize= 125)

def on_card_buy(player:Player, index:int) -> None:
    """Called when card is bought."""

    global shop_screen_cards_button
    try:
        player.buy_card(index)
    except:
        # tkinter.messagebox (safety net)
        messagebox.showerror("Insufficient Cargo!", "This card is too expensive!")
        return
    shop_screen_cards_button[index].config(state="disabled", image=card_back)
    update_buyable(player)
    update_cargo(player)
    update_deck_contents(player)

card_buy_dict:dict = {
    0: lambda: on_card_buy(player, 0),
    1: lambda: on_card_buy(player, 1),
    2: lambda: on_card_buy(player, 2),
    3: lambda: on_card_buy(player, 3),
    4: lambda: on_card_buy(player, 4)
}

for i in range(len(shop_screen_cards_button)):
    shop_screen_cards_button[i]:tk.Button = tk.Button(shop_card_anchor, image= card_back, width=125, height=175, borderwidth=0, bg='black',
                        activebackground= "black", padx = 8, pady=60, command = card_buy_dict[i])
    shop_screen_cards_button[i].grid(row=0, column=i, padx=10, pady=(10,0))

##################################################### Insert Cost #####################################################
for i in range(5):
    shop_screen_cards_cost[i] = tk.Label(shop_card_anchor, text="COST:" + "0",
                             font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
    shop_screen_cards_cost[i].grid(row=1, column=i, padx=36, pady=10)

################################################## Insert Cargo Value ##################################################
Shop_cargo_left = tk.Label(description_button_frame, text="CARGO LEFT: " + "0",
                      font=("LoRes 9 Plus OT Wide", 16), fg="white", bg="black")
Shop_cargo_left.grid(row=1, column=2, pady=(5,0))

############################################### Insert Deck Quantities #################################################
placeholder_txt_deck:str = "1× [+1]   1× [+2]   1× [+3]   1× [+4]   1× [+5]   1× [+6]   1× [+7]   1× [+8]   1× [+9]"

Txt_deck = tk.Label(description_button_frame, text= placeholder_txt_deck,
                      font=("LoRes 9 Plus OT Wide", 14), fg="#999999", bg="black")
Txt_deck.grid(row=2, column=2, pady=0)

################################################## Insert Next Button ##################################################
Next_Level = tk.Button(shop_screen, text="NEXT LEVEL", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black", width=10, bd="15", highlightbackground="white",
                      command=lambda: end_shopping(player))
Next_Level.pack(pady=(10,0))

def end_shopping(player:Player):
    """Called when player has finished shopping. Start next level."""

    player.next_level(reward= 10)
    player.start_level()
    initiate_level(player)

Reward = tk.Label(shop_screen, text="+10 CARGO", font=("LoRes 9 Plus OT Wide", 14), fg="white", bg="black")
Reward.pack(pady=2)

###################################################### END SCREEN ######################################################

def initiate_death(player:Player) -> None:
    """Called upon death. Prepares death message."""

    global Death_message, Level_score, root, end_screen
    Death_message.config(text=random.choice(Death_list))
    Level_score.config(text= f"YOU LOST ON: LEVEL {player.read_level()}")
    root.after(50, end_screen.tkraise)
    player.reset_player()

##################################################### Insert Title #####################################################
Title = tk.Label(end_screen, text='GAME OVER', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(end_screen_y_padding_from_top_window, 0))

##################################################### Insert Level Score ###############################################
Level_score = tk.Label(end_screen, text=F"YOU LOST ON: LEVEL", font=("LoRes 9 Plus OT Wide", 15), fg="white", bg="black",
                 padx=-10)
Level_score.pack(pady=0)

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

Main_Menu_Button = tk.Button(button_frame, text="Try Again?".upper(), font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white",
                        command=lambda: initiate_main())
Main_Menu_Button.grid(row=1, column=0, padx=50)

def initiate_main():
    """Called upon pressing try again button. Back to main menu after death."""
    global root, main_menu
    root.after(50, main_menu.tkraise)

################################################## Boot Up Game ########################################################

initiate_main()
root.mainloop()