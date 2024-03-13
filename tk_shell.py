# Import customtkinter module
import customtkinter as ctk
import tkinter as tk

# Sets the appearance mode of the application
# "System" sets the appearance same as that of the system
ctk.set_appearance_mode("dark")	 

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
ctk.set_default_color_theme("dark-blue")

# window size
appWidth, appHeight = 900, 700

# Create App class
class App(ctk.CTk):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title("The German Cock") 

		self.geometry(f"{appWidth}x{appHeight}") 

		# configure grid layout (4x4)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(2, weight=0)
		self.grid_rowconfigure((0, 1, 2), weight=1)

		self.logo_label = ctk.CTkLabel(self, text="Welcome", font=ctk.CTkFont(size=20, weight="normal"))
		self.logo_label.grid(row=1, column=1, padx=0, pady=0)
		self.nothing = ctk.CTkLabel(self, text=" ", font=ctk.CTkFont(size=20, weight="normal"))
		
	

if __name__ == "__main__":
	app = App()
	app.mainloop() 


