# The Hitchhiker's Guide to the DCRDEX

This is an attempt at a more newbie friendly and easy to follow installation and configuration guide for a DCRDEX client and required nodes.

A few points to keep in mind before going any further:

*   DCRDEX currently requires clients to run full nodes of the supported chains - your system will require approximately ~25 GB of free space for trading DCR & BTC.
*   Your full nodes will need to be online and synched before you can trade, bitcoind in particular can take several hours to a few days depending on your internet speed and hardware.
*   [dex.decred.org](dex.decred.org) has a one-off registration fee of 1 DCR.
*   The minimum trade size on [dex.decred.org](dex.decred.org) is currently set to 40 DCR to ensure on-chain fees are less than 1% of the smallest possible trade on DCR/BTC.
*   Since all trades are settled on-chain, they can take several hours to complete - your machine needs to stay online throughout this whole process. A loss of internet connectivity for more than 20 hours during trade settlement has the potential to result in lost funds.
*   There is a reputation system in place which limits the amount of ordering you can initially do. Start with smaller orders to build your reputation up.

## Prerequisites

In order to trade on the DEX client you will be essentially running hot wallets. As such, it is recommended that you use a dedicated system specific for this task. 

This can be done by a virtual machine, a dedicated computer or even a Raspberry Pi, with the caveat that on the latter you [would want to boot from an SSD](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md) since SD cards degrade over time and will eventually fail.

As far as machine specifications go, I'd suggest as a minimum 4GB of RAM, 2 cores and a 35 GB drive - it's also recommended that you have a swap partition of at least 2 GB.

A machine with these specifications took about 2 days to syncronise the bitcoin blockchain, better specs will considerably speed this up.

Something else to keep in mind,  if you are using a virtual machine **it will only be as secure as the host system that you are running it on**. Consider using a dedicated computer if you are planning on trading and/or holding a significant amount of funds in these wallets for an extended period of time.

## Installation

With your machine set up, we can start installing the Decred CLI tools.

Open a terminal window by pressing **Ctrl + Alt + T**

Ensure you're in your home folder.

    cd ~

Import the Decred Release Signing Key in GnuPG.

    gpg --keyserver pgp.mit.edu --recv-keys F516ADB7A069852C7C28A02D6D897EDF518A031D

#### If you are using a dedicated computer or a virtual machine (amd64)

Download the installer, manifest, and signature files.

    wget https://github.com/decred/decred-release/releases/download/v1.6.0/{dcrinstall-linux-amd64-v1.6.0,dcrinstall-v1.6.0-manifest.txt,dcrinstall-v1.6.0-manifest.txt.asc}

Verify the manifest. The output from this command should say “Good signature from Decred Release [**release@decred.org**](mailto:release@decred.org)”. Warnings about the key not being certified with a trusted signature can be ignored.

    gpg --verify dcrinstall-v1.6.0-manifest.txt.asc

Verify the SHA-256 hash in the manifest matches that of the binary - the following two commands should have the same output.

    sha256sum dcrinstall-linux-amd64-v1.6.0

    grep dcrinstall-linux-amd64-v1.6.0 dcrinstall-v1.6.0-manifest.txt

Make the binary executable.

    chmod +x dcrinstall-linux-amd64-v1.6.0

Run it to install the Decred CLI tools, the DEX client and create your Decred wallet.

    ./dcrinstall-linux-amd64-v1.6.0 --dcrdex

#### If you are using a Raspberry Pi (arm64)

Download the installer, manifest, and signature files.

    wget https://github.com/decred/decred-release/releases/download/v1.6.0/{dcrinstall-linux-arm64-v1.6.0,dcrinstall-v1.6.0-manifest.txt,dcrinstall-v1.6.0-manifest.txt.asc}

Verify the manifest. The output from this command should say “Good signature from Decred Release [**release@decred.org**](mailto:release@decred.org)”. Warnings about the key not being certified with a trusted signature can be ignored.

    gpg --verify dcrinstall-v1.6.0-manifest.txt.asc

Verify the SHA-256 hash in the manifest matches that of the binary - the following two commands should have the same output.

    sha256sum dcrinstall-linux-arm64-v1.6.0

    grep dcrinstall-linux-arm64-v1.6.0 dcrinstall-v1.6.0-manifest.txt

Make the binary executable.

    chmod +x dcrinstall-linux-arm64-v1.6.0

Run it to install the Decred CLI tools, the DEX client and create your Decred wallet.

    ./dcrinstall-linux-arm64-v1.6.0 --dcrdex

### Decred Wallet Creation

