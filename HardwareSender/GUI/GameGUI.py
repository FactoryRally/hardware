import tkinter as tk
from tkinter import font
from tkinter import messagebox
import os

"""
This module is the UI which handles the whole game process. 
"""

SELECTED_GAME = ""

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class GameGUI(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""

	# __init__ function for class tkinterApp
	def __init__(self, main):
		# __init__ function for class Tk
		tk.Tk.__init__(self)
		self.title("FactoryRally")
		super().geometry("640x320")
		# creating a container
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.main = main

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (GameStartPage, GameSelector):
			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(GameStartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		"""
		This method is used to switch between frames.

		:param cont: the name of the frame which should be switched to
		"""
		frame = self.frames[cont]
		frame.tkraise()
		frame.update()

	def get_game(self):
		return SELECTED_GAME

	def set_games(self, games):
		self.frames[GameSelector].list.insert(0,*games)


class GameStartPage(tk.Frame):
	"""
	This class is used to tell it should generate a new Publisher as a new
	game started.
	"""
	ACTIVE = False

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, master=parent)
		self.controller = controller
		self.text = tk.StringVar()
		self.text.set("Bitte warten Sie bis zumindest ein Spiel erstellt wurde.")
		self.label1 = tk.Label(self)
		self.label1.configure(textvariable=self.text, font=(None, 12))
		self.label1.place(x='240', y='80', anchor='center')
		self.button = tk.Button(self, text='Ein Spiel ist erstellt', command=self.button_click)
		self.button.place(x='240', y='150', anchor='center')

	def button_click(self):
		"""
		This method sets the parameter active to true if a game is running
		according to user input.
		"""
		self.ACTIVE = True
		self.controller.frames[GameSelector].list.insert(0, *self.controller.main.resource_handler.get_games())
		self.controller.show_frame(GameSelector)

	def get_state(self):
		"""
		This method returns the current state of the button. If it is pressed,
		it resets it.

		:return: whether or not the button is pressed
		"""
		if self.ACTIVE:
			self.ACTIVE = False
			self.controller.show_frame(GameSelector)
			return self.ACTIVE
		return False


class GameSelector(tk.Frame):
	"""
	This class provides a simple interface for the user to choose a game.
	"""

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, master=parent)
		self.controller = controller
		game_font = tk.font.Font(size=12)
		self.list = tk.Listbox(self, width=40, font=game_font, )
		self.confirm_button = tk.Button(self, text="Spiel auswählen", command=self.return_game)
		self.list.pack()
		self.confirm_button.pack()

	def return_game(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		global SELECTED_GAME
		if tk.messagebox.askquestion("Question", "Sind Sie sicher, dass Sie dieses Spiel wählen wollen?") == 'yes':
			SELECTED_GAME = self.list.get(self.list.curselection())
			self.controller.iconify()
			self.controller.destroy()
		else:
			tk.messagebox.showinfo("Information", "Bitte wählen Sie ein anderes Spiel aus!")

	def set_games(self, games):
		"""
		This method sets a given list.

		:param games: the currently active games
		"""
		self.list.insert(0, *games)