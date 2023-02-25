import ijson
import argparse
from openpyxl import Workbook

# read threats from input json and put into a list
def put_json_into_list(filename):
    topten = [['Rank','TID','Name','URL']]
    with open(filename, "rb") as f:
        for record in ijson.items(f, "item"):
            threat = [
                record["rank"],
                record["tid"],
                record["name"],
                record["url"],
            ]
            topten.append(threat)
    return topten

# export to CSV
def export_to_csv(filename, output):
    topten = put_json_into_list(filename)
    resulting_csv = open(output, "w")
    resulting_csv.write("\n")
    for threat in topten:
        for i in threat:       
            resulting_csv.write("{},".format(i))
        resulting_csv.write("\n")
    resulting_csv.close()

# export to XLSX (MS Excel)
def export_to_xlsx(filename, output):
    topten = put_json_into_list(filename)
    workbook = Workbook()
    sheet = workbook.active
    for threat in topten:
        sheet.append(threat)
    workbook.save(output)

# define input parameters 
parser = argparse.ArgumentParser(
    prog='tttexport',
    description='Simple exporter of Top10 Threats from MITRE Calculator')

parser.add_argument("-f", "--format", type=str, help="Output format: csv|xlsx")
parser.add_argument("-i", "--inputfile", type=str, help="JSON file from MITRE Top10 Calc")
parser.add_argument("-o", "--outputfile", type=str, help="Output filename")
args = parser.parse_args()

# run the proggy
if args.format == None or args.inputfile == None or args.outputfile == None:
    print("some arguments are not present, try again or run with --help\n")
elif args.inputfile and args.outputfile != None and args.format == 'csv':
    export_to_csv(args.inputfile, args.outputfile)
elif args.inputfile and args.outputfile != None and args.format == 'xlsx':
    export_to_xlsx(args.inputfile, args.outputfile)
