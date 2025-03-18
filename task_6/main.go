package main

import (
	"fmt"
	"sync"
	"time"
)

// Transaction represents a simple transaction
type Transaction struct {
	ID   string
	Data string
}

// Block represents a block in the blockchain
type Block struct {
	Height    int
	Timestamp time.Time
	Txs       []Transaction
	PrevHash  string
	Hash      string
}

// Validator represents a CometBFT validator
type Validator struct {
	ID          int
	VotingPower int
	Prevotes    map[int]bool
	Precommits  map[int]bool
	LockedBlock *Block // Locked block (if any)
	Blockchain  []Block
	Step        string // NewHeight, Propose, Prevote, Precommit, Commit
}

// Network simulates the CometBFT network
type Network struct {
	Validators  []*Validator
	PendingTxs  []Transaction
	Height      int
	Round       int
	ProposerIdx int
	Mutex       sync.Mutex
}

// NewNetwork initializes a network with validators
func NewNetwork(numValidators int) *Network {
	n := &Network{
		Validators:  make([]*Validator, 0),
		PendingTxs:  make([]Transaction, 0),
		Height:      0, // Start at 0 (genesis)
		Round:       0,
		ProposerIdx: 0,
	}
	for i := 0; i < numValidators; i++ {
		n.Validators = append(n.Validators, &Validator{
			ID:          i,
			VotingPower: 1,
			Prevotes:    make(map[int]bool),
			Precommits:  make(map[int]bool),
			LockedBlock: nil,
			Blockchain:  []Block{{Height: 0, Timestamp: time.Now(), PrevHash: "0", Hash: "genesis"}},
			Step:        "NewHeight",
		})
	}
	return n
}

// AddTransaction adds a transaction
func (n *Network) AddTransaction(tx Transaction) {
	n.Mutex.Lock()
	defer n.Mutex.Unlock()
	n.PendingTxs = append(n.PendingTxs, tx)
}

// GetProposer selects the proposer
func (n *Network) GetProposer() *Validator {
	return n.Validators[n.ProposerIdx]
}

// ProposeBlock proposes a block
func (n *Network) ProposeBlock(proposer *Validator) (Block, bool) {
	n.Mutex.Lock()
	defer n.Mutex.Unlock()

	if len(n.PendingTxs) == 0 {
		return Block{}, false // No block to propose
	}

	prevBlock := proposer.Blockchain[len(proposer.Blockchain)-1]
	block := Block{
		Height:    n.Height + 1,
		Timestamp: time.Now(),
		Txs:       n.PendingTxs,
		PrevHash:  prevBlock.Hash,
		Hash:      fmt.Sprintf("block%d", n.Height+1),
	}
	n.PendingTxs = []Transaction{}
	return block, true
}

// Prevote simulates the Prevote phase
func (n *Network) Prevote(validator *Validator, height int, block Block) bool {
	if block.Height == height && (validator.LockedBlock == nil || validator.LockedBlock.Hash == block.Hash) {
		validator.Prevotes[height] = true
		return true
	}
	return false
}

// Precommit simulates the Precommit phase
func (n *Network) Precommit(validator *Validator, height int, block Block) bool {
	if validator.Prevotes[height] && (validator.LockedBlock == nil || validator.LockedBlock.Hash == block.Hash) {
		validator.Precommits[height] = true
		return true
	}
	return false
}

// Consensus checks for >2/3 agreement
func (n *Network) Consensus(block Block) bool {
	n.Mutex.Lock()
	defer n.Mutex.Unlock()

	totalVotingPower := 0
	prevoteCount := 0
	precommitCount := 0

	for _, v := range n.Validators {
		totalVotingPower += v.VotingPower
		if v.Prevotes[block.Height] {
			prevoteCount += v.VotingPower
			if prevoteCount > (2*totalVotingPower)/3 && v.LockedBlock == nil {
				v.LockedBlock = &block // Lock on block
			}
		}
		if v.Precommits[block.Height] {
			precommitCount += v.VotingPower
		}
	}

	threshold := (2 * totalVotingPower) / 3
	return prevoteCount > threshold && precommitCount > threshold
}

// AddBlock adds a block if consensus is reached
func (n *Network) AddBlock(block Block) bool {
	if n.Consensus(block) {
		n.Mutex.Lock()
		defer n.Mutex.Unlock()
		for _, v := range n.Validators {
			v.Blockchain = append(v.Blockchain, block)
			v.Step = "Commit"
		}
		n.Height++
		n.ProposerIdx = (n.ProposerIdx + 1) % len(n.Validators)
		fmt.Printf("Block at height %d added to blockchain\n", block.Height)
		for _, v := range n.Validators {
			v.Step = "NewHeight" // Transition to next height
		}
		return true
	}
	fmt.Printf("Block at height %d rejected: no consensus\n", block.Height)
	n.Round++
	return false
}

// SimulateNetwork runs a simulation
func SimulateNetwork(n *Network) {
	n.AddTransaction(Transaction{ID: "tx1", Data: "Send 10 ATOM"})
	n.AddTransaction(Transaction{ID: "tx2", Data: "Send 5 ATOM"})

	for i := 0; i < 2; i++ {
		proposer := n.GetProposer()
		proposer.Step = "Propose"
		block, ok := n.ProposeBlock(proposer)
		if !ok {
			continue // Skip if no transactions
		}

		for _, v := range n.Validators {
			v.Step = "Prevote"
			n.Prevote(v, block.Height, block)
		}

		for _, v := range n.Validators {
			v.Step = "Precommit"
			n.Precommit(v, block.Height, block)
		}

		n.AddBlock(block)
	}

	for _, v := range n.Validators {
		fmt.Printf("Validator %d blockchain length: %d\n", v.ID, len(v.Blockchain))
	}
}

func main() {
	network := NewNetwork(4) // 4 validators
	SimulateNetwork(network)
}