A Decred wallet will be created as part of the installation process, you will be given a sequence of 33 words known as a seed phrase. Write it down and store it in a safe place and **DO NOT SHARE IT WITH ANYONE**. For more information see the [Wallets & Seeds](https://docs.decred.org/faq/wallets-and-seeds/) section of the Decred documentation.

## Configuration and Registration

Add the path to the Decred binaries to your `.profile` for easier management.

    echo "PATH=~/decred:$PATH" >> ~/.profile && source ~/.profile

To make life easier, you can use tmux to manage multiple terminal sessions - first, lets verify that you have it installed.

    sudo apt-get update
    sudo apt-get install tmux

Now we'll create a bash script called dcrdex.sh which will start a tmux session for each application, starting dcrd, bitcoind, dcrwallet and dexc.

    echo "tmux new -d -s dcrd 'dcrd'; tmux new -d -s dcrwallet 'dcrwallet'; tmux new -d -s bitcoind 'bitcoind'; tmux new -d -s dexc 'dexc'" > ~/dcrdex.sh;

Make it executable

    chmod +x ~/dcrdex.sh

You can start all daemons by running

    ~/dcrdex.sh

To check the status of the different processes you can attach the relevant session by using the following commands:

* Decred full node:

      tmux attach -t dcrd

* Bitcoin full node & Wallet:

      tmux attach -t bitcoind

* DCRDEX client
 
      tmux attach -t dexc

* Decred Wallet:

      tmux attach -t dcrwallet

Attach the dcrwallet, when it starts for the first time it will prompt to enter your passphrase.

You can detach from tmux sessions by pressing **CTRL + B**, then **D**.

At this point your nodes will be synching in the background and you will see messages like this in bitcoind:

> 2021-02-16T19:30:03Z UpdateTip: new best=00000000000005212a4f8eadc418abfff2b81e906c80d6e39195aa1a04e4cc32 height=185627 version=0x00000001 log2_work=68.295222 tx=4369721 date='2012-06-21T20:32:25Z' progress=0.007177 cache=27.2MiB(166302txo)

and this in dcrd:

> 2021-02-16 19:30:51.014 [INF] BMGR: Processed 837 blocks in the last 11.16s (8863 transactions, 4305 tickets, 4143 votes, 73 revocations, height 130940, 2017-05-07 00:19:37 +0100 BST)

To verify that your Decred node is fully synched you can use the following command and compare against the latest block on [dcrdata.org](www.dcrdata.org).

        dcrctl getbestblock
        
For Bitcoin, you can use the following command and compare with [blockcypher](https://live.blockcypher.com/btc/) or your block explorer of choice.

        bitcoin-cli getblockcount

### Decred Trading Wallet Configuration

It's recommended that within the Decred wallet you have a specific account for trading on the DEX, you can create one with the following command:

        dcrctl --wallet createnewaccount dex

At the time of writing, [dex.decred.org](dex.decred.org) has a registration fee of 1 DCR. You will now need to fund this newly created account and deposit at least enough DCR to cover the registration fee and on-chain fees for the registration transaction. You can also transfer more if you want to sell DCR - just keep in mind that the minimum lot size is currently 40 DCR. 

Generate a new receiving address in the DEX account with the following command:

        dcrctl --wallet getnewaddress dex

### Bitcoin Trading Wallet Configuration

Let's now create a trading wallet for bitcoin:

        bitcoin-cli createwallet dex

It is recommended that you password-protect your Bitcoin trading wallet. By using the following command you'll be able enter a passphrase without echoing it in the terminal:

        read -s BTCPASS
        
Now enter your passphrase and press return. By executing the following command the bitcoin dex wallet will now be encrypted with this passphrase:

        bitcoin-cli -rpcwallet=dex encryptwallet $BTCPASS
        
You will see the following message:

> wallet encrypted; The keypool has been flushed and a new HD seed was generated (if you are using HD). You need to make a new backup.

To verify that you've recorded it correctly, enter your passphrase again:

        read -s VERIFYPASS
 
 And try unlocking your bitcoin dex wallet for one second.
 
        bitcoin-cli -rpcwallet=dex walletpassphrase $VERIFYPASS 1
      
You won't see any positive feedback if the passphrases match, but you will see the following error if they don't

> Error: The wallet passphrase entered was incorrect.

Now we need to modfiy the configuration file to make bitcoind load the dex wallet automatically at startup:

        echo 'wallet=dex' >> ~/.bitcoin/bitcoin.conf
        
### DEX Configuration

The dex client should already be running in the background.

* Open a web browser and navigate to **localhost:5758**.

![omnibar-client](https://github.com/decred/dcrdex/raw/master/docs/images/omnibar-client.png)
        
* Create your DEX client application password. You will use this password to perform all future security-sensitive client operations, including registering, signing in, and trading.

![client-pw](https://github.com/decred/dcrdex/blob/master/docs/images/client-pw.png)

* Connect to your Decred wallet. The client will auto-fill most of your wallet settings, but you will need to specify the account name, which we set up as **dex** above. Enter the wallet password, which is the dcrwallet passphrase you entered during the dcrinstall process and the DEX client app password you created in the previous step.

![decred-reg](https://github.com/decred/dcrdex/raw/master/docs/images/decred-reg.png)

* Enter the dex address: **dex.decred.org**.

![add-dex-reg](https://github.com/decred/dcrdex/raw/master/docs/images/add-dex-reg.png)

* Check the registration fee, and enter your password one more time to authorize payment - this will deduct the registration fee from your **dex** decred account.

![confirm-reg](https://github.com/decred/dcrdex/blob/master/docs/images/confirm-reg.png)

* On the markets view, while you're waiting for confirmations on your registration fee, add a Bitcoin wallet. You'll need to specify the wallet name, which we created as **dex** in the previous steps. Enter the wallet password you set up with bitcoin-cli and the DEX client app password.

![create-btc.png](https://github.com/decred/dcrdex/blob/master/docs/images/create-btc.png)

Once your registration fee has been confirmed you should be ready to trade.
     
    
