import glob
from fpdf import FPDF
import pandas as pd
from pathlib import Path

filepaths = glob.glob("xlsx/*.xlsx")
# print(filepath)  # ['xlsx/10002-2023.1.18.xlsx', 'xlsx/10001-2023.1.18.xlsx', 'xlsx/10003-2023.1.18.xlsx']

for file in filepaths:
	# Gather the data
	df = pd.read_excel(file, sheet_name="Sheet 1")
	order_number, date = Path(file).stem.split("-")
	columns_names = [item.replace("_", " ").title() for item in list(df.columns)]  # Format the column names
	# Find and change some names to a shorter version
	for i in range(len(columns_names)):
		if columns_names[i] == 'Amount Purchased':
			columns_names[i] = 'Quantity'
		if columns_names[i] == "Price Per Unit":
			columns_names[i] = "Unit Price"
		if columns_names[i] == "Total Price":
			columns_names[i] = "Total"

	# Create a new PDF
	pdf = FPDF(orientation="portrait", unit="mm", format="a4")
	pdf.add_page()

	# Write the title and date
	pdf.set_font(family="times", size= 24, style="B")
	pdf.cell(w=0, h=15, ln=1, txt=f"Order number: {order_number}" )
	pdf.set_font(family="times", size= 18, style="B")
	pdf.set_text_color(90, 90, 90)
	pdf.cell(w=0, h=10, ln=1, txt=f"Date (y/m/d): {date}" )
	pdf.ln(5)

	# Write the names of each column
	pdf.set_font(family="helvetica", size=14)
	pdf.set_text_color(0, 0, 0)
	pdf.cell(border=1, w=30, h=10, txt=columns_names[0], ln=0)  # product id
	pdf.cell(border=1, w=80, h=10, txt=columns_names[1], ln=0)  # product name
	pdf.cell(border=1, w=25, h=10, txt=columns_names[3], ln=0)  # unit price
	pdf.cell(border=1, w=23, h=10, txt=columns_names[2], ln=0)  # amount purchased
	pdf.cell(border=1, w=0, h=10, txt=columns_names[4], ln=1)  # total price

	# Write the individual items and its cost
	total_price = 0
	for index, row in df.iterrows():
		total_price += row["total_price"]

		pdf.cell(border=1, w=30, h=10, txt=str(row["product_id"]), ln=0)
		pdf.cell(border=1, w=80, h=10, txt=str(row["product_name"]), ln=0)
		pdf.cell(border=1, w=25, h=10, txt=str(row["price_per_unit"]), ln=0)
		pdf.cell(border=1, w=23, h=10, txt=str(row["amount_purchased"]), ln=0)
		pdf.cell(border=1, w=0, h=10, txt=str(row["total_price"]), ln=1)

	pdf.cell(border=1, w=0, h=10, txt=f"Total Cost: ${total_price}", ln=1, align="R")


	# Save and export
	pdf.output(f"PDFs/{order_number}-store_name.pdf")
