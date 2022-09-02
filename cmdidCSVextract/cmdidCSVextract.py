# Original code by nguen, modified for MoonlightTS by tamilpp25
# Used for converting sorapointa's cmdid.csv to MoonlightTS packetIds.json

import csv
import json
from sys import argv

def convert(csv_path: str, json_path='./packetIds.json'):
    result = {'PacketHead': 13371337}

    with open(csv_path, 'r') as csv_cmdid:
        csv_rows = csv.reader(csv_cmdid)
        for row in csv_rows:
            packetName = row[0]
            cmdid = int(row[1])
            result[packetName] = cmdid

    with open(json_path, 'w') as json_cmdid:
        json.dump(result, json_cmdid, indent=4)

def toEnum(csv_path: str, json_path='./cmdids.ts'):
    with open(csv_path, 'r') as csv_cmdid:
        csv_rows = csv.reader(csv_cmdid)
        with open(json_path, 'w') as enum_cmd:
            enum_cmd.write('export enum CmdID {\n\tPacketHead = 13371337,\n')
            data = list(csv_rows)
            for i,row in enumerate(data):
                packetName = row[0]
                cmdid = int(row[1])
                # result[packetName] = cmdid
                if i != (len(data)-1) :
                    enum_cmd.write("\t{} = {},\n".format(packetName,cmdid))
                else:
                    enum_cmd.write("\t{} = {}\n".format(packetName,cmdid))
            enum_cmd.write("}")

def usage():
    print(
"""\tCmdId CSV extractor
Usage: 
    py cmdidCSVextract.py <cmdid.csv path> [packetids.json path] [enum form? (True|False)] - Convert cmdid to packetIds.json

Note:
    enum form is for newer version of MoonlightTS""")


if __name__ == "__main__":
    if len(argv) < 3:
        usage()
    else:
        if len(argv) == 3: 
            convert(argv[1])
        elif len(argv) == 4:
            if argv[3].lower() == "true":
                toEnum(argv[1],argv[2])
            elif argv[3].lower() == "false":
                convert(argv[1],argv[2])
            else:
                usage()
        else:
            usage()
        