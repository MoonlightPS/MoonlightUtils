# ProtoUtils
Used for packing / unpacking .proto files

# Usage
1. for packing multiple .proto files into a single one:
```powershell
py proto.py --pack <proto directory> <outputfile>
```

2. for unpacking .proto files into multiple files:
```powershell
proto.py --unpack <proto> <output> <del OBF>
```
## Note
- **del Obf** flag deletes obfuscated files when unpacking [THIS IS INACCURATE ONLY WORKS FINE FOR YAZAWAZI's GRASSGROWERS]
- unpack requires running the command **TWICE** in order to resolve imports
