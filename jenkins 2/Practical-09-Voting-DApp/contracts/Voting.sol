// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
// Classroom demo: counts clicks, not a secure one-person-one-vote system.
contract Voting {
    uint public candidate1Votes;
    uint public candidate2Votes;
    function voteCandidate1() public { candidate1Votes++; }
    function voteCandidate2() public { candidate2Votes++; }
}
