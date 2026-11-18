// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Student {
    struct StudentData { uint id; string name; string studentAddress; }
    mapping(uint => StudentData) public students;
    function addStud(uint id, string memory name, string memory addr) public {
        students[id] = StudentData(id, name, addr);
    }
    function getS(uint id) public view returns (uint, string memory, string memory) {
        StudentData memory s = students[id];
        return (s.id, s.name, s.studentAddress);
    }
}
