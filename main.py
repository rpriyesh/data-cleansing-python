# Author:   Priyesh Rajamohanan
# Date:     26 November 2016
# Desc:     Excel file cleanup using OpenPyXL

from order_cleaner import OrderCleaner
from excel_ops import FileReader, FileWriter

counties_lookup = ('antrim', 'armagh', 'carlow', 'cavan', 'clare', 'cork', 'derry',
                   'donegal', 'down', 'dublin', 'fermanagh', 'galway', 'kerry',
                   'kildare', 'kilkenny', 'laois', 'leitrim', 'limerick', 'longford',
                   'louth', 'mayo', 'meath', 'monaghan', 'offaly', 'roscommon', 'sligo',
                   'tipperary', 'tyrone', 'waterford', 'westmeath', 'wexford', 'wicklow')

# read file
reader = FileReader('Data\\Customers2016.xlsx')
orders_raw = reader.read_file()

# clean data read from file
cleaner = OrderCleaner(counties_lookup, orders_raw)
orders_clean = cleaner.clean_data()

# write new file with clean data
writer = FileWriter('Data\\Customers2016_Cleaned.xlsx')
writer.write_file(orders_clean)

print ("\nSuccess! Please find the cleaned file under 'Data' folder.")
