# Copyright © 2020-2022 Mrack
# Email: Mrack@qq.com
 
import argparse
import os
import subprocess
import sys
import shutil

api_template = \
    '''use flutter_rust_bridge::*;
pub fn hello() -> SyncReturn<String>  {
    SyncReturn("hello rust".to_string())
}
'''

lib_template = \
    '''mod api;
'''

call_template = \
    '''import 'dart:ffi';
import 'dart:io';
import 'bridge_generated.dart';
const base = 'rsapi';
final path = Platform.isWindows ? '$base.dll' : 'lib$base.so';
late final dylib = DynamicLibrary.open(path);
late final rsapi = RsapiImpl(dylib);'''

toml = '''

[lib]
name = "rsapi"
crate-type = ["cdylib"]'''


def run_command(command, cwd=None):
    return subprocess.Popen(
        command,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        cwd=  cwd if cwd!=None else os.path.dirname(os.path.realpath(__file__)),
    ).wait()


def write_file(filename, content, append=False):
    with open(filename, 'w' if not append else "a", encoding="utf-8") as f:
        f.write(content)


def genarater_rust():
    if os.access("rsapi", mode=os.F_OK):
        print("Rust directory already exists.")
        return
    if run_command("cargo new --lib rsapi") != 0:
        return
    if run_command("cargo add flutter_rust_bridge","rsapi") != 0:
        return
    write_file("rsapi/src/api.rs", api_template)
    write_file("rsapi/src/lib.rs", lib_template)
    write_file("rsapi/Cargo.toml", toml, True)
    if os.access("lib/rs", mode=os.F_OK):
        shutil.rmtree("lib/rs")
    os.mkdir("lib/rs", mode=os.F_OK)

    write_file("lib/rs/api.dart", call_template)


def genarater_lib(target, release):
    if run_command("cargo build {} --target {}".format((
            "--release" if release else ""), target),"rsapi") != 0:
        return
    lib = "librsapi.so"
    if "android" in target:
        path = 'android/app\src/main/jniLibs/{}/'.format(
            "arm64-v8a" if "aarch64" in target else "armeabi-v7a" if "armv7" in target else "x86_64" if "x86_64" in target else "")
        if not os.access(path, os.F_OK):
            os.makedirs(path)
    elif "windows" in target:
        lib = "rsapi.dll"
        path = 'build/windows/runner/{}/'.format(
            "Release" if release else "Debug",)
        if os.access(path, os.F_OK) ==0:
            run_command("flutter build windows {}".format("--release" if release else "--debug"))
            
    elif "linux" in target:
        path = 'build/linux/x64/{}/bundle/lib/'.format(
            "release" if release else "debug")
        if os.access(path, os.F_OK) ==0:
            run_command("flutter build linux {}".format("--release" if release else "--debug"))
    else:
        print(target + ' is not supported')
        return

    if os.access(path + lib,os.F_OK) != 0:
        os.remove(path + lib)
    shutil.copy("rsapi/target/{}/{}/{}".format(
        target, "release" if release else "debug", lib), path + lib)


def main():
    parser = argparse.ArgumentParser(
        description='rust_flutter_gen')
    parser.add_argument("--rust", default=False, action='count')
    parser.add_argument("--target", default='',help='''x86_64-unknown-linux-gnu, x86_64-pc-windows-msvc, aarch64-linux-android, armv7-linux-androideabi''')
    parser.add_argument("--release", default=False, action='count')
    parser.add_argument("--gen", default=False, action='count')
    args = parser.parse_args()

    if args.rust:
        genarater_rust()

    if args.gen:
        if run_command("flutter pub add flutter_rust_bridge") != 0:
            return
        if run_command("flutter pub add ffi") != 0:
            return
        if run_command("flutter pub add -d ffigen:^6.0.1") != 0:
            return
        run_command(
            "flutter_rust_bridge_codegen --rust-input ./rsapi/src/api.rs --dart-output ./lib/rs/bridge_generated.dart")
        
    if args.target:
        genarater_lib(args.target, args.release)


if __name__ == '__main__':
    main()