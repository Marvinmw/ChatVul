contract A{
  uint8 public num;
  address public owner;
  uint256 public time;
  string public message;
  bytes public data;


  function callOne() public{
      num = 100;
      owner = msg.sender;
      time = block.timestamp;
      message = "Darah";
      data = abi.encodePacked(num, msg.sender, block.timestamp);

  }


contract B{

  uint8 public num;
  address public owner;
  uint256 public time;
  string public message;
  bytes public data;

  function callTwo(address contractAddress) public returns(bool){

      (bool success,) = contractAddress.delegatecall(
          abi.encodeWithSignature("callOne()")
      );
      }
     
}