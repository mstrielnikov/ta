package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math/big"
	"net/http"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/ethclient"
	"github.com/julienschmidt/httprouter"
)

// EthereumService holds the Ethereum client and configuration
type EthereumService struct {
	client *ethclient.Client
	config Config
}

// BlockResponse represents the response for block data
type BlockResponse struct {
	Number       string `json:"number"`
	Hash         string `json:"hash"`
	Transactions int    `json:"transactions"`
}

// BalanceResponse represents the response for balance data
type BalanceResponse struct {
	Address string `json:"address"`
	Balance string `json:"balance"` // Balance in Ether
}

// NewEthereumService creates a new Ethereum service
func NewEthereumService(config Config) (*EthereumService, error) {
	log.Printf("Connecting to Ethereum node at %s", config.EthNodeURL)

	client, err := ethclient.Dial(config.EthNodeURL)
	if err != nil {
		log.Printf("Failed to connect to Ethereum node: %v", err)
		return nil, fmt.Errorf("failed to connect to Ethereum node: %v", err)
	}

	// Verify the network ID to confirm the correct network
	ctx := context.Background()
	networkID, err := client.NetworkID(ctx)
	if err != nil {
		log.Printf("Failed to fetch network ID: %v", err)
		return nil, fmt.Errorf("failed to fetch network ID: %v", err)
	}

	log.Printf("Successfully connected to Ethereum node, network ID: %v", networkID)

	return &EthereumService{
		client: client,
		config: config,
	}, nil
}

// GetLatestBlock fetches the latest block from the Ethereum blockchain
func (s *EthereumService) GetLatestBlock(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	log.Println("Received request to fetch latest block")

	ctx := context.Background()
	block, err := s.client.BlockByNumber(ctx, nil) // nil fetches the latest block
	if err != nil {
		log.Printf("Failed to fetch latest block: %v", err)
		http.Error(w, fmt.Sprintf("failed to fetch latest block: %v", err), http.StatusInternalServerError)
		return
	}

	response := BlockResponse{
		Number:       block.Number().String(),
		Hash:         block.Hash().Hex(),
		Transactions: len(block.Transactions()),
	}

	log.Printf("Successfully fetched latest block - number: %s, hash: %s, transactions: %d", response.Number, response.Hash, response.Transactions)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// GetBalance fetches the balance of a given Ethereum address
func (s *EthereumService) GetBalance(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
	address := ps.ByName("address")

	log.Printf("Received request to fetch balance for address: %s", address)

	if !common.IsHexAddress(address) {
		log.Printf("Invalid Ethereum address provided: %s", address)
		http.Error(w, "invalid Ethereum address", http.StatusBadRequest)
		return
	}

	ctx := context.Background()
	account := common.HexToAddress(address)
	balance, err := s.client.BalanceAt(ctx, account, nil) // nil uses the latest block
	if err != nil {
		log.Printf("Failed to fetch balance for address %s: %v", address, err)
		http.Error(w, fmt.Sprintf("failed to fetch balance: %v", err), http.StatusInternalServerError)
		return
	}

	// Convert balance from Wei to Ether
	balanceInEther := new(big.Float).Quo(new(big.Float).SetInt(balance), big.NewFloat(1e18))

	response := BalanceResponse{
		Address: address,
		Balance: fmt.Sprintf("%.18f", balanceInEther),
	}

	log.Printf("Successfully fetched balance for address %s: %s", response.Address, response.Balance)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// Start starts the HTTP server
func (s *EthereumService) Start() {
	router := httprouter.New()
	router.GET("/block/latest", s.GetLatestBlock)
	router.GET("/balance/:address", s.GetBalance)

	log.Printf("Starting server on port %s", s.config.Port)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", s.config.Port), router))
}
