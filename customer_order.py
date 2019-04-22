# Author:   Priyesh Rajamohanan
# Date:     26 November 2016
# Desc:     Class to hold order details


class CustomerOrder:
    def __init__(self, contact_name, company, address, country_code, phone, amount, order_date):
        self.contact_name = contact_name
        self.company = company
        self.address1 = address
        self.county = ""
        self.eir_code = ""
        self.country_code = country_code
        self.phone = phone
        self.amount = amount
        self.order_date = order_date
        self.is_valid = True
        self.remarks = ""
