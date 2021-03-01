import _tkinter
import tkinter as tk
from GUI import WifiScanner
from tkinter import font
from tkinter import messagebox
import os

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')

selected_wlan = ""


class WlanSelector(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""

	# __init__ function for class tkinterApp
	def __init__(self):
		# __init__ function for class Tk
		tk.Tk.__init__(self)

		# creating a container
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (WlanChooser, PasswordPage, InformationDisplay):
			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(WlanChooser)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


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


def show_error_box(msg):
	"""
	This
	:param msg:
	:return:
	"""
	messagebox.showerror("Wrong Password entered!", msg)


def show_question_box(msg, obj):
	"""
	This
	:param obj:
	:param msg:
	:return:
	"""
	if tk.messagebox.askquestion("Warning", msg) == 'yes':
		tk.messagebox.showinfo('Info', msg)
	else:
		obj.master.switch_frame(WlanChooser).pack()


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
								command=lambda: self.execute_password_check(ssid=selected_wlan))
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
			show_error_box("Password wrong!")


class InformationDisplay(tk.Frame):
	"""
	This
	"""

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, master=parent)
		self.controller = controller
		self.text3 = tk.Text(self)
		self.text3.configure(borderwidth='2', height='10', width='120')
		_text_ = '''text3'''
		self.text3.insert('0.0', _text_)
		self.text3.pack(side='top')

	def update_information(self):
		"""
		This
		:return:
		"""


app = WlanSelector()
app.mainloop()
