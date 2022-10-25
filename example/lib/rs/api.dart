import 'dart:ffi';
import 'dart:io';
import 'bridge_generated.dart';
const base = 'rsapi';
final path = Platform.isWindows ? '$base.dll' : 'lib$base.so';
late final dylib = DynamicLibrary.open(path);
late final rsapi = RsapiImpl(dylib);