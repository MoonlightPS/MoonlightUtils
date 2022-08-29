# MIT License

# Copyright (c) 2022 tamilpp25

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import listdir
import os
import sys


def packProtos(protoname,inputdir):
    writtenfiles = 0
    fileCount = len(listdir(inputdir))
    with open(protoname,'w') as final:
        final.write('syntax = "proto3";\n\n')
        print("Reading proto files...")
        for i in listdir(inputdir):
            with open(inputdir+i,'r') as protofile:
                index = 0
                canWrite = False
                for index,line in enumerate(protofile):
                    if(line.startswith('enum') or line.startswith('message') or canWrite):
                        canWrite = True
                        final.write(line)
                    else:
                        continue
                print("Writing proto file",i,"to",protoname)
                final.write('\n')
                writtenfiles += 1
    print('Done writing protofile!')
    print("Loaded files:",fileCount,"Written files:",writtenfiles)


PROTOS = []
# OG_PROTOFILE_LOCATION = "C:\\Stuff\\Starrail\\CrepeSR\\src\\data\\proto\\StarRail.proto"
# PROTO_OUTPUT_DIR = "C:\\Stuff\\Starrail\\protos\\"
JAVA_PACKAGE = "io.grasscutter.stargazer.net.proto"
# for unpacking java format^


def oneLineProtoGen(value,PROTO,output):
    split = value.split()
    with open(PROTO + split[1] + ".proto",'w') as proto:
        proto.write('syntax = "proto3";\n')
        proto.write('option java_package = '+ "\"" + JAVA_PACKAGE + "\"" + ';\n\n')
        # print("one line! ",name,line)

        if("{}" in split):
            proto.write(value)
        else:
            if("repeated" in split or "oneof" in split and split[4] in PROTOS):
                if(split[4] in PROTOS):
                    proto.write("import \"" + split[4] + ".proto\";\n\n")
            else:
                if(split[3] in PROTOS):
                    proto.write("import \"" + split[3] + ".proto\";\n\n")
            proto.write(value)
        print("Generated " + split[1] + ".proto !")
                    

def generateManyLineProto(line,value,PROTO,output):
    lines = open(PROTO,'r').readlines()
    generated = []
    data = value.split()
    tempImport = [] #to prevent dupe imports

    while lines[line] != "}\n":
        # print(lines[line])
        generated.append(lines[line])
        line+=1

    generated.append("}\n")

    with open(output + data[1] + ".proto",'w') as proto:
        proto.write('syntax = "proto3";\n')
        proto.write('option java_package = '+ "\"" +JAVA_PACKAGE + "\"" + ';\n\n')

        # print("\nJust generated:",generated)
        # print("\nJoint string:\n","".join(generated),sep="")

        copy_generated = generated.copy()
        del copy_generated[0]
        del copy_generated[-1]

        if("oneof" in "".join(generated)):
            del copy_generated[-1]

        # Special case for 1 line oneof field proto:
        for i in generated:
            if(len(generated) == 3 and "oneof" in "".join(generated)):
                splitData = i.split()
                # print("splitData:",splitData,"size:",len(splitData))
                if(len(splitData) > 3 and splitData[3] in PROTOS and splitData[3] not in tempImport):
                    tempImport.append(splitData[3])
                    proto.write("import \"" + splitData[3] + '.proto\";\n')


        # Import writer
        for i in copy_generated:
            splitData = i.split()
            # print("Generated Split: ", i.split())
            # print("split length:",len(i.split()))
            if(len(splitData) != 0):
                if(splitData[0] in PROTOS and splitData[0] not in tempImport):
                    tempImport.append(splitData[0])
                    proto.write("import \"" + splitData[0] + '.proto\";\n')
           
            if("repeated" in i):
                if(splitData[1] in PROTOS and splitData[1] not in tempImport):
                    tempImport.append(splitData[1])
                    proto.write("import \"" + splitData[1] + '.proto\";\n')

        proto.write("\n")
        proto.write("".join(generated))
        print("Generated " + data[1] + ".proto !")

def generateProto(proto,output):
    for i in listdir(output):
        PROTOS.append(i.replace(".proto",""))

    print("Total protos found: ",len(PROTOS))
    print("Loaded proto files: ",PROTOS)
    print("\nGenerating protocol files...\n")
    with open(proto,'r') as file:
        for line,value in enumerate(file):
            if(value.startswith("enum") or value.startswith("message")):
                if("}" in value):
                    # print(value.split() ,"<--------- ONE LINE PROTO")
                    oneLineProtoGen(value,proto,output)
                else:
                    # print(value.split() ,"<--------- MANY LINE PROTO")
                    generateManyLineProto(line,value,proto,output)

def help():
    print("""
            Proto packer / unpacker
Usage:

    proto.py --pack <proto directory> <outputfile>   - pack protos from a directory into a single one
    proto.py --unpack <proto> <output> [del OBF]  - unpack protos into output directory

Note:
    [del Obf] deletes obfuscated files when unpacking [THIS IS INACCURATE ONLY WORKS FINE FOR YAZAWAZI's GRASSGROWERS]
    unpack requires running the command twice in order to resolve imports
    """)

def delObfFiles(dir):
   for files in listdir(dir):
    if(files.strip('.proto')[0:11].isupper()):
        os.remove(dir+files)
        print("Deleted file: ",files)
   

if len(sys.argv) < 4:
    help()
else:
    if sys.argv[1].lower() == "--unpack":
        if(sys.argv[4].lower() == "true"):
            generateProto(sys.argv[2], sys.argv[3]+"\\")
            delObfFiles(sys.argv[3]+"\\")
        else:
            generateProto(sys.argv[2], sys.argv[3]+"\\")
    elif sys.argv[1].lower() == "--pack":
        packProtos(sys.argv[3], sys.argv[2]+"\\")
    else:
        help()
    