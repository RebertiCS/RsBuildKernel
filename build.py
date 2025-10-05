#!/usr/bin/env python3
"""Main file to get and build android linux kernel"""
import os
import re
import subprocess
from datetime import datetime
import time

from pathlib import Path
import argparse

from dotenv import load_dotenv

load_dotenv()

PWD = os.getcwd()

KERNEL_URL = os.getenv("KERNEL_URL")
KERNEL_BRANCH = os.getenv("KERNEL_BRANCH")
DEFCONFIG = os.getenv("DEFCONFIG")

PREBUILT_URL = os.getenv("PREBUILT_URL")
PREBUILT_NAME = re.search(r"(?<=\/)([^\/]+)(?=\/?$)", PREBUILT_URL).group(0)
SRC_DIR = f"{PWD}/kernel"

MAKE_PARAMS = None


def main():
    """Main."""
    parser = argparse.ArgumentParser(
        prog="build.py",
        description="Automated android kernel build.",
        epilog="RsKernelBuild - v1.0 - GPLv2 RebertiCS @ 2025.",
    )

    parser.add_argument(
        "-c",
        "--clean",
        help="Run mrproper before building kernel.",
        action="store_true",
    )

    args = parser.parse_args()

    MAKE_PARAMS = setup_env()
    build_defconfig_cmd = ["make", DEFCONFIG] + MAKE_PARAMS
    build_cmd = ["make"] + MAKE_PARAMS

    os.chdir(SRC_DIR)

    if args.clean:
        print(
            f"[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] Running mrproper for cleanup."
        )
        subprocess.run(["make", "-C", SRC_DIR, "mrproper"])

    # Building Defconfig
    print(f"[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] Building {DEFCONFIG}")
    subprocess.run(build_defconfig_cmd)

    # Building Kernel
    print(f"[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] Compiling Kernel.")
    start_time = time.time()

    subprocess.run(build_cmd)

    end_time = round(time.time() - start_time, 5)

    print(
        f"[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] Compiler finished, took: {end_time}s"
    )


def setup_env():
    """Setup env toolchains for compiling"""

    tc_dir = f"{PWD}/toolchain/clang"
    jobs = subprocess.run(["nproc"], capture_output=True, text=True).stdout.replace(
        "\n", ""
    )

    os.environ["PATH"] = tc_dir + "/bin:" + os.getenv("PATH")

    print(
        "RsBuild: \n",
        f" - Kernel Repo: {KERNEL_URL}\n",
        f" - Kernel Branch: {KERNEL_BRANCH}\n",
        f" - Prebuilt: {PREBUILT_NAME}\n",
        f" - Defconfig: {DEFCONFIG}\n",
    )
    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    if not Path(f"tmp/{PREBUILT_NAME}").is_file():
        # Donwload toolchain from PREBUILT_URL
        subprocess.run(["wget", "-c", PREBUILT_URL, "-O", f"tmp/{PREBUILT_NAME}"])

    if not os.path.exists("toolchain"):
        os.makedirs("toolchain")

    if not os.path.exists("toolchain/clang"):
        print("toolchain/clang not found, creating folder.")
        os.makedirs("toolchain/clang")

        print(f"Extracting {PREBUILT_NAME} to toolchain/clang.")
        # Extract toolchain
        subprocess.run(["tar", "-xzf", f"tmp/{PREBUILT_NAME}", "-C", "toolchain/clang"])

    if not os.path.exists("kernel"):
        print("Cloning kernel source code.")
        # Extract toolchain
        subprocess.run(
            [
                "git",
                "clone",
                "--recurse-submodules",
                "--depth",
                "1",
                "--branch",
                KERNEL_BRANCH,
                KERNEL_URL,
                "./kernel",
            ]
        )

    MAKE_PARAMS = [
        "-j",
        jobs,
        "-C",
        SRC_DIR,
        f"O={SRC_DIR}/out",
        f"CROSS_COMPILE={tc_dir}/bin/llvm-",
        "ARCH=arm64",
        "CC=clang",
        "CLANG_TRIPLE=aarch64-linux-gnu-",
        "LLVM=1",
        "CONFIG_SECTION_MISMATCH_WARN_ONLY=y",
        "CONFIG_FRAME_WARN=0",
    ]

    return MAKE_PARAMS


if __name__ == "__main__":
    main()
