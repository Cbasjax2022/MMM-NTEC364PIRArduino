from time import time
import gspread
from datetime import datetime


# DEFINE VARIABLES
# SECRET CREDENTIALS FILE
gc = gspread.service_account(filename='apicredentials.json')
# API KEY
sh = gc.open_by_key('1DorK1dQWwjlAj4ZiZ9OE_o8lVTSwrah3tS0H1yJ9ctc')

worksheet = sh.sheet1
now = datetime.now()

# Function to find next empty row in spreadsheet
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def main():
    # Loop to write date/time to spreadsheet 5 times
    for i in range(5):
        next_row = next_available_row(worksheet)
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    # update_acell uses "a1, b7,etc cell notation.
    # update_cell uses "1, 1" cell notation as in 1st row 1st column. 
    # The following line updates the A column and uses string substitution to \
    # dynamically assign the next available row in the sheet
        worksheet.update_acell("A{}".format(next_row), current_datetime)
        # diagnostic output
        print("wrote {} row to spreadsheet".format(i+1))

    print("Done writing to spreadsheet")

main()