# Import customtkinter module
import customtkinter as ctk
import tkinter as tk
import guest
from database import Database


# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("dark")

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")

list_of_names = list(guest.gen_dates())


# window size
appWidth, appHeight = 900, 700


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("900x500")
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.title("Bokpapper")

    def get_info(self):

        self.name_input = ctk.CTkEntry(self)
        self.name_input.insert(0, "Enter Name")
        self.name_input.grid(row=1, column=0, sticky="n")

        self.guest_amount = ctk.CTkOptionMenu(
            self, values=["1", "2", "3", "4", "5", "6", "7", "8"])
        self.guest_amount.grid(row=1, column=2, sticky="n")

        self.date_input = ctk.CTkOptionMenu(self, values=[list_of_names[0], list_of_names[1], list_of_names[2],
                                            list_of_names[3], list_of_names[4], list_of_names[5], list_of_names[6]], command=guest.select_time)
        self.date_input.grid(row=1, column=4, sticky="n")

    def available_times(self):
        pass

# Create App class


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("The German Cock")

        self.geometry(f"{appWidth}x{appHeight}")

        self.toplevel_window = None

    def booking_page(self):
        if self.toplevel_window is None or not self.toplevel_window_winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.get_info()
        else:
            self.toplevel_window.focus()

    def main_page(self):

        # configure grid layout (5x5)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.logo_label = ctk.CTkLabel(self, text="German Cock", font=ctk.CTkFont(
            family="Lobster", size=20, weight="bold"))
        self.logo_label.grid(row=2, column=2, sticky="n", rowspan=1)

        self.start_button = ctk.CTkButton(
            self, text="Click To Book", command=self.booking_page)
        self.start_button.grid(row=2, column=2, sticky="", rowspan=1)


def main():
    app = App()
    db = Database()

    app.main_page()
    app.mainloop()


if __name__ == "__main__":
    main()
