// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Parent1 {
    string internal first;
    constructor(string memory n) { first = n; }
}
contract Parent2 {
    string internal second;
    constructor(string memory n) { second = n; }
}
contract Child is Parent1, Parent2 {
    string public childName;
    constructor(string memory a, string memory b, string memory c)
        Parent1(a) Parent2(b) { childName = c; }
    function disp() public view returns (string memory, string memory, string memory) {
        return (first, second, childName);
    }
}
