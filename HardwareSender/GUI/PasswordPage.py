import tkinter as tk
from NetworkUtilities import WifiScanner
from GUI import WlanChooser
from GUI import WlanGuiSelector


class PasswordPage(tk.Frame):
	"""
	This is wrong
	"""

	def __init__(self, parent, controller):
		global selected_wlan
		self.controller = controller
		tk.Frame.__init__(self, master=parent)
		print(type(parent))
		self.label2 = tk.Label(self)
		self.label2.configure(text=selected_wlan)
		self.label2.pack(side='top')
		self.entry2 = tk.Entry(self)
		_text_ = '''entry2'''
		self.entry2.delete('0', 'end')
		self.entry2.insert('0', _text_)
		self.entry2.pack(side='top')
		self.button4 = tk.Button(self)
		self.button4.configure(padx='20', pady='5', text='Cancel', command=lambda: self.controller.show_frame(WlanChooser))
		self.button4.pack(side='right')
		self.button5 = tk.Button(self)
		self.button5.configure(padx='20', pady='5', relief='raised',
								command=lambda: self.execute_password_check(ssid=WlanChooser.selected_wlan))
		self.button5.pack(side='left')

	def execute_password_check(self, ssid):
		"""
		This
		:param master:
		:return:
		"""
		print(type(self.entry2.get()))
		check = WifiScanner.connect_to_wlan(str(ssid), str(self.entry2.get()))
		if check:
			self.controller.show_frame(InformationDisplay).pack()
		else:
			WlanGuiSelector.show_error_box("Password wrong!")