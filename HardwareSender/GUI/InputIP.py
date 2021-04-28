import tkinter as tk
import os
from tkinter import messagebox, font


if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class InputIP(tk.Tk):
	"""
	This class is used to display the current game event on the Raspberry Pi.
	"""

	def __init__(self, ips):
		tk.Tk.__init__(self)
		self.title("FactoryRally")
		self.answer = None
		super().geometry("640x320")
		game_font = tk.font.Font(size=12)
		self.list = tk.Listbox(self, width=40, font=game_font, )
		self.confirm_button = tk.Button(self, text="Host auswählen", command=self.return_game)
		self.list.insert(0, *ips)
		self.list.pack()
		self.confirm_button.pack()

	def return_game(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		if tk.messagebox.askquestion("Question", "Sind Sie sicher, dass Sie diesen Host wählen wollen?") == 'yes':
			self.ip = self.list.get(self.list.curselection())
			self.iconify()
			self.destroy()
		else:
			tk.messagebox.showinfo("Information", "Bitte wählen Sie einen anderen Host aus!")
