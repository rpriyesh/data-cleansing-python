# Author:   Priyesh Rajamohanan
# Date:     27 November 2016
# Desc:     Class to clean order data

import datetime
import re

class OrderCleaner:
    def __init__(self, counties_lookup, orders):
        self.counties_lookup = counties_lookup
        self.orders = orders

    def clean_data(self):
        max = len(self.orders)
        # loop and clean each order
        for index in range(1, max, 1):
            order = self.orders[index]

            order.contact_name = self.clean_contact_name(order.contact_name)

            company, address1, county, eir_code = self.split_address(order.company, order.address1)
            order.company = company
            order.address1 = address1
            order.county = county
            order.eir_code = eir_code

            is_valid, result = self.validate_country_code(order.country_code)
            if is_valid:
                order.country_code = result
            else:
                order.remarks += "Invalid country code; "

            is_valid, result = self.validate_phone(order.phone)
            if is_valid:
                order.phone = result
            else:
                order.is_valid = False
                order.remarks += "Invalid phone; "

            is_valid, result = self.validate_amount(order.amount)
            if is_valid:
                order.amount = result
            else:
                order.is_valid = False
                order.remarks += "Invalid amount; "

            is_valid, result = self.validate_date(order.order_date)
            if is_valid:
                order.order_date = result
            else:
                order.is_valid = False
                order.remarks += "Invalid date; "

            self.orders[index] = order
        return self.orders

    def clean_contact_name(self, name):
        name = name.strip()
        return name

    def validate_country_code(self, code):
        try:
            int(code)
            return True, code
        except ValueError:
            return False, ""

    def validate_county(self, county):
        county_formatted = county.lower()
        county_formatted = county_formatted.replace(".", "")
        county_formatted = county_formatted.replace("co ", "")
        county_formatted = county_formatted.replace("go ", "")
        county_formatted = ''.join([char for char in county_formatted if not char.isdigit()])
        county_formatted = county_formatted.strip()
        # check if the county name exists in the county lookup
        if any(county_formatted in item for item in self.counties_lookup):
            return True
        else:
            return False

    def validate_phone(self, phone):
        phone_formatted = phone.strip()
        phone_formatted = phone_formatted.replace("-", "")

        try:
            int(phone_formatted)
            return True, phone
        except ValueError:
            return False, ""

    def validate_amount(self, amount):
        try:
            float(amount)
            return True, amount
        except ValueError:
            return False, 0

    def validate_date(self, date):
        try:
            datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
            return True, date
        except ValueError:
            return False, date

    def clean_county(self, county):
        county = county.title().replace("Go", "Co")  # special condition for Go Galway
        county = county.replace(".", "")  # removing special characters

        # special condition for D1, D2, D3
        pattern = re.compile('[D]{1}[\d]{1}$')
        res = re.match(pattern, county)
        if len(county) == 2 and res is not None:
            county = 'Dublin' + county.replace('D', '')

        # prefixing counties with Co
        if not county.startswith('Co ', 0, 3):
            county = 'Co ' + county

        return county

    def split_address(self, company, address):
        address1 = ""
        county = ""
        eir_code = ""

        if address is not None:
            address_lines = address.split(",")
            counter = 1
            max = len(address_lines)
            # finding the last 2 address parts to validate county and eir code
            for index in range(max, max - 2, -1):
                address_line = address_lines[index - 1]
                address_line = address_line.strip()
                pattern = re.compile('[AC-FHKNPRTV-Y]{1}[0-9]{1}[0-9W]{1}[ \-]?[0-9AC-FHKNPRTV-Y]{4}$')
                res = re.match(pattern, address_line)
                if res is not None:
                    # if valid, consider as eir code remove from the address part
                    eir_code = address_line
                    address = address.replace(address_line, "")
                elif self.validate_county(address_line):
                    # if valid, consider as county remove from the address part
                    county = self.clean_county(address_line)

                    address = address.replace(address_line, "")

            # clean and join the remaining address part to form Address 1
            address_lines = address.split(",")
            for address_line in address_lines:
                if address_line.strip() is not "":
                    if company is "" or company is None:
                        company = address_line
                    else:
                        address1 += address_line + ', '

            address1 = ' '.join(address1.split())
            address1 = address1.strip()
            while address1.endswith(","):
                address1 = address1[:-1]
                address1 = address1.strip()

        return company, address1, county, eir_code
