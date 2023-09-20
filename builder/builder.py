import os
import sys
import json
import shutil
import subprocess

import toolchain

# read build_config.json
build_config = ''
with open("build_config.json", "r") as file:
    build_config = json.load(file)

# spawn a subprocess
def spawn(argv):
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    while p.poll() == None:
        print(p.stdout.readline(), end='')

    return p.poll()

##### STM32 build and flash process START #####
def build_stm32():
    print("INFO: building TMA-1 STM32 binary...")

    # step into STM32CubeMX project folder
    os.chdir('../device/TMA-1')

    # set build environment variables
    os.environ["ENABLE_TELEMETRY"] = '1' if build_config["STM32"]["output"]["telemetry"] else '0'
    os.environ["ENABLE_SERIAL"]    = '1' if build_config["STM32"]["output"]["serial"] else '0'

    os.environ["ENABLE_MONITOR_CAN"]           = '1' if build_config["STM32"]["sensor"]["can"] else '0'
    os.environ["ENABLE_MONITOR_DIGITAL"]       = '1' if build_config["STM32"]["sensor"]["digital"] else '0'
    os.environ["ENABLE_MONITOR_ANALOG"]        = '1' if build_config["STM32"]["sensor"]["analog"] else '0'
    os.environ["ENABLE_MONITOR_PULSE"]         = '1' if build_config["STM32"]["sensor"]["pulse"] else '0'
    os.environ["ENABLE_MONITOR_ACCELEROMETER"] = '1' if build_config["STM32"]["sensor"]["accelerometer"] else '0'
    os.environ["ENABLE_MONITOR_GPS"]           = '1' if build_config["STM32"]["sensor"]["gps"] else '0'

    os.environ["DEBUG_MODE"] = '1' if build_config["STM32"]["debug"]["debug_mode"] else '0'

    os.environ["DEBUG"] = '0' if build_config["STM32"]["debug"]["release_build"] else '1'
    os.environ["OPT"] = '-O2' if build_config["STM32"]["debug"]["release_build"] else '-Og'

    # build
    ret = spawn(['make'])

    if ret != 0:
        print("\nERROR: build job failed. terminating.")
        return -1

    # step back to builder
    os.chdir('../../builder')

    # move target executable
    if os.path.exists('../device/TMA-1/build/TMA-1.elf'):
        os.makedirs('./build', exist_ok=True)
        shutil.copyfile('../device/TMA-1/build/TMA-1.elf', './build/TMA-1.elf')
        print("INFO: build of TMA-1 STM32 binary completed! binary copied to build/TMA-1.elf")
        return 0

    else:
        print("\nERROR: No binary found for STM32. terminating.")
        return -1


def flash_stm32():
    print("INFO: flashing TMA-1 STM32 binary...")

    retry = 0
    ret = spawn(['openocd', '-f', './config/TMA-1.cfg'])

    while ret != 0 and retry < 3:
        retry += 1
        print(f"ERROR: flashing failed. retry count: {retry}")
        ret = spawn(['openocd', '-f', './config/TMA-1.cfg'])

    if ret != 0:
        print("\nERROR: max retry count reached. terminating.")
        return -1

    print('INFO: TMA-1 STM32 binary successfully flashed. please recyle the power.')
    return 0
##### STM32 build and flash process END #####

##### ESP32 build and flash process START #####
def build_esp32():
    return 0

def flash_esp32():
    return 0
##### ESP32 build and flash process END #####

# Monolith TMA-1 software build and flash process
def build():
    print("INFO: checking toolchain...")
    if toolchain.validate() != 0:
        print("\nERROR: toolchain is corrupt. please delete builder/toolchain/.cache and retry.")
        return -1

    if build_stm32() != 0:
        print("\nERROR: build of TMA-1 STM32 binary failed. please delete builder/toolchain and retry.")

    elif flash_stm32() != 0:
        print("\nERROR: flashing of TMA-1 STM32 binary failed. please check debugger and retry.")
    if build_esp32() != 0:
        print("\nERROR: build of TMA-1 ESP32 binary failed. please delete builder/toolchain and retry.")

    elif flash_esp32() != 0:
        print("\nERROR: flashing of TMA-1 ESP32 binary failed. please check debugger and retry.")

# clean build directories
def clean():
    # build directory
    print("cleaning ./build...")
    if os.path.exists('./build'):
        shutil.rmtree('./build')

    # STM32CubeMX build directory
    print("cleaning ./device/TMA-1/build...")
    if os.path.exists('../device/TMA-1/build'):
        shutil.rmtree('../device/TMA-1/build')

    print("clean done!")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        build()
    elif sys.argv[1] == "build":
        build()
    elif sys.argv[1] == "clean":
        clean()
    else:
        print(f'ERROR: unknown command {sys.argv[1]}')
