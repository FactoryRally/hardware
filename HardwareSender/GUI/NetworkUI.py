# -*- coding: utf-8 -*-
import _tkinter
import tkinter as tk
from NetworkUtilities import NetworkUtility
from tkinter import font
from tkinter import messagebox
import os

"""
This module is the networking UI which gets started on boot 
and allows the user a simple interface to connect to a WLAN.
"""

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')

SELECTED_WLAN = None


class NetworkUI(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""

	# __init__ function for class tkinterApp
	def __init__(self):
		# __init__ function for class Tk
		tk.Tk.__init__(self)
		self.title("FactoryRally")
		super().geometry("640x320")

		# creating a container
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (WlanChooser, PasswordPage):
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
		"""
		This method is used to switch between frames.

		:param cont: the name of the frame which should be switched to
		"""
		frame = self.frames[cont]
		frame.tkraise()
		frame.update()


class WlanChooser(tk.Frame):
	"""
	This class displays all available networks and lets a user choose his network.
	"""

	def __init__(self, parent, controller):
		self.controller = controller
		tk.Frame.__init__(self, master=parent)
		game_font = tk.font.Font(size=15)
		self.list = tk.Listbox(self, width=30, height=5, font=game_font)
		for num, ele in enumerate(NetworkUtility.return_all_wifi_connections(), start=0):
			self.list.insert(num, ele)
		self.confirm_button = tk.Button(self, text="Netzwerk auswählen!", command=self.choose_wlan)
		scrollbar = tk.Scrollbar(self)
		scrollbar.pack(side="right", fill="y")
		self.list.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.list.yview)
		self.list.pack(pady=40)
		self.confirm_button.pack()

	def choose_wlan(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		global SELECTED_WLAN
		try:
			SELECTED_WLAN = self.list.get(self.list.curselection())
			self.controller.show_frame(PasswordPage)
		except _tkinter.TclError as e:
			tk.messagebox.showerror("Keine Auswahl getroffen!",
									"Bitte wählen Sie ein Netzwerk aus bevor Sie Netzwerk auswählen drücken!")


def show_error_box(msg):
	"""
	This function shows a error box with a given message.

	:param msg: the message to be displayed
	"""
	messagebox.showerror("Connection could not be established!", msg)


def show_question_box(msg, obj):
	"""
	This function displays a question box with a given question.

	:param obj: wrapper for switching between frames
	:param msg: the message thats to be displayed
	"""
	if tk.messagebox.askquestion("Warning", msg) == 'yes':
		tk.messagebox.showinfo('Info', msg)
	else:
		obj.master.switch_frame(WlanChooser).pack()


class PasswordPage(tk.Frame):
	"""
	This class is used to let the user input their password.
	"""

	def __init__(self, parent, controller):
		global SELECTED_WLAN
		self.controller = controller
		tk.Frame.__init__(self, master=parent)
		self.entry2 = tk.Entry(self)
		self.label = tk.Label(self)
		self.label.config(text='13', font=(None, 14))
		self.label.place(x=160, y=35, anchor="center")
		_text_ = '''entry2'''
		self.entry2.delete('0', 'end')
		self.entry2.insert('0', _text_)
		self.entry2.place(x=240, y=100)
		self.button4 = tk.Button(self)
		self.button4.configure(padx=60, pady=3, text='Abbrechen', command=lambda: self.controller.show_frame(WlanChooser))
		self.button4.place(x=350, y=160)
		self.button5 = tk.Button(self)
		self.button5.configure(padx=60, pady=3, text='Verbinden',
							   command=lambda: self.execute_password_check(ssid=SELECTED_WLAN))
		self.button5.place(x=130, y=160)

	def execute_password_check(self, ssid):
		"""
		This method connects to a given network using the given password.

		:param ssid: network name
		"""
		estab, msg = (NetworkUtility.connect_to_wlan(str(ssid), str(self.entry2.get())))
		if estab:
			app.destroy()
		else:
			show_error_box(msg)


app = NetworkUI()
app.mainloop()
