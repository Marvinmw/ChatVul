

## Vulnerability Type: Signature Replay Attack

The code is missing protection against signature replay attacks. The `send` function in the `ERC777` contract is using `_send` function to transfer tokens. The `_send` function is not checking if the message hash has already been processed by the contract. This can allow an attacker to replay a signed message multiple times, resulting in unauthorized token transfers.

## Recommendation

To protect against signature replay attacks, the contract should only allow new hashes to be processed. This can be achieved by storing every message hash processed by the contract and checking message hashes against the existing ones before executing the function. Additionally, the address of the contract should be included in the hash to ensure that the message is only used in a single contract. It is also recommended to never generate the message hash including the signature to prevent signature malleability.

## Example

A possible implementation of the recommendation is as follows:

```Solidity
pragma solidity ^0.8.0;

contract ERC777Protected is Context, IERC777, IERC20 {
    using Address for address;
    IERC1820Registry internal constant _ERC1820_REGISTRY = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);
    mapping(bytes32 => bool) private _processedHashes;
    mapping(address => uint256) private _balances;
    uint256 private _totalSupply;
    string private _name;
    string private _symbol;
    bytes32 private constant _TOKENS_SENDER_INTERFACE_HASH = keccak256("ERC777TokensSender");
    bytes32 private constant _TOKENS_RECIPIENT_INTERFACE_HASH = keccak256("ERC777TokensRecipient");
    address[] private _defaultOperatorsArray;
    mapping(address => bool) private _defaultOperators;
    mapping(address => mapping(address => bool)) private _operators;
    mapping(address => mapping(address => bool)) private _revokedDefaultOperators;
    mapping(address => mapping(address => uint256)) private _allowances;

    constructor(
        string memory name_,
        string memory symbol_,
        address[] memory defaultOperators_
    ) {
        _name = name_;
        _symbol = symbol_;
        _defaultOperatorsArray = defaultOperators_;
        for (uint256 i = 0; i < defaultOperators_.length; i++) {
            _defaultOperators[defaultOperators_[i]] = true;
        }
        _ERC1820_REGISTRY.setInterfaceImplementer(address(this), keccak256("ERC777Token"), address(this));
        _ERC1820_REGISTRY.setInterfaceImplementer(address(this), keccak256("ERC20Token"), address(this));
    }

    function name() public view virtual override returns (string memory) {
        return _name;
    }

    function symbol() public view virtual override returns (string memory) {
        return _symbol;
    }

    function decimals() public pure virtual returns (uint8) {
        return 18;
    }

    function granularity() public view virtual override returns (uint256) {
        return 1;
    }

    function totalSupply() public view virtual override(IERC20, IERC777) returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address tokenHolder) public view virtual override(IERC20, IERC777) returns (uint256) {
        return _balances[tokenHolder];
    }

    function send(
        address recipient,
        uint256 amount,
        bytes memory data
    ) public virtual override {
        bytes32 messageHash = keccak256(abi.encodePacked(address(this), _msgSender(), recipient, amount, data));
        require(!_processedHashes[messageHash], "ERC777Protected: message hash already processed");
        _processedHashes[messageHash] = true;
        _send(_msgSender(), recipient, amount, data, "", true);
    }

    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
        bytes32 messageHash = keccak256(abi.encodePacked(address(this), _msgSender(), recipient, amount));
        require(!_processedHashes[messageHash], "ERC777Protected: message hash already processed");
        _processedHashes[messageHash] = true;
        _send(_msgSender(), recipient, amount, "", "", false);
        return true;
    }

    function burn(uint256 amount, bytes memory data) public virtual override {
        bytes32 messageHash = keccak256(abi.encodePacked(address(this), _msgSender(), amount, data));
        require(!_processedHashes[messageHash], "ERC777Protected: message hash already processed");
        _processedHashes[messageHash] = true;
        _burn(_msgSender(), amount, data, "");
    }

    function isOperatorFor(address operator, address tokenHolder) public view virtual override