import tkinter as tk
import os

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')

class InformationDisplay(tk.Tk):
	"""
	This class is used to display the current game event on the Raspberry Pi.
	"""

	def __init__(self):
		super().__init__("FactoryRally")
		self.text = tk.StringVar()
		self.text1 = tk.StringVar()
		super().geometry("640x320")

		self.text.set("Aktueller Spielzug:")
		self.text1.set("")
		self.label1 = tk.Label(self)
		self.label1.configure(textvariable=self.text, font=(None, 24))
		self.label1.place(x='130', y='80', anchor='center')
		self.label2 = tk.Label(self)
		self.label2.configure(textvariable=self.text1, font=(None, 35))
		self.label2.place(x='160', y='130', anchor='center')

	def update_information(self, msg):
		"""
		This method displays the current game event.

		:param: msg: the current game event
		"""
		self.text1.set(msg)