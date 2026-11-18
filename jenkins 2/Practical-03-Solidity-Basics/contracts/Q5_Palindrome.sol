// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Palindrome {
    function check(uint n) public pure returns (string memory) {
        uint original = n;
        uint reversed = 0;
        while (n > 0) {
            reversed = reversed * 10 + n % 10;
            n = n / 10;
        }
        return reversed == original ? "Palindrome" : "Not Palindrome";
    }
}
