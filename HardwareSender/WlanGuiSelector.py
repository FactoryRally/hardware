import tkinter as tk
from shlex import split
from tkinter import font
import os
import subprocess
import WifiScanner

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class GameSelector(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""
	def __init__(self, games):
		super().__init__()
		super().geometry("640x320")
		game_font = tk.font.Font(size=15)
		self.list = tk.Listbox(self, width=40, font=game_font, )
		self.list.insert(0, *games)
		self.confirm_button = tk.Button(self, text="Choose Game", command=self.print_selection)
		self.list.pack()
		self.confirm_button.pack()

	def return_game(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		self.value = self.list.get(self.list.curselection())
		self.destroy()


