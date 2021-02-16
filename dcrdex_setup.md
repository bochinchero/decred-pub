# The Hitchhiker's Guide to the DCR DEX

This is an attempt at a newbie-friendly and easy to follow installation and configuration guide for a DCR DEX client instance.

A few points to keep in mind before we get too carried away:

*   DCR DEX currently requires clients to run full nodes of the supported chains - your system will require approximately ~25 GB of free space for trading DCR+BTC.
*   Your full nodes will need to be online and synched before you can trade, bitcoind in particular can take several hours to a few days depending on your internet speed and hardware.
*   Minimum trade size on [dex.decred.org](dex.decred.org) is currently set to 40 DCR to ensure on-chain fees are less than 1% of the trade. There is a one-off registration fee of 1 DCR.
*   Since all trades are settled on-chain, they can take several hours to complete - your node needs to stay online throughout this whole process.

## Prerequisites

In order to trade on the DEX client you will be essentially running hot wallets. As such, it is recommended that you use a dedicated system specific for this task. 

This can be done by using dedicated computer, a virtual machine or even a Raspberry Pi, with the caveat that you [would want to boot from an SSD](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md) since SD cards degrade over time and will eventually fail.

If you don't know what you are doing, I'd suggest going with the virtual machine route - below are some tutorials for Ubuntu which is relatively newbie friendly.

*   [How to create an Ubuntu VM on Windows 10 w/ Hyper-V](https://www.thomasmaurer.ch/2019/06/how-to-create-an-ubuntu-vm-on-windows-10/)
*   [How to Install Ubuntu on VirtualBox](https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/)

Once you're up and running with we can move on to the next steps.

## Installation

Once your machine is set up you will need to install the Decred CLI tools.

Import the Decred Release Signing Key in GnuPG.

`gpg --keyserver pgp.mit.edu --recv-keys F516ADB7A069852C7C28A02D6D897EDF518A031D`

Download the installer, manifest, and signature files.

`wget https://github.com/decred/decred-release/releases/download/v1.6.0/{dcrinstall-linux-amd64-v1.6.0,manifest-dcrinstall-v1.6.0.txt,manifest-dcrinstall-v1.6.0.txt.asc}`

Verify the manifest. The output from this command should say “Good signature from Decred Release [**release@decred.org**](mailto:release@decred.org)”. Warnings about the key not being certified with a trusted signature can be ignored.

`gpg --verify manifest-dcrinstall-v1.6.0.txt.asc`

Verify the SHA-256 hash in the manifest matches that of the binary - the following two commands should have the same output.

`sha256sum dcrinstall-linux-amd64-v1.6.0`

`grep dcrinstall-linux-amd64-v1.6.0 manifest-dcrinstall-v1.6.0.txt`

Make the binary executable.

`chmod +x dcrinstall-linux-amd64-v1.6.0`

Run it to install the Decred CLI tools and to create your wallet.

`./dcrinstall-linux-amd64-v1.6.0`

Add the path to the Decred binaries to your `.profile`.

`echo "PATH=~/decred:$PATH" >> ~/.profile && source ~/.profile`
