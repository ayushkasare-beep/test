// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
// Per source PDF, uses a struct/mapping rather than the stated Person inheritance.
contract CourseRegistration {
    struct Student { string name; uint id; bool registered; }
    address public owner;
    string public courseName;
    uint public courseFeeWei;
    uint public capacity;
    uint public registeredCount;
    mapping(address => Student) public students;
    event Registered(address student, string name, uint id);
    constructor(string memory name, uint fee, uint maxSeats) {
        require(maxSeats > 0, "Capacity required");
        owner = msg.sender; courseName = name; courseFeeWei = fee; capacity = maxSeats;
    }
    function register(string memory name, uint id) public payable {
        require(registeredCount < capacity, "Full");
        require(!students[msg.sender].registered, "Already registered");
        require(msg.value == courseFeeWei, "Wrong fee");
        students[msg.sender] = Student(name, id, true);
        registeredCount++;
        emit Registered(msg.sender, name, id);
    }
    function seatsLeft() public view returns (uint) { return capacity - registeredCount; }
    function withdraw() public {
        require(msg.sender == owner, "Only owner");
        uint amount = address(this).balance;
        (bool ok, ) = payable(owner).call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
