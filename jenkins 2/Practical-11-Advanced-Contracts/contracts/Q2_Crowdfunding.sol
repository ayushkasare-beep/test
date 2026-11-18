// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Campaign {
    address payable public owner;
    uint public goalWei;
    uint public deadline;
    uint public totalFunds;
    constructor(uint goal, uint durationSeconds) {
        require(goal > 0 && durationSeconds > 0, "Invalid campaign");
        owner = payable(msg.sender);
        goalWei = goal;
        deadline = block.timestamp + durationSeconds;
    }
}
contract Contribution is Campaign {
    mapping(address => uint) public contributions;
    bool public withdrawn;
    event ContributionReceived(address indexed contributor, uint amount);
    event GoalReached(uint total);
    event RefundIssued(address indexed contributor, uint amount);
    constructor(uint goal, uint durationSeconds) Campaign(goal, durationSeconds) {}
    function contribute() public payable {
        require(block.timestamp < deadline, "Campaign ended");
        require(!withdrawn, "Already withdrawn");
        require(msg.value > 0, "Send ETH");
        contributions[msg.sender] += msg.value;
        uint previous = totalFunds;
        totalFunds += msg.value;
        emit ContributionReceived(msg.sender, msg.value);
        if (previous < goalWei && totalFunds >= goalWei) emit GoalReached(totalFunds);
    }
    function refund() public {
        require(block.timestamp >= deadline, "Campaign active");
        require(totalFunds < goalWei, "Goal met");
        uint amount = contributions[msg.sender];
        require(amount > 0, "Nothing to refund");
        contributions[msg.sender] = 0;
        totalFunds -= amount;
        (bool ok, ) = payable(msg.sender).call{value: amount}("");
        require(ok, "Refund failed");
        emit RefundIssued(msg.sender, amount);
    }
    function withdraw() public {
        require(msg.sender == owner, "Owner only");
        require(totalFunds >= goalWei, "Goal not met");
        require(!withdrawn, "Already withdrawn");
        withdrawn = true;
        (bool ok, ) = owner.call{value: address(this).balance}("");
        require(ok, "Withdraw failed");
    }
}
