// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Vehicle {
    string public vehicleType;
    string public vehicleName;
    constructor(string memory t, string memory n) { vehicleType = t; vehicleName = n; }
    function disp() public view returns (string memory, string memory) {
        return (vehicleType, vehicleName);
    }
}
contract Bike is Vehicle {
    string public brand;
    string public color;
    constructor(string memory t, string memory n, string memory b, string memory c)
        Vehicle(t, n) { brand = b; color = c; }
    function dispB() public view returns (string memory, string memory) {
        return (brand, color);
    }
}
