# The Hitchhiker's Guide to the DCR DEX

This is an attempt at a newbie-friendly and easy to follow installation and configuration guide for a DCR DEX client instance.

A few points to keep in mind before we get too carried away:

*   DCR DEX currently requires clients to run full nodes of the supported chains - your system will require approximately ~25 GB of free space for trading DCR+BTC.
*   Your nodes will need to be online and fully synched before you can trade, this can take several hours to days depending on your internet speed and hardware.
*   Minimum trade size on [dex.decred.org](dex.decred.org) is currently set to 40 DCR to ensure on-chain fees are less than 1% of the trade. The one-off registration fee is 1 DCR.
*   Since all trades are settled on-chain, they can take several hours to complete - your node needs to stay online.

## Prerequisites

Taking into account that in order to trade on the DEX client you will be running hot wallets, it is suggested that you set up a system specifically for task. 

This can be done by using dedicated computer (best), a virtual machine or even a Raspberry Pi, with the caveat that you [would want to boot from an SSD](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md).

If you don't know what you are doing, I'd suggest going with the virtual machine route - below are some tutorials for Ubuntu which is relatively newbie friendly.

*   [How to create an Ubuntu VM on Windows 10 w/ Hyper-V](https://www.thomasmaurer.ch/2019/06/how-to-create-an-ubuntu-vm-on-windows-10/)
*   [How to Install Ubuntu on VirtualBox](https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/)

Once you're up and running with your system we can move on to the next steps.

## Installation

First lets open a terminal and ensure you are in the home folder:

```
cd ~
```

Get latest version of dcrinstall - if you are using an VPS/VM that would usually be:  
      
`wget https://github.com/decred/decred-release/releases/download/v1.6.0/dcrinstall-linux-amd64-v1.6.0`

For a raspberry pi you would use:

wget https://github.com/decred/decred-release/releases/download/v1.6.0/dcrinstall-linux-arm-v1.6.0

Change permissions to executable:

chmod +x dcrinstall-linux-amd64-v1.6.0

execute dcrinstall

./dcrinstall-linux-amd64-v1.6.0

This will download dcrd, dcrwallet and dcrlnd - as part of the process it will also create a new wallet within dcrwallet and generate the seed phrase, although this is not the  wallet you will be using for your routing node (as dcrlnd creates a separate one).
