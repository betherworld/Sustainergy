#Import the necessary libraries
import serial
import web3
from web3 import Web3

#Defines Constants
temp_threshold = 25 #Temperature at which you don't get any token
counter_threshold = 600 #Number of measurements, that are send to the Blockchain at one time

#Init Web3 Server
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

#Participants of the Transactions
owner = w3.eth.accounts[0]
receiver = w3.eth.accounts[1]

#Properties of the Contract
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

#Init Account
w3.eth.defaultAccount = owner

sustainergy_contract = w3.eth.contract(address=Web3.toChecksumAddress(contractAdress),abi=contractAbi)


#Defines function that calculates number of tokens earned
def compute_token(average):
	#Calculates the difference between the average room temperature and a set threshold
    diff = temp_threshold - average
	#If the room temperature is higher than the set maximum no tokens will be generated
    if diff < 0:
        return 0
	#The number of tokens received is half of the temperature difference squared
    anz_token = 0.5 * diff ** 2
	#The function returns the number of tokens earned
    return anz_token

#Defines function that accesses the smart contract
def create_token(n):
	sustainergy_contract.functions.createTokens(receiver,n,120).transact()

#Init connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600)

#Defines variables
average = 0.0
counter = 0
tokenrest = 0

#Initiates infinite loop
while 1:
    try:
		#Saves data from the Arduino (which is sent every second) in the variable x
        x = float(ser.readline())
		#Filters obviously wrong measurements
        if x > 0:
			#Calculates the weighted average of the last average and the current measurement
            average = (average*counter + x)/(counter+1)
			#Increases the counter by 1
            counter += 1
			#Prints the counter and the average
            if counter%15==0:
                print("Temperature:  "+x)
		#If the counter exceeds a set threshold it is reset and the number of earned tokens is calculated
        if counter >= counter_threshold:
			#Compute amount of token
            tokenfloat = compute_token(average) + tokenrest
			#average and counter is reset to 0
            average = 0
            counter = 0
			#The tokens are converted to an integer
            tokenint = int(tokenfloat)
			#The tokens earned are printed
            print("Create " + tokenint + " tokens")
			#The leftover tokens are saved
            tokenrest = tokenfloat - tokenint
			#Writes the created tokens to the blockchain
            create_token(tokenint)
            print("Tokens successfully created")
	#If no data is received the try path is skipped
    except:
        pass
