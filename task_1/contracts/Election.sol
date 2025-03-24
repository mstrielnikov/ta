// SPDX-License-Identifier: MIT
pragma solidity >=0.8.2 <0.9.0;

contract Voting {
    // Struct to store voter information
    struct Voter {
        bool isRegistered; // Added to track voter registration
        bool voted;
        uint256 candidateId; // Index of the candidate voted for
    }

    // Struct to store candidate information
    struct Candidate {
        address addr;
        bool registered;
        uint256 voteCount;
    }

    enum ElectionPhase {
        Ballot,
        Ongoing,
        Submit
    }

    // Address of the contract owner (election administrator)
    address public owner;

    // Mapping to store voter information
    mapping(address => Voter) public voters;

    // Array to store candidate information
    Candidate[] public candidates;

    // Total number of votes cast
    uint256 public totalVotes;

    // Election status
    ElectionPhase public phase;

    // Events for frontend integration
    event VoterRegistered(address voter);
    event VoteCast(address voter, address candidateAddr);
    event CandidateRegistered(uint256 indexed candidateIndex, address candidateAddr, uint256 voteCount);
    event BallotPhaseEvent();
    event OngoingPhaseEvent();
    event SubmitPhaseEvent();
    event WinnerDeclared(address winnerAddr, uint256 voteCount);

    // Modifier to restrict functions to owner only
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    // Modifier to check whether election phase is Ballot
    modifier ballotPhase() {
        require(phase == ElectionPhase.Ballot, "Must be in Ballot phase");
        _;
    }

    // Modifier to check whether election is ongoing
    modifier ongoingPhase() {
        require(phase == ElectionPhase.Ongoing, "Must be in Ongoing phase");
        _;
    }

    // Modifier to check whether election is submitted
    modifier submitPhase() {
        require(phase == ElectionPhase.Submit, "Must be in Submit phase");
        _;
    }

    // Constructor
    constructor() {
        owner = msg.sender;
        phase = ElectionPhase.Ballot;
    }

    // Function to register a voter (only owner)
    function registerVoter(address _voter) public onlyOwner ballotPhase {
        require(!voters[_voter].isRegistered, "Voter already registered");
        voters[_voter] = Voter({
            isRegistered: true,
            voted: false,
            candidateId: 0
        });
        emit VoterRegistered(_voter);
    }

    // Function to register a candidate (only owner)
    function registerCandidate(address _candidateAddr) public onlyOwner ballotPhase {
        require(_candidateAddr != address(0), "Invalid candidate address");
        
        // Check if candidate is already registered
        for (uint256 i = 0; i < candidates.length; i++) {
            require(candidates[i].addr != _candidateAddr, "Candidate already registered");
        }
        
        candidates.push(
            Candidate({
                addr: _candidateAddr,
                registered: true,
                voteCount: 0
            })
        );

        emit CandidateRegistered(candidates.length - 1, _candidateAddr, 0);
    }

    // Function to start the election (only owner)
    function startElection() public onlyOwner ballotPhase {
        require(candidates.length > 0, "No candidates added");

        phase = ElectionPhase.Ongoing;
        emit OngoingPhaseEvent();
    }

    // Function to cast a vote
    function vote(uint256 _candidateId) public ongoingPhase {
        // Check if voter is registered
        require(voters[msg.sender].isRegistered, "Voter not registered");

        // Check if voter hasn't voted yet
        require(!voters[msg.sender].voted, "Voter has already voted");
        
        // Check if requested candidate exists
        require(_candidateId < candidates.length, "Invalid candidate ID");
        
        // Check if requested candidate is registered
        require(candidates[_candidateId].registered, "Candidate not registered");
            
        // Record the vote
        voters[msg.sender].voted = true;
        voters[msg.sender].candidateId = _candidateId;
        
        // Increment candidate votes
        candidates[_candidateId].voteCount++;

        totalVotes++;
        emit VoteCast(msg.sender, candidates[_candidateId].addr);
    }

    // Function to end the election and declare winner (only owner)
    function submitVotes() public onlyOwner ongoingPhase returns (address winnerAddr, uint256 winnerVotes) {
        require(totalVotes > 0, "No votes submitted");
        
        phase = ElectionPhase.Submit;
        emit SubmitPhaseEvent();

        require(candidates.length > 0, "No candidates in election");

        uint256 maxVotes = 0;
        uint256 winnerId = 0;

        // Find the winning candidate
        for (uint256 i = 0; i < candidates.length; i++) {
            if (candidates[i].voteCount > maxVotes) {
                maxVotes = candidates[i].voteCount;
                winnerId = i;
            }
        }

        winnerAddr = candidates[winnerId].addr;
        winnerVotes = candidates[winnerId].voteCount;
        emit WinnerDeclared(winnerAddr, winnerVotes);

        return (winnerAddr, winnerVotes);
    }

    // Function to list all candidates
    function listCandidates() public view 
        returns (uint256[] memory ids, address[] memory addrs, uint256[] memory voteCounts) {
        uint256[] memory candidateIds = new uint256[](candidates.length);
        address[] memory candidateAddrs = new address[](candidates.length);
        uint256[] memory candidateVoteCounts = new uint256[](candidates.length);

        for (uint256 i = 0; i < candidates.length; i++) {
            candidateIds[i] = i;
            candidateAddrs[i] = candidates[i].addr;
            candidateVoteCounts[i] = candidates[i].voteCount;
        }
        
        return (candidateIds, candidateAddrs, candidateVoteCounts);
    }

    // Fallback function to reject calls to non-existent functions
    fallback() external {
        revert("Function does not exist");
    }

    // Receive function to reject plain Ether transfers
    receive() external payable {
        revert("This contract does not accept Ether");
    }
}