# The Hitchhiker's Guide to the DCR DEX

This is an attempt at a newbie-friendly and easy to follow installation and configuration guide for a DCR DEX client and required nodes.

A few points to keep in mind before we get too carried away:

*   DCR DEX currently requires clients to run full nodes of the supported chains - your system will require approximately ~25 GB of free space for trading DCR & BTC.
*   Your full nodes will need to be online and synched before you can trade, bitcoind in particular can take several hours to a few days depending on your internet speed and hardware.
*   [dex.decred.org](dex.decred.org) has a one-off registration fee of 1 DCR.
*   The minimum trade size on [dex.decred.org](dex.decred.org) is currently set to 40 DCR to ensure on-chain fees are less than 1% of the smallest possible trade on DCR/BTC.
*   Since all trades are settled on-chain, they can take several hours to complete - your machine needs to stay online throughout this whole process.

## Prerequisites

In order to trade on the DEX client you will be essentially running hot wallets. As such, it is recommended that you use a dedicated system specific for this task. 

This can be done by using dedicated computer, a virtual machine or even a Raspberry Pi, with the caveat that on the latter you [would want to boot from an SSD](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md) since SD cards degrade over time and will eventually fail.

If you don't know what you are doing, I'd suggest going with the virtual machine route - below are some tutorials for Ubuntu which is relatively newbie friendly.

*   [How to create an Ubuntu VM on Windows 10 w/ Hyper-V](https://www.thomasmaurer.ch/2019/06/how-to-create-an-ubuntu-vm-on-windows-10/)
*   [How to Install Ubuntu on VirtualBox](https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/)

As far as VM specs, I'd suggest at least 6GB of RAM, 2 cores and a 30 GB drive - it's also recommended that you have a swap partition of at least 2 GB. 

## Installation

With your machine set up, we can start installing the Decred CLI tools.

Open a terminal window by pressing **Ctrl + Alt + T**

Import the Decred Release Signing Key in GnuPG.

`gpg --keyserver pgp.mit.edu --recv-keys F516ADB7A069852C7C28A02D6D897EDF518A031D`

Download the installer, manifest, and signature files. If you are using a Raspberry Pi, you'll need the arm64 files instead.

`wget https://github.com/decred/decred-release/releases/download/v1.6.0/{dcrinstall-linux-amd64-v1.6.0,dcrinstall-v1.6.0-manifest.txt,dcrinstall-v1.6.0-manifest.txt.asc}`

Verify the manifest. The output from this command should say “Good signature from Decred Release [**release@decred.org**](mailto:release@decred.org)”. Warnings about the key not being certified with a trusted signature can be ignored.

`gpg --verify dcrinstall-v1.6.0-manifest.txt.asc`

Verify the SHA-256 hash in the manifest matches that of the binary - the following two commands should have the same output.

`sha256sum dcrinstall-linux-amd64-v1.6.0`

`grep dcrinstall-linux-amd64-v1.6.0 dcrinstall-v1.6.0-manifest.txt`

Make the binary executable.

`chmod +x dcrinstall-linux-amd64-v1.6.0`

Run it to install the Decred CLI tools, the DEX client and create your Decred wallet.

`./dcrinstall-linux-amd64-v1.6.0 --dcrdex`

As part of the wallet creation process, you will be given a sequence of 33 words known as a seed phrase. Write it down and store it in a safe place and **DO NOT SHARE IT WITH ANYONE**. For more information see the [Wallets & Seeds](https://docs.decred.org/faq/wallets-and-seeds/) section of the Decred documentation.

Add the path to the Decred binaries to your `.profile` for easier management.

`echo "PATH=~/decred:$PATH" >> ~/.profile && source ~/.profile`

## Configuration

To make life easier, we can use tmux to manage multiple terminal sessions - first, lets verify that you have it installed.

`sudo apt-get install tmux`

Now we'll create a bash script called dcrdex.sh which will start a tmux session for each application, starting dcrd, bitcoind, dcrwallet and dexc.

`echo "tmux new -d -s dcrd 'dcrd'; tmux new -d -s dcrwallet 'dcrwallet'; tmux new -d -s bitcoind 'bitcoind'; tmux new -d -s dexc 'dexc'" > ~/dcrdex.sh;`

Make it executable

`chmod +x ~/dcrdex.sh`

You can start all daemons by running

`~/dcrdex.sh`

To check the status of the different processes you can attach the relevant session by using the following commands:

* Decred full node: `tmux attach -t dcrd` 

* Bitcoin full node & Wallet: `tmux attach -t bitcoind`

* DCRDEX client: `tmux attach -t dexc` 
 
* Decred Wallet: `tmux attach -t dcrwallet` 

When dcrwallet is started for the first time it will prompt to enter your passphrase.

You can detach from tmux sessions by pressing **CTRL+B**, then **D**.

At this point your nodes will be synching in the background and you will see messages like this in bitcoind:

> 2021-02-16T19:30:03Z UpdateTip: new best=00000000000005212a4f8eadc418abfff2b81e906c80d6e39195aa1a04e4cc32 height=185627 version=0x00000001 log2_work=68.295222 tx=4369721 date='2012-06-21T20:32:25Z' progress=0.007177 cache=27.2MiB(166302txo)

and this in dcrd:

> 2021-02-16 19:30:51.014 [INF] BMGR: Processed 837 blocks in the last 11.16s (8863 transactions, 4305 tickets, 4143 votes, 73 revocations, height 130940, 2017-05-07 00:19:37 +0100 BST)

