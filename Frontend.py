
"""
Application.py ini adalah class untuk GUI Aplikasi.
"""

import tkinter as tkr
from tkinter import messagebox
import tkinter.font as tk_font 
import time
import pyautogui as pag

import copy

import random


""" Untuk mengatur font family """
def Calibri(fontSize):
	return tk_font.Font(family = "Calibri", size = fontSize, underline = "0")

def Kaiti(fontSize):
	return tk_font.Font(family = "Kaiti", size = fontSize, underline = "0")



def split_thousands(n):
	result = ""
	while(n > 1000):
		result = str(int(n % 1000)).zfill(3) + result
		n //= 1000
		if n > 0:
			result = "." + result
	if n > 0:
		result = str(n) + result

	return result 


def in_range(n, maks):
	return 0 <= n < maks 



class Application(object):
	"""docstring for Application"""


	def __init__(self):
		super(Application, self).__init__()
		self.current_entry_cursor_position = 0
		self.number_of_entries = 4
		self.house_price_shown = 0

		self.set_window()
		self.set_prompts_and_entries()
		self.set_key_bindings()
		self.set_button()
		self.set_garage_button()
		self.place_application_title()

		self.win.mainloop()


	def set_window(self):
		# Segala pengaturan berkaitan dengan GUI Window
		self.win = tkr.Tk()
		self.win.title("Aplikasi Prediksi Harga Rumah") 
		self.win_bg = "#c4c4c4"
		self.win.config(bg = "#c4c4c4")
		screen_width, screen_height = pag.size()
		self.win.geometry(str(screen_height) + "x" + str(screen_width))
		self.win.state('zoomed') # Auto maximize
		self.win.iconphoto(False, tkr.PhotoImage(file = 'icon.png'))


	def shut_down(self):
		self.win.destroy()


	def place_application_title(self):
		self.title = tkr.Label(self.win,
								text = "Aplikasi Prediksi Harga Rumah di Jakarta Selatan",
								font = Calibri(50),
								bg = self.win_bg)
		self.title.place(relx = 0.5, rely = 0.15, anchor = tkr.CENTER)

		self.title2 = tkr.Label(self.win,
								# text = "南雅加达区域房子价格预测应用",
								font = Kaiti(50),
								bg = self.win_bg)
		self.title2.place(relx = 0.5, rely = 0.25, anchor = tkr.CENTER)


	# Key Bindings
	def set_key_bindings(self):
		self.win.bind('<Return>', self.BindEnter) # Bind tombol Enter di keyboard
		self.win.bind('<Up>', self.BindUp)
		self.win.bind("<KeyPress>", self.onKeyPress)
		self.win.bind('<Down>', self.move_cursor_to_next_entry)


	def BindEnter(self, arg):
		self.move_cursor_to_next_entry(0)


	def move_cursor_to_next_entry(self, arg):
		if in_range(self.current_entry_cursor_position + 1, self.number_of_entries):
			self.current_entry_cursor_position += 1
		self.focus_set_entry()


	def BindUp(self, arg):
		if in_range(self.current_entry_cursor_position - 1, self.number_of_entries):
			self.current_entry_cursor_position -= 1
		self.focus_set_entry()


	def onKeyPress(self, arg):
		self.re_show_prediction()
		

	def re_show_prediction(self):
		if self.house_price_shown > 0:
			self.house_price_label.place_forget()
		self.show_prediction(self.random_prediction_result(self.get_predictors()))


	# Setting Entries
	def focus_set_entry(self):
		self.all_entries[self.current_entry_cursor_position].focus_set()


	def set_prompts_and_entries(self):
		"""
		Setting entry untuk input luas tanah, luas bangunan, jumlah kamar tidur, dan jumlah kamar mandi.
		"""
		# self.all_prompts_and_entries = []
		self.all_prompts = []
		self.all_entries = []
		for i in range(self.number_of_entries):
			prompt = tkr.Label(self.win,
								text = "ini label",
								font = Calibri(20),
								bg = '#c4c4c4')
			entry = tkr.Entry(self.win,
										font = Calibri(20),
										width = 5
										)
			
			prompt_and_entry = [prompt, entry]
			self.all_prompts.append(prompt)
			self.all_entries.append(entry)

		variable = [
			["Luas tanah", 0.3],
			["Luas bangunan", 0.375],
			["Jumlah kamar tidur", 0.45],
			["Jumlah kamar mandi", 0.525],
		]

		for i in range(self.number_of_entries):
			self.all_prompts[i].config(text = variable[i][0])
			self.all_prompts[i].place(relx = 0.05, rely = variable[i][1])
			self.all_entries[i].place(relx = 0.22, rely = variable[i][1])

		self.all_entries[0].focus_set()


	def set_button(self):
		submit_button = tkr.Button(self.win, text = "SUBMIT", font = Calibri(30), command = self.get_predictors)
		# submit_button.place(relx = 0.2, rely = 0.8, anchor = tkr.CENTER)


	def set_garage_button(self):
		tidak_ada_garasi = tkr.Button(self.win, text = "Tidak ada garasi", font = Calibri(20), command = self.has_no_garage)
		ada_garasi = tkr.Button(self.win, text = "Ada garasi", font = Calibri(20), command = self.has_garage)

		tidak_ada_garasi.place(relx = 0.05, rely = 0.65, anchor = tkr.W)
		ada_garasi.place(relx = 0.18, rely = 0.65, anchor = tkr.W)


	def has_garage(self):
		self.ada_garasi = 1
		self.re_show_prediction()
		# print("ada garasi", self.ada_garasi)


	def has_no_garage(self):
		self.ada_garasi = 0
		self.re_show_prediction()
		# print("ada garasi", self.ada_garasi)


	# Machine Learning
	def get_predictors(self):
		predictors = []
		try:
			for i in range(self.number_of_entries):
				predictors.append(int(self.all_entries[i].get()))
			predictors.append(self.ada_garasi)
			return predictors
		except:
			print("Data prediktor belum lengkap!")


	def show_prediction(self, house_price):
		if house_price == None:
			return

		self.house_price_label = tkr.Label(self.win,
									text = "Rp " + split_thousands(house_price) + ",00",
									# text = "Rp " + split_thousands(self.get_predicted_house_price()) + ",00",
									font = Calibri(60))
		self.house_price_label.place(relx = 0.5, rely = 0.8, anchor = tkr.CENTER)
		self.house_price_shown += 1


	def random_prediction_result(self, predictors):
		"""
		Ini cuma fungsi dummy untuk mendapat hasil prediksi saja, sebelum ada model machine learning yang sesungguhnya, supaya terlihat tampilan prediksi harga akan seperti apa.
		"""
		if predictors != None:
			return random.randrange(500000000, 28000000000)


	def predict(self, predictors):
		"""
		Ini fungsi untuk mendapatkan hasil prediksi

		"""
		model = pickle.load(open(saved_model_filename, 'rb'))
		prediction = model.predict(np.array([predictors]))
		return prediction


a = Application()