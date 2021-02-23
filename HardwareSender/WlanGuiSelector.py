import tkinter as tk
from shlex import split
from tkinter import font
import os
import subprocess
from getpass import getpass

if os.environ.get('DISPLAY', '') == '':
	os.environ.__setitem__('DISPLAY', ':0.0')


class GameSelector(tk.Tk):
	"""
	This class provides a simple interface for the user to choose a game.
	"""
	def __init__(self, games):
		super().__init__()
		super().geometry("640x320")
		game_font = tk.font.Font(size=15)
		self.list = tk.Listbox(self, width=40, font=game_font, )
		self.list.insert(0, *games)
		self.confirm_button = tk.Button(self, text="Choose Game", command=self.print_selection)
		self.list.pack()
		self.confirm_button.pack()

	def return_game(self):
		"""
		This method retrieves the selected game when the user presses the button.
		"""
		self.value = self.list.get(self.list.curselection())
		self.destroy()


def getssid(netname):
    p1 = subprocess.Popen(split("nmcli --fields NAME"), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(split("grep -i "+str(netname)), stdin=p1.stdout, stdout=subprocess.PIPE)
    ss=p2.communicate()[0].decode('utf-8')
    return str(ss.split()[1])

result = subprocess.run(['nmcli', "d", "wifi", "list"], stdout=subprocess.PIPE)
scan_out_lines = str(result).split("\\n")[1:-1]
scan_out_data = {}
for each_line in scan_out_lines:
    split_line = [e for e in each_line.split(" ") if e != ""]
    line_data = {"SSID": split_line[0], "RSSI": int(split_line[2]), "channel": split_line[3], "HT": (split_line[4] == "Y"), "CC": split_line[5], "security": split_line[6]}
    scan_out_data[split_line[1]] = line_data

scan_out_data.get('Infra').get('SSID')

#network = input("Network: ")
#password = getpass()
#result = subprocess.run(['nmcli', "d", "wifi", "connect", network, "password", str(password)], stdout=subprocess.PIPE)
#print(result.stdout.decode('utf-8'))