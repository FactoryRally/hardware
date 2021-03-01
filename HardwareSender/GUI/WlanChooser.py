from tkinter import font
import _tkinter
import tkinter as tk
from GUI import PasswordPage

selected_wlan = ""

class WlanChooser(tk.Frame):
	"""
	This
	"""
	def __init__(self, parent, controller):
		self.controller = controller
		tk.Frame.__init__(self, master=parent)
		game_font = tk.font.Font(size=15)
		self.list = tk.Listbox(self, width=40, font=game_font)
		self.list.insert(0, ["a", "b", "c"])
		self.confirm_button = tk.Button(self, text="Choose WLAN", command=self.choose_wlan)
		self.list.pack()
		self.confirm_button.pack()

	def choose_wlan(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		global selected_wlan
		try:
			selected_wlan = self.list.get(self.list.curselection())
			self.controller.show_frame(PasswordPage)
		except _tkinter.TclError as e:
			tk.messagebox.showerror("Selection Error", "Please select a WLAN Interface before your press choose WLAN!")