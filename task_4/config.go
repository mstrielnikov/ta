package main

import (
	"github.com/joho/godotenv"
	"log"
	"os"
)

// Config holds configuration for the service
type Config struct {
	EthNodeURL string
	Port       string
}

// loadConfigFromEnv loads configuration from environment variables
func loadConfigFromEnv() Config {
	// Load .env file if it exists
	if err := godotenv.Load(); err != nil {
		log.Printf("No .env file found. Fallback to check env variables: %v", err)
	}

	config := Config{
		EthNodeURL: os.Getenv("ETH_NODE_URL"),
		Port:       os.Getenv("PORT"),
	}

	// Validate required parameters
	if config.EthNodeURL == "" {
		log.Fatal("ETH_NODE_URL environment variable is required")
	}
	if config.Port == "" {
		config.Port = "8080"
		log.Printf("no PORT env var provided. Set to default web port: %s", config.Port)
	}

	return config
}
