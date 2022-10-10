# MoonlightUtils
Utility scripts needed for MoonlightTS

### Command to compile game.proto
```bash
protoc --plugin=protoc-gen-ts_proto=.\node_modules\.bin\protoc-gen-ts_proto.cmd --ts_proto_out=. --ts_proto_opt=esModuleInterop=true game.proto
```

