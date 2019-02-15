from tkinter import *
import web3
from web3 import Web3
import numpy as np

#Init Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
#Names of Companies or Households
names = ['name1','name2','name3','name4','name5','name6','name7','name8','name9','name10']
#Contract Properties
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

	# Window Creation
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Sustainergy")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a button instance
        refresh = Button(self, text="Refresh", command = self.showText)
        # placing the button on my window
        refresh.place(x=0, y=350)

        self.showText()

	#Show leaderboard
    def showText(self):
        balances = np.empty(10)
        for i in range(10):
            balances[i] =sustainergy_contract.functions.balance(w3.eth.accounts[i]).call()
        indecies = np.argsort(balances)
        for i in range(10):
            text = Label(self, text=w3.eth.accounts[indecies[9-i]])
            text.place(x=0, y = i*20+20)
            text = Label(self, text=names[indecies[9-i]])
            text.place(x=400, y= i*20+20)
            text = Label(self, text=balances[indecies[9-i]])
            text.place(x=500, y= i*20+20)

root = Tk()

#Windowsize
root.geometry("600x350")

app = Window(root)
root.mainloop()
