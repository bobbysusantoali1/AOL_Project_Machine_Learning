
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

import matplotlib.pyplot as mp
import numpy as np

import pickle

import house_price_dataset




""" Untuk mengatur font family """
def Calibri(fontSize):
	return tk_font.Font(family = "Calibri", size = fontSize, underline = "0")

def Kaiti(fontSize):
	return tk_font.Font(family = "Kaiti", size = fontSize, underline = "0")

def debug(content, identifier = ""):
	print("\n[debugging]", identifier, content, "\n")

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

def normalize(value, mean, stddev):
	return (value - mean) / stddev

def inverse_normalize(normalized_value, mean, stddev):
	return normalized_value * stddev + mean

def make_histogram(data):
	"""
	Parameter : 1-D Array atau List
	"""
	mp.hist(data, num_of_bins = 150)
	mp.show()


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
		self.place_application_title()
		self.set_visualization_buttons()
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
		self.show_prediction(self.predict([self.get_predictors()]))


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



	# Machine Learning
	def get_predictors(self):
		predictors = []
		column_mean = [
			381.4361014420686, 
 			383.3127797115863, 
 			4.56340129288911, 
 			3.773247140726007
		]

		column_stdev = [
			359.20056658411033,
 			421.96660419457726,
 			1.80335043836757,
 			1.685849903933497
		]
		

		for i in range(self.number_of_entries):
			temp = int(self.all_entries[i].get())
			predictors.append(normalize(temp, column_mean[i], column_stdev[i]))

		return predictors
		


	def show_prediction(self, house_price):
		# print("[debugging] HOUSE PRICE =", house_price)
		debug(house_price,"HOUSE PRICE")
		if house_price == None:
			return

		self.house_price_label = tkr.Label(self.win,
									text = "Rp " + split_thousands(house_price) + ",00",
									# text = "Rp " + split_thousands(self.get_predicted_house_price()) + ",00",
									font = Calibri(60))
		
		if house_price > 0:
			self.house_price_label.place(relx = 0.5, rely = 0.8, anchor = tkr.CENTER)
		
		self.house_price_shown += 1


	def predict(self, predictors):
		"""
		Ini fungsi untuk mendapatkan hasil prediksi

		"""
		debug(predictors, "predictors")

		saved_model_filename = 'model.sav'
		model = pickle.load(open(saved_model_filename, 'rb'))
		# predictor = np.array(predictors)
		prediction = model.predict(np.array(predictors))
		

		# hasil prediksi perlu di inverse transform
		prediction = inverse_normalize(prediction, 12529821426.753855, 16323248921.26816)
		prediction = int(prediction)

		# debug(prediction, 'prediction PREDIKSI')

		return prediction


	def show_histogram(self, idx):
		"""
		Fungsi perantara 
		"""
		print("show histogram cmd idx =", idx)
		pass


	def show_LT_histogram(self):
		print("masuk show lt hist")
		make_histogram(house_price_dataset.dataset[:,[1]])
		pass


	def show_LB_histogram(self):
		pass


	def show_KT_histogram(self):
		pass


	def show_KM_histogram(self):
		pass


	def set_visualization_buttons(self):
		"""
		Set button untuk menampilkan visualisasi pada window terpisah
		"""
		variable = [
			["Luas tanah", 0.29],
			["Luas bangunan", 0.365],
			["Jumlah kamar tidur", 0.44],
			["Jumlah kamar mandi", 0.515],
		]


		show_histogram_buttons = [
			tkr.Button(self.win,
						text = "Show Histogram " + variable[0][0],
						font = Calibri(20),
						command = self.show_LT_histogram),
			tkr.Button(self.win,
						text = "Show Histogram " + variable[1][0],
						font = Calibri(20),
						command = self.show_LB_histogram),
			tkr.Button(self.win,
							text = "Show Histogram " + variable[2][0],
							font = Calibri(20),
							command = self.show_KT_histogram),
			tkr.Button(self.win,
							text = "Show Histogram " + variable[3][0],
							font = Calibri(20),
							command = self.show_KM_histogram)
		]

		for i in range(4):
			show_histogram_buttons[i].place(relx = 0.27, rely = variable[i][1])


	



a = Application()
# print(hard_code_data.dataset)