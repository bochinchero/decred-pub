This guide assumes you already have a linux host and access to a terminal.

Keep in mind that if you want your node to be a public routing node you'll need to open the dcrlnd p2p listening port, by default this is 9735.
You could also make the dcrd node public by opening port 9108.

It is also recommended that your host has at least a 2G swap partition set up.

Some additional information on security and safety:

* [How to harden SSH in Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-harden-openssh-on-ubuntu-18-04)
* [How to setup a firewall with ufw in Ubuntu & Debian](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server)
* [dclrnd safety guideliens](https://github.com/decred/dcrlnd/blob/master/docs/safety.md)

## Decred Installation

First lets go to your home folder:

	cd ~

Get latest version of dcrinstall - if you are using an VPS/VM that would ussually be:
    	
	wget https://github.com/decred/decred-release/releases/download/v1.6.0/dcrinstall-linux-amd64-v1.6.0

For a raspberry pi you would use:

	wget https://github.com/decred/decred-release/releases/download/v1.6.0/dcrinstall-linux-arm-v1.6.0

Change permissions to executable:

	chmod +x dcrinstall-linux-amd64-v1.6.0

execute dcrinstall

	./dcrinstall-linux-amd64-v1.6.0

This will download dcrd, dcrwallet and dcrlnd - as part of the process it will also create a new wallet within dcrwallet and generate the seed phrase, although this is not the  wallet you will be using for your routing node (as dcrlnd creates a separate one).

## Decred Full Node
### Configuration

The dcrd full node needs to have the **txindex** option enabled, so modify the dcrd.conf by running the following command:

	nano ~/.dcrd/dcrd.conf

Scroll down to **Optional Indexes** section and uncomment (remove the ;) following setting:
   
	; Build and maintain a full hash-based transaction index which makes all
	; transactions available via the getrawtransaction RPC.
	txindex=1


Save the configuration file by presssing **CTRL + X**, then **Y**, then **Enter**.

### Running dcrd

I like to use tmux to have different consoles within a single ssh session, you can create a new tmux session for dcrd with the following command. This step is not required if you have desktop access, you can just create a new terminal instead.

	tmux new -s dcrd

this will give you a brand new terminal that you can check when needed, now you can start dcrd:

	~/decred/dcrd

At this point the decred blockchain will start downloading and the node will be synchronising, this process usually takes a few hours depending on the hardware/broadband speed.

You can detach from the tmux session by pressing **CTRL+B**, then **D**. If you need to check back in to see the status of the node you can reattach the session by using the following command:

	tmux attach-session -t dcrd

To know if your node has fully synched, look at the 'height' in the last message in the dcrd session and compare against the latest block on dcrdata.org.

## Decred Lightning Network Daemon 

### Configuration

Settings for your dcrlnd node can be modified by opening up the dcrlnd.conf with the following command:

	nano ~/.dcrlnd/dcrlnd.conf

In my case, I want this node to be public and it will be running on a VPS with a static ip address. 
The following setting needs to be modified:

	; Adding an external IP will advertise your node to the network. This signals
	; that your node is available to accept incoming channels. If you don't wish to
	; advertise your node, this value doesn't need to be set. Unless specified
	; (with host:port notation), the default port (9735) will be added to the
	; address.
	 externalip=<enter your address here>

Further down, you can also modify the alias of the node and the colour that it will be displayed in on explorers.

If you plan on running Ride The Lightning on the same host to manage your node, you will also need to enable listening for REST connections:

	; All ipv4 interfaces on port 8080:
	restlisten=localhost:8080

### Running

Create a new tmux session or open a new terminal for dcrlnd
	 
	 tmux new -s dcrlnd

now you can start dcrlnd:
	
	~/decred/dcrlnd

You will be promptedforwarded to create and unlock the wallet:

	LTND: Waiting for wallet encryption password. Use `dcrlncli create` to create a wallet, `dcrlncli unlock` to unlock an existing wallet, or `dcrlncli changepassword` to change the password of an existing wallet and unlock it.

Detach from the session by pressing **CTRL+B**, then **D**. 

The next step is to use dcrlncli to create a wallet, this will be your main wallet for funding lightning channels and is different from the dcrwallet configured during installation,  I cannot stress enoguh that you have to **write down the seed**.

	~/decred/dcrlncli create

Go back to the dcrlnd terminal by attaching the session:

	 tmux attach -t dcrlnd

You will now see it updating and synchronising. Once fully synchronised you'll be ready to start funding the wallet and opening channels.

As of 1.6.0 there is no seeder for dcrlnd, so you won't be connected on the network until you add a peer


### Command line usage

At this stage you're basically set to start

You can generate a new address by using the command below:

	~/decred/dcrlncli newaddress

check your balance:

	~/decred/dcrlncli walletbalance

and send coins to another wallet:

	~/decred/dcrlncli sendcoins < address > < amount >

connect to an online node:

	~/decred/dcrlncli connect <node pubkey @ address : port >
	
open a channel:

	~/decred/dcrlncli openchannel < node pubkey > < amount >


## Ride the Lightning

An obvious disclaimer here, RTL is developed for Bitcoin. However given that dcrlnd is a fork of upstream lnd and uses the same BOLTs and APIs, a lot of the functionality *should work*. At the time of writing I've tested the following:

* Opening channels ✅
* Adding peers ✅
* Closing channels ✅
* Receiving mainnet coins - this probably will need tweaking as RTL has bech32 option and you can't disable it.
* Sending mainnet coins ✅
*  Sending LN payments
*  Creating LN invoice
 

### Installation

First lets take of the prerequisites, starting by [node.js](https://nodejs.org/en/download/). The instance I'm using is based on ubuntu, in this case the command is:

	curl -sL https://deb.nodesource.com/setup_15.x | sudo 	-E bash -

and then:

	sudo apt-get install -y nodejs

We also need to ensure we have g++:

	sudo apt-get install -y build-essential

Once completed, go back to your home folder and pull from the RTL repository:

	cd ~
	git clone https://github.com/Ride-The-Lightning/RTL.git

Then go into the RTL folder and install:
	
	cd RTL
	npm install --only=prod

This part takes a while... Once it's complete we're ready to modify the configuration file before starting it up.

### Configuration

RTL includes a sample configuration, I've modified it to work with the setup we've below - **read a bit further down instead of just copying and pasting**:

    {
      "multiPass": "password",
      "port": "3000",
      "defaultNodeIndex": 1,
      "SSO": {
        "rtlSSO": 0,
        "rtlCookiePath": "",
        "logoutRedirectLink": ""
      },
      "nodes": [
        {
          "index": 1,
          "lnNode": "My Node",
          "lnImplementation": "LND",
          "Authentication": {
            "macaroonPath": "/home/user/.dcrlnd/data/chain/decred/mainnet",
            "configPath": "/home/user/.dcrlnd/dcrlnd.conf"
          },
          "Settings": {
            "userPersona": "OPERATOR",
            "themeMode": "DAY",
            "themeColor": "PURPLE",
            "channelBackupPath": "~/.dcrlnd/data/chain/decred/mainnet",
            "enableLogging": false,
            "lnServerUrl": "https://localhost:8080",
            "swapServerUrl": "http://localhost:8081",
            "fiatConversion": false
          }
        }
      ]
    }

Key parts that have changed from the sample configuration:

The password can stay unchanged initially, you will get prompted to change it and will be encrypted as soon as you login the first time.

The port is 3000 by default, if your node is public you may want to consider changing this as its the port used to access the web interface:

	"port": "3000",

The macaroon and config paths are standard given the dcrlnd configuration that we just deployed with this installation method:

	"macaroonPath": "/home/user/.dcrlnd/data/chain/decred/mainnet"
	"configPath": "/home/user/.dcrlnd/dcrlnd.conf"

User mode changes some of the interface, I'm assuming the majority of people using this at this stage prefer the node operator interface than the merchant one:

	"userPersona": "OPERATOR",

The channel backup path is also standard with the setup that we've used for this tutorial:
	           
	"channelBackupPath": "/home/user/.dcrlnd/data/chain/decred/mainnet",

You can create the new config file by doing

	nano ~/RTL/RTL-Config.json
		
and pasting the modified config in, then save by pressing **CTRL+X**, then **Y**, then **ENTER**.

At this stage, open a new terminal or create a new tmux session:

	tmux new -s rtl

and run RTL:

	node rtl

You should get the following message:

	Please note that, RTL has encrypted the plaintext password into its corresponding hash.Server is up and running, please open the UI at http://localhost:3000

If you open a browser window and go to the ip address of the node with the specified port you'll be greeted with the RTL password prompt window, and asked to change it.
