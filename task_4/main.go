package main

import (
	"log"
)

func main() {
	// Configure logging to include timestamps
	log.SetFlags(log.LstdFlags)

	// Load configuration from environment variables
	config := loadConfigFromEnv()

	service, err := NewEthereumService(config)
	if err != nil {
		log.Fatalf("Failed to initialize Ethereum service: %v", err)
	}

	service.Start()
}
