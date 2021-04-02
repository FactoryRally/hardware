import tkinter as tk

class GameStartPage(tk.Tk):
	"""
	This class is used to display the current game event on the Raspberry Pi.
	"""

	ACTIVE = False

	def __init__(self):
		tk.Tk.__init__(self)
		super().geometry("640x320")
		self.text = tk.StringVar()
		self.text.set("Spiel beendet!")
		self.label1 = tk.Label(self)
		self.label1.configure(textvariable=self.text, font=(None, 24))
		self.label1.place(x='130', y='80', anchor='center')
		self.button = tk.Button(self, text='Neues Spiel ist gestartet!', command=self.button_click)
		self.button.place(x='320', y='220', anchor='center')

	def button_click(self):
		"""
		This method
		"""
		self.ACTIVE = True

	def get_state(self):
		"""
		This method returns the current state of the button. If it is pressed,
		it resets it.
		:return: whether or not the button is pressed
		"""
		if self.ACTIVE:
			self.ACTIVE = False
			return self.ACTIVE
		return False

val = GameStartPage()
val.mainloop()