# rust_flutter_gen

### 简介
在Flutter项目中添加Rust的支持

### 使用说明

* 1 创建Flutter项目 ``` flutter create cm_rs ```

* 2 rust_flutter_gen.py 放入 cm_rs目录

* 3 添加Rust lib库 ``` python rust_flutter_gen.py --rust ```

* 4 创建ffi代码 ``` python rust_flutter_gen.py --gen ```

* 5 构建平台链接库 ``` python rust_flutter_gen.py --target=x86_64-pc-windows-msvc [target]```

``` 目前支持 x86_64-unknown-linux-gnu, x86_64-pc-windows-msvc, aarch64-linux-android, armv7-linux-androideabi ```

* 6 rsapi 调用库函数 ``` rsapi.hello() ```


* 7 运行 ``` flutter run ```






> High-level memory-safe binding generator for Flutter/Dart <-> Rust   
> https://github.com/fzyzcjy/flutter_rust_bridge  
> https://cjycode.com/flutter_rust_bridge/