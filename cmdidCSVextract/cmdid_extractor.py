import json
import sys

HEADER = '''export enum CmdID {
  PacketHead = 13371337,
'''
FOOTER = '}'

lines = [HEADER]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        data = json.load(open(sys.argv[1],'r'))
        for i in data.items():
            lines.append(f'  {i[1]} = {(i[0])},\n')
        lines.append(FOOTER)
        with open(sys.argv[2],'w') as f:
            f.writelines(lines)
            print(f'Wrote cmdids to file {sys.argv[2]}')
    else:
        print('\tConvert crepe protos packetIds.json to MoonlightTS enums')
        print('Usage: py cmdid_extractor.py <path to packetIds.json> <outputfile>')