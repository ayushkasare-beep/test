// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract PerfectNumber {
    function check(uint n) public pure returns (string memory) {
        if (n < 2) return "Not Perfect Number";
        uint sum = 0;
        for (uint i = 1; i <= n / 2; i++) if (n % i == 0) sum += i;
        return sum == n ? "Perfect Number" : "Not Perfect Number";
    }
}
