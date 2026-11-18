// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Employee {
    struct EmployeeData { uint id; string name; uint salary; string designation; }
    mapping(uint => EmployeeData) public employees;
    function addempD(uint id, string memory name, uint salary, string memory designation) public {
        employees[id] = EmployeeData(id, name, salary, designation);
    }
    function getE(uint id) public view returns (uint, string memory, uint, string memory) {
        EmployeeData memory e = employees[id];
        return (e.id, e.name, e.salary, e.designation);
    }
    function updatesal(uint id, uint newSalary) public { employees[id].salary = newSalary; }
}
