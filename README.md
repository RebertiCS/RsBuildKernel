# RsBuildKernel
Toolchain to build the android kernel

## Usage:
### Run Options:
run `python build.py -h`

### Configuration:
Configure `.env` with the information needed:

``` sh
KERNEL_URL = '<GIT KERNEL REPO>'
KERNEL_BRANCH = '<GIT BRANCH>'
PREBUILT_URL = '<PREBUILT TAR URL>'
DEFCONFIG = '<DEVICE DEFCONFIG>'
```

## Requirements

### Debian:

``` sh
sudo apt install git-core gnupg flex bison build-essential zip curl wget zlib1g-dev libc6-dev-i386 x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig clang axel xz-utils make ccache openssl libssl-dev bc gcc-aarch64-linux-gnu python-is-python3 android-tools-adb android-tools-fastboot
```

### Fedora

``` sh
sudo dnf install git-core gnupg flex bison zip curl wget xsltproc unzip fontconfig clang axel xz make ccache openssl openssl-devel openssl-devel-engine bc gcc-aarch64-linux-gnu python-is-python3 android-tools
```

### Python:

``` sh
pip install dotenv
```

