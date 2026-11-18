// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Rental {
    string public agencyName;
    event VehicleRented(address renter, string vehicle, uint daysRented, uint totalRent);
    constructor(string memory agency) { agencyName = agency; }
    function calculateRent(uint daysRented) public pure virtual returns (uint) {
        return 0 * daysRented;
    }
}
contract CarRental is Rental {
    constructor(string memory agency) Rental(agency) {}
    function calculateRent(uint daysRented) public pure override returns (uint) {
        return daysRented * 10000;
    }
    function rent(uint daysRented) public {
        require(daysRented > 0, "Enter days");
        emit VehicleRented(msg.sender, "Car", daysRented, calculateRent(daysRented));
    }
}
contract BikeRental is Rental {
    constructor(string memory agency) Rental(agency) {}
    function calculateRent(uint daysRented) public pure override returns (uint) {
        return daysRented * 3000;
    }
    function rent(uint daysRented) public {
        require(daysRented > 0, "Enter days");
        emit VehicleRented(msg.sender, "Bike", daysRented, calculateRent(daysRented));
    }
}
