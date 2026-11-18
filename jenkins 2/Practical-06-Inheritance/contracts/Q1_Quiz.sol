// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;
contract Quiz {
    struct Question { string text; string correctAnswer; }
    Question[] public questions;
    uint public correctCount;
    uint public wrongCount;
    event Answered(string question, string answer, bool correct);
    function add(string memory question, string memory correctAnswer) public {
        questions.push(Question(question, correctAnswer));
    }
    function ansQ(uint i, string memory answer) public {
        require(i < questions.length, "Invalid index");
        bool ok = keccak256(bytes(answer)) == keccak256(bytes(questions[i].correctAnswer));
        if (ok) correctCount++; else wrongCount++;
        emit Answered(questions[i].text, answer, ok);
    }
}
