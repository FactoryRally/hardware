class NewprojectApp:
    def __init__(self, master=None):
        root.geometry('640x320')

        self.text = tk.StringVar()
        self.text1 = tk.StringVar()

        self.text.set("Aktueller Spielzug:")
        self.text1.set("")
        # build ui
        self.frame1 = tk.Frame(master)
        self.label1 = tk.Label(self.frame1)
        self.label1.configure(textvariable=self.text, font=(None, 24))
        self.label1.place(x='130', y='80', anchor='center')
        self.label2 = tk.Label(self.frame1)
        self.label2.configure(textvariable=self.text1, font=(None, 35))
        self.label2.place(x='160', y='130', anchor='center')
        self.frame1.configure(height='640', width='320')
        self.frame1.place(anchor='nw', x='0', y='0')

        # Main widget
        self.mainwindow = self.frame1
        self.mainwindow.update()

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()
