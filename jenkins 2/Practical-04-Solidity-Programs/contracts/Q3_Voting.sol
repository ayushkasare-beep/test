// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Voting {
    string[] public candidates;
    mapping(address => bool) public hasVoted;
    mapping(string => uint) public votes;
    constructor(string[] memory names) {
        require(names.length > 0, "Need candidates");
        candidates = names;
    }
    function vote(string memory name) public {
        require(!hasVoted[msg.sender], "Already voted");
        bool found;
        for (uint i = 0; i < candidates.length; i++) {
            if (keccak256(bytes(candidates[i])) == keccak256(bytes(name))) { found = true; break; }
        }
        require(found, "Unknown candidate");
        votes[name]++;
        hasVoted[msg.sender] = true;
    }
    function winner() public view returns (string memory) {
        string memory top = candidates[0];
        for (uint i = 1; i < candidates.length; i++) {
            if (votes[candidates[i]] > votes[top]) top = candidates[i];
        }
        return top;
    }
}
