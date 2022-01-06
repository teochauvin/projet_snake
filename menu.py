from tkinter import *
from main import *

bg_color = "dark green"
size_app = "700x400"

def center(toplevel):

    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = size_app.split("x")

    x = screen_width//2 - int(size[0])//2
    y = screen_height//2 - int(size[1])//2
     
    return str(x), str(y)


class Menu :

    def __init__(self) :

        fenetre = Tk()
        fenetre.geometry(size_app)
        x, y = center(fenetre)

        fenetre.geometry(size_app + "+" + x + "+" + y)
        fenetre.title("Snake")
        fenetre.configure(bg = bg_color)

        def fonc(bool):
            fenetre.withdraw()
            train(100)
            jeu_visuel(human = bool)

        Label(fenetre, text='Menu principal', font=("Helvetica", 40), foreground = "White", bg = bg_color).pack(pady = 50)
        Button(fenetre, text = 'Jouer', width=60, height = 2, command = lambda : fonc(True), bg = bg_color).pack(pady = 3)
        Button(fenetre, text = 'Intelligence artificielle', width=60, height = 2, command = lambda : fonc(False), bg = bg_color).pack(pady = 3)
        Button(fenetre, text = 'Quitter', width=60, height = 2, command = fenetre.destroy, bg = bg_color).pack(pady = 3)

        fenetre.mainloop()


if __name__ == "__main__" :
    menu = Menu()