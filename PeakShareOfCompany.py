import sys
import csv
from collections import OrderedDict, namedtuple

class DataInconsistantException(Exception):
    pass


def PeakShareOfCompanies(file_name):
    """ Reading csv data file and retruning company based """
    try:
        with open(file_name) as file_data:
           reader = csv.reader(file_data)
           return GetPeakShare(reader)
    except IOError, err:
         raise IOError("File dosen't Exist")

def get_company_names(raw_data):
    '''
    retrieving all the company names
    '''
    return next(raw_data)[2:]


def GetPeakShare(reader):
    '''
    doing all the compuation
    '''
    schema = namedtuple('parameters', ['price', 'year', 'month'])
    result = OrderedDict()
    company_names = get_company_names(reader)
    for name in company_names:
        result[name] = schema(0, 'year', 'month')
    for row in reader:
        try:
            year, month = row[:2] 
            if year=='' or month=='':
                raise DataInconsistantException("Please check the data inside the file")
            for name, price in zip(company_names, map(int, row[2:])): 
                if result[name].price < price:
                    result[name] = schema(price, year.strip(), month.strip())
        except:
            raise DataInconsistantException("Please check the data inside the file")
    return result

def displayResult(output):
    '''
    converting order dict into list
    '''
    for company,value in output.iteritems():
       print("%s: %s %s (%s)" % (company, value.year, value.month,value.price))

def main():
    print "Enter the csv file path "
    file_path = raw_input("input: ")
    output=PeakShareOfCompanies(file_path)
    print "********************OUTPUT***********************"
    displayResult(output)
    print "*************************************************"
         

if __name__ == "__main__":
    main()