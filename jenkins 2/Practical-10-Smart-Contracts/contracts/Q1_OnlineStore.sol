// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Product {
    uint public productId;
    uint public priceWei;
    uint public stock;
    string public productName;
    constructor(uint id, uint price, uint count, string memory name) {
        productId = id; priceWei = price; stock = count; productName = name;
    }
    function disProduct() public view returns(uint, uint, uint, string memory) {
        return (productId, priceWei, stock, productName);
    }
}
contract OnlineStore is Product {
    address payable public owner;
    constructor(uint id, uint price, uint count, string memory name) Product(id, price, count, name) {
        owner = payable(msg.sender);
    }
    function purchase() public payable {
        require(stock > 0, "Out of stock");
        require(msg.value == priceWei, "Wrong ETH amount");
        stock -= 1;
        (bool ok, ) = owner.call{value: msg.value}("");
        require(ok, "Payment failed");
    }
}
