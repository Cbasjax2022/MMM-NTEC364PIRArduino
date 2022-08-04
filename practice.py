from time import time
import gspread
from datetime import datetime
import requests

gc = gspread.service_account(filename='MMM PIR data')
sh = gc.open_by_key('1DorK1dQWwjlAj4ZiZ9OE_o8lVTSwrah3tS0H1yJ9ctc')
worksheet = sh.sheet1
now = datetime.now()

for i in range(5):
    current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    worksheet.update_cell(current_datetime)
