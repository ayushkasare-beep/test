// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
// Learning example: accounts are controlled by their creators.
contract Bank {
    struct User { uint accountNo; string name; uint balance; address owner; }
    mapping(uint => User) public users;
    function createAccount(uint accno, string memory name) public {
        require(accno != 0 && users[accno].accountNo == 0, "Invalid or existing account");
        users[accno] = User(accno, name, 0, msg.sender);
    }
    function deposit(uint accno) public payable {
        require(users[accno].accountNo != 0, "Account not found");
        require(msg.value > 0, "Send ETH");
        users[accno].balance += msg.value;
    }
    function withdraw(uint accno, uint amount) public {
        User storage u = users[accno];
        require(u.owner == msg.sender, "Only account owner");
        require(amount > 0 && u.balance >= amount, "Insufficient balance");
        u.balance -= amount;
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "Transfer failed");
    }
    function getBalance(uint accno) public view returns (uint) {
        require(users[accno].accountNo != 0, "Account not found");
        return users[accno].balance;
    }
}
