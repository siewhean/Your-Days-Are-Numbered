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

def shop():
    root.destroy()
    import shop_screen

def home():
    root.destroy()
    import main_menu

###################################################### Variables ######################################################
y_padding_from_top_window = 100
deck_box_height = 150
font_size_offset = 5
back_button_height = 50
back_button_y_offset = 10

##################################################### Insert Title #####################################################
Title = tk.Label(root, text='GAME OVER', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                 padx=-10)
Title.pack(pady=(y_padding_from_top_window, 0))
Title.pack()

##################################################### Insert Level Score ###############################################

def level_number():
    import main
    number = "placeholder" #INSERT LEVEL NUMBER HERE
    return number

Level_score = tk.Label(root, text=F"YOU LOST ON: Level {level_number()}", font=("LoRes 9 Plus OT Wide", 15), fg="white", bg="black",
                 padx=-10)
Level_score.pack(pady=0)
Level_score.pack()

##################################################### Insert Death Message #############################################

import random
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

Death_message = tk.Label(root, text=random.choice(Death_list), font=("LoRes 9 Plus OT Wide", 30), fg="white", bg="black",
                 padx=-10)
Death_message.pack(pady=35)
Death_message.pack()

################################################## Insert Main Menu Button #############################################
button_frame = tk.Frame(root)
button_frame.configure(bg="black")
button_frame.pack(pady=65)

Main_Menu_Button = tk.Button(button_frame, text="Try Again?", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black",
                        borderwidth=10, highlightbackground="white",
                        command=lambda: home())
Main_Menu_Button.grid(row=1, column=0, padx=50)

root.mainloop()
