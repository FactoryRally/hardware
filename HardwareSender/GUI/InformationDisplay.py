import tkinter as tk
import os

if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')


class InformationDisplay(tk.Tk):
    """
    This class is used to display the current game event on the Raspberry Pi.
    """

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("FactoryRally")
        self.text = tk.StringVar()
        self.text1 = tk.StringVar()
        super().geometry("640x320")

        self.text.set("Aktueller Spielzug:")
        self.text1.set("")
        self.label1 = tk.Label(self)
        self.label1.configure(textvariable=self.text, font=(None, 12))
        self.label1.place(x='130', y='80', anchor='center')
        self.label2 = tk.Label(self)
        self.label2.configure(textvariable=self.text1, font=(None, 16))
        self.label2.place(x='190', y='130', anchor='center')

    def update_information(self, msg):
        """
        This method displays the current game event.

        :param: msg: the current game event
        """
        self.text1.set(msg)
        self.label2.update()

if __name__ == '__main__':
    infp = InformationDisplay()
    infp.update_information("movement: Player 2")
    infp.mainloop()