import tkinter as tk

class InformationDisplay(tk.Frame):
	"""
	This
	"""

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, master=parent)
		self.controller = controller
		# build ui
		self.text3 = tk.Text(self)
		self.text3.configure(borderwidth='2', height='10', width='120')
		_text_ = '''text3'''
		self.text3.insert('0.0', _text_)
		self.text3.pack(side='top')
		self.configure(height='200', width='200')
		self.pack(side='top')


	def update_information(self):
		"""
		This
		:return:
		"""
		self