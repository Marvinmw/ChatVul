// https://etherscan.io/address/0xf91546835f756da0c10cfa0cda95b15577b84aa7#code

pragma solidity ^0.4.23;
// produced by the Solididy File Flattener (c) David Appleton 2018
// contact : dave@akomba.com
// released under Apache 2.0 licence
contract Token {
    /* This is a slight change to the ERC20 base standard.
    function totalSupply() constant returns (uint256 supply);
    is replaced with:
    uint256 public totalSupply;
    This automatically creates a getter function for the totalSupply.
    This is moved to the base contract since public getter functions are not
    currently recognised as an implementation of the matching abstract
    function by the compiler.
    */
    /// total amount of tokens
    
    // virtual-channel state
    
    function createChannel(
        bytes32 _lcID,
        address _partyI,
        uint256 _confirmTime,
        address _token,
        uint256[2] _balances // [eth, token]
    ) 
        public
        payable 
    {
        require(Channels[_lcID].partyAddresses[0] == address(0), "Channel has already been created.");
        require(_partyI != 0x0, "No partyI address provided to LC creation");
        require(_balances[0] >= 0 && _balances[1] >= 0, "Balances cannot be negative");
        // Set initial ledger channel state
        // Alice must execute this and we assume the initial state 
        // to be signed from this requirement
        // Alternative is to check a sig as in joinChannel
        Channels[_lcID].partyAddresses[0] = msg.sender;
        Channels[_lcID].partyAddresses[1] = _partyI;

        if(_balances[0] != 0) {
            require(msg.value == _balances[0], "Eth balance does not match sent value");
            Channels[_lcID].ethBalances[0] = msg.value;
        } 
        if(_balances[1] != 0) {
            Channels[_lcID].token = HumanStandardToken(_token);
            require(Channels[_lcID].token.transferFrom(msg.sender, this, _balances[1]),"CreateChannel: token transfer failure");
            Channels[_lcID].erc20Balances[0] = _balances[1];
        }

        Channels[_lcID].sequence = 0;
        Channels[_lcID].confirmTime = _confirmTime;
        // is close flag, lc state sequence, number open vc, vc root hash, partyA... 
        //Channels[_lcID].stateHash = keccak256(uint256(0), uint256(0), uint256(0), bytes32(0x0), bytes32(msg.sender), bytes32(_partyI), balanceA, balanceI);
        Channels[_lcID].LCopenTimeout = now + _confirmTime;
        Channels[_lcID].initialDeposit = _balances;

        emit DidLCOpen(_lcID, msg.sender, _partyI, _balances[0], _token, _balances[1], Channels[_lcID].LCopenTimeout);
    }

    function LCOpenTimeout(bytes32 _lcID) public {
        require(msg.sender == Channels[_lcID].partyAddresses[0] && Channels[_lcID].isOpen == false);
        require(now > Channels[_lcID].LCopenTimeout);

        if(Channels[_lcID].initialDeposit[0] != 0) {
            Channels[_lcID].partyAddresses[0].transfer(Channels[_lcID].ethBalances[0]);
        } 
        if(Channels[_lcID].initialDeposit[1] != 0) {
            require(Channels[_lcID].token.transfer(Channels[_lcID].partyAddresses[0], Channels[_lcID].erc20Balances[0]),"CreateChannel: token transfer failure");
        }

        emit DidLCClose(_lcID, 0, Channels[_lcID].ethBalances[0], Channels[_lcID].erc20Balances[0], 0, 0);

        // only safe to delete since no action was taken on this channel
        delete Channels[_lcID];
    }

 }