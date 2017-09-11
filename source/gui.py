import tkinter as tk
from tkinter import font, messagebox

import itertools as it
import os
import subprocess
import webbrowser

from cmdHandler import CmdHandler
from cmdHandler import CONFIG_FILE_PATH


root = tk.Tk()
cmd = CmdHandler()

class MainButton(object):
	"""docstring for MainButton"""
	
	def __init__(self):
		super(MainButton, self).__init__()
		
		self.button = tk.Button(root, command=self.toggleFirewall)

		self.state = False

		self.image_on = tk.PhotoImage(file="../etc/on.png")
		self.image_off = tk.PhotoImage(file="../etc/off.png")

		self.button.config(image=self.image_off)

		self.button.pack()

	def toggleFirewall(self):

		if cmd.isAdmin is not True:
			popupAdmin()

		if self.state and cmd.firewallOFF():
				self.button['image'] = self.image_off
				self.state = False
		elif cmd.firewallON():
				self.button['image'] = self.image_on
				self.state = True

def makeAboutButton():
	img = tk.PhotoImage(file="../etc/about.png")

	b = tk.Button(root, command=showAbout)
	b.config(image=img)
	b.image = img

	return b

def showAbout():
	webbrowser.open("https://github.com/thepunishbr/overwatch-troll-control", new=0, autoraise=True)

def popupAdmin():
	tk.messagebox.showerror("Error", "Sorry, you need to run this program as ADMIN")
	root.destroy()

def openConfigFile():
	subprocess.run(["notepad.exe ", CONFIG_FILE_PATH])
	cmd.loadConfig()
	print("[Info] New config loaded!")

def makeConfigButton():
	helv = font.Font(family='Calibri', size=14, weight=font.BOLD)
	b = tk.Button(root, text="config", font=helv, command=openConfigFile)

	return b

def on_closing():
	cmd.firewallOFF()
	root.destroy()

def main():

	main_button = MainButton()
	about_button = makeAboutButton()
	help_button = makeConfigButton()

	root.rowconfigure((0,1), weight=1)
	root.columnconfigure((0,2), weight=1) 

	main_button.button.grid(row=0, column=0, columnspan=2, sticky='EWNS')
	help_button.grid(row=1, column=0, columnspan=1, sticky='EWNS')
	about_button.grid(row=1, column=1, columnspan=1, sticky='EWNS')

	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.title("Overwatch Troll Control v1.1")

	root.mainloop()

if __name__ == '__main__':
	main()

