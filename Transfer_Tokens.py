from tkinter import *
import web3
from web3 import Web3
import numpy as np

#Init web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

#Contract's Properties
contractAdress = "0xd5e49e2141b60681057432aa64851d7bd1b054a5"
contractAbi = '''[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_receiver",
				"type": "address"
			},
			{
				"name": "_amount",
				"type": "uint256"
			},
			{
				"name": "_credential",
				"type": "uint256"
			}
		],
		"name": "createTokens",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_receiver",
				"type": "address"
			},
			{
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "transferTokens",
		"outputs": [
			{
				"name": "success",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "checkBalance",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "balance",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"name": "sender",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "receiver",
				"type": "address"
			},
			{
				"indexed": false,
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	}
]'''
#Init Contract
sustainergy_contract = w3.eth.contract(address=Web3.toChecksumAddress(contractAdress),abi=contractAbi)

class Window(Frame):
    #Defines global variables
    global sender_Entry
    global receiver_Entry
    global amount_Entry

    #Init Window
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()


    def init_window(self):

        # changing the title of our master widget
        self.master.title("Sustainergy")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a button instance
        send_button = Button(self, text="Send", command = self.send)
        # placing the button on my window
        send_button.place(x=0, y=150)

        #Init Widgets
        global sender_Entry
        global receiver_Entry
        global amount_Entry

        sender_Entry = Entry(self)
        receiver_Entry = Entry(self)
        amount_Entry = Entry(self)

        sender_Entry.place(x=0, y=0)
        receiver_Entry.place(x=0, y=30)
        amount_Entry.place(x=0, y=60)

        sender_Entry.insert(0,"Sender")
        receiver_Entry.insert(0,"Receiver")
        amount_Entry.insert(0,"Amount")

    def send(self):
        #Send Tokens
        w3.eth.defaultAccount = sender_Entry.get()
        sustainergy_contract.functions.transferTokens(receiver_Entry.get(), int(amount_Entry.get())).transact()

#Opens Window
root = Tk()

#Windowsize
root.geometry("150x200")

app = Window(root)
root.mainloop()
