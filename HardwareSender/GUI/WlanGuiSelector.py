import tkinter as tk
from GUI import WifiScanner
from tkinter import font
from tkinter import messagebox
import os

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class WlanSelector(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""
	def __init__(self):
		super().__init__()
		super().geometry("640x320")
		game_font = tk.font.Font(size=15)
		self.list = tk.Listbox(self, width=40, font=game_font, )
		self.list.insert(0, WifiScanner.return_all_wifi_connections())
		self.confirm_button = tk.Button(self, text="Choose WLAN", command=self.choose_wlan)
		self.list.pack()
		self.confirm_button.pack()

	def choose_wlan(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		self.value = self.list.get(self.list.curselection())
		WifiScanner.connect_to_wlan()
		self.destroy()

	def show_message_box(self):
		messagebox.showerror("Wrong Password entered!", "Please input the correct Password or choose another Network!")


if __name__ == '__main__':
	WlanSelector()


