import glob
import fpdf
import pandas as pd

filepaths = glob.glob("xlsx/*.xlsx")
# print(filepath)  # ['xlsx/10002-2023.1.18.xlsx', 'xlsx/10001-2023.1.18.xlsx', 'xlsx/10003-2023.1.18.xlsx']

index = 1
for file in filepaths:
	df = pd.read_excel(file, sheet_name="Sheet 1")
	print(f"------- Printing file {index} -------")
	print(df)
	print(" ")
	index += 1
