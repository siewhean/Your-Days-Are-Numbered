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

def next():
    root.destroy()
    import game_screen

def shop():
    root.destroy()
    import shop_screen

###################################################### Variables ######################################################
y_padding_from_top_window = 100
deck_box_height = 150
font_size_offset = 5
back_button_height = 50
back_button_y_offset = 10

############################################# Insert Target Heading Value #############################################
Title = tk.Label(root, text='YOUR DAYS ARE\nNUMBERED', font=("LoRes 9 Plus OT Wide", 60), fg="white", bg="black",
                                padx=-10)
Title.pack(pady=(y_padding_from_top_window, 0))
Title.pack()

################################################## Insert Play Button ##################################################
play_button_frame = tk.Frame(root)
play_button_frame.configure(bg="black")
play_button_frame.pack(pady=100)

Play_Button = tk.Button(play_button_frame, text="PLAY", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black", borderwidth=10, highlightbackground="white",
                      command=lambda: next())
Play_Button.grid(row=0, column=0, padx=50)

################################################## Insert Shop Button ##################################################
Shop_Button = tk.Button(play_button_frame, text="SHOP", font=("LoRes 9 Plus OT Wide", 24), fg="white", bg="black", borderwidth=10, highlightbackground="white",
                      command=lambda: shop())
Shop_Button.grid(row=0, column=1, padx=50)


root.mainloop()
