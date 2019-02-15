pragma solidity ^0.4.25;

/* This contract should manage a CO2-token and have four functions:

1. It should award Tokens to a user if an expert tells it to do so;

2. It should make it possible to send and

3. Also receive Tokens

4. It would be nice if it was possible to buy tokens with ether

*/

contract sustainergy {



  event Transfer(address sender, address receiver, uint amount);

  //Associate addresses with balances

  mapping(address => uint) public balance;





  function createTokens(address _receiver, uint _amount, uint _credential) {

    //Does the function caller have the necessary credentials to create tokens (unfinished)

    //bytes32 hasch = 6e91ec6b618bb462a4a6ee5aa2cb0e9cf30f7a052bb467b0ba58b8748c00d2e5;

    //require(keccak256(abi.encodePacked(_credential)) == hasch);

    //Checks for an overflow

    require(balance[_receiver] + _amount > balance[_receiver]);

    //Adds the created tokens to the sender's account

    balance[_receiver] = balance[_receiver] + _amount;

  }

  

  //Function to transfer tokens

  function transferTokens(address _receiver, uint _amount) public returns (bool success){

    //Checks whether sender has more tokens than he wants to send

    require(balance[msg.sender] >= _amount);

    //Checks for overflow

    require(balance[_receiver] + _amount > balance[_receiver]);

    //Subtracts sent tokens from sender's balance

    balance[msg.sender] = balance[msg.sender] - _amount;

    //Adds sent tokens to receiver's balance

    balance[_receiver] = balance[_receiver] + _amount;



    emit Transfer(msg.sender, _receiver, _amount);



    return true;

  }



  //Checks the user's account balance

  function checkBalance() public view returns (uint) {

    return balance[msg.sender];

  }



}


