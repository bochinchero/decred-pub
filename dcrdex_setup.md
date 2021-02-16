# A newbie friendly guide to the DCR DEX

This is an attempt at a simple to understand installation and configuration guide for a DCR DEX client instance.

A few points to keep in mind before we get too carried away:

*   DCR DEX currently requires clients to run full nodes of the supported chains - your system will require approximately ~30 GB of free space for trading DCR+BTC.
*   Your nodes will need to be online and fully synched before you can trade, this can take several hours to days depending on your internet speed and hardware.
*   Minimum trade size on dex.decred.org is currently set to 40 DCR, this is to make on-chain fees \<1%. Registration fee is 1 DCR.
*   Since all trades are settled on-chain, they can take several hours to complete - your node needs to stay online.

## Prerequisites

Taking into account that in order to trade on the DEX client you will be running hot wallets, it is suggested that you set up a system specifically for task. 

This can be done by using dedicated computer, a virtual machine or even a Raspberry Pi, with the caveat that you would want to boot from an SSD or HD.

If you don't know what you are doing, I'd suggest going with the virtual machine route.

*   [How to Install Ubuntu on VirtualBox](https://www.freecodecamp.org/news/how-to-install-ubuntu-with-oracle-virtualbox/)
*   [Using a Raspberry Pi w/ USB Mass Storage](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md)
