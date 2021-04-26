import tkinter as tk
import os

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class InputIP(tk.Tk):
	"""
	This class is used to display the current game event on the Raspberry Pi.
	"""

	def __init__(self):
		tk.Tk.__init__(self)
		self.title("FactoryRally")
		self.answer = None
		super().geometry("640x320")
		self.text.set("Bitte gegen Sie die IP-Adresse vom Spielserver ein:")
		self.label1 = tk.Label(self)
		self.label1.configure(textvariable=self.text, font=(None, 12))
		self.label1.place(x='220', y='60', anchor='center')
		self.entry2 = tk.Entry(self)
		self.entry2.place(x=160, y=100)
		self.button = tk.Button(self, text='IP auswählen', command=self.choose_ip)
		self.button.place(x='240', y='170', anchor='center')

	def choose_ip(self):
		self.answer = self.entry2.get()
		self.iconify()
		self.destroy()
