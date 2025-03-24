# Task 6: Consensum algorithm PoC

This the PoC based on simplified implementation of Cosmos's novel consensus protocol CometBFT based on [spec](https://github.com/cometbft/cometbft/blob/main/spec/consensus/consensus.md) and more detailed [doc](https://docs.cometbft.com/v1.0/explanation/introduction/). Implemented right from zero without original dependencies or CometBFT libs in demo purposes.
This PoC doesn't involve actual nodes or network and just simulate validators by mocking them.

## CometBFT Features
* CometBFT consists of two chief technical components: a blockchain consensus engine ([by state machine replication model](https://en.wikipedia.org/wiki/State_machine_replication)) and a generic application interface [ABCI](https://docs.cometbft.com/v1.0/spec/abci/)
* Is a PoS consensus protocol with BFT tolerancy up to 1/3 unresponsive nodes (validators) 
* It made native to usage in application and exposes connection to node network via own P2P [CometBFT Socket Protocol](https://github.com/cometbft/knowledge-base/tree/main/p2p) (not covered by the scope of this demo)  
* Used SHA-256 for block hashes and Ed25519 for [vote signatures](https://github.com/cometbft/cometbft/blob/main/p2p/internal/nodekey/nodekey.go)
* CometBFT nodes emit events through [websocket](https://docs.cometbft.com/v1.0/explanation/core/subscription) in ABCI format, making it's easy to subscribe for a particular event
* It's possible to enable [gRPC support](https://docs.cometbft.com/v1.0/explanation/core/subscription) for ABCI
* Introduces and operates on top of own [data structures](https://docs.cometbft.com/v1.0/spec/core/data_structures)
* Consensus module write messages as a [WAL logs](https://docs.cometbft.com/v1.0/spec/consensus/wal.md)

The original paper seem to be unavailable on the time of [this demo](https://docs.cometbft.com/v1.0/spec/consensus/consensus-paper): `Error 404`. Docs and source code was used as a ref.
The repo's [doc page](https://github.com/cometbft/cometbft/blob/main/docs/explanation/introduction/README.md) was used as much as possible.

## Brief CometBFT design overview
The original consensus's core loop can be summed up to a cycle which rotates across following pahses:
1. Propose phase. A proposer (rotated based on voting power) suggests a block with transactions. 
2. Prevote phase. Validators vote on the block. If >2/3 prevote, the block advances. 
3. Precommit phase. Validators lock their votes. If >2/3 precommit, the block is finalized and added. 
4. Retry. If consensus fails (due to faults or timeouts), the round increments, and a new proposer is selected.
5. Validators propose and vote on blocks in rounds, requiring >2/3 agreement for finality. Finality is immediate, preventing forks under normal conditions.

The protocols UML timeline diagram
[![Diag](https://mermaid.ink/img/pako:eNqdlVFv0zAQx7-K5adUS0vsNFmJxKQNxHiAUm2oD1AejHM0Zq0dHKfbmPbdcepkSdeipfQpyf3-d-d_bd8D5ioFnOACfpcgObwTbKnZeiGR_eVMG8FFzqRBU8QKNAVzq_TNfnRWRWda5aoAjbw5W4mUGaUH--icVOwTgcgBhO4i9AAS7iLhQjpoOjw7myboPE2_aCYLxo1Q0jN3xEfmjtb9TJUBpDa2VYt-ALHMDHqDAuRdgoRCFIMm20qpHL23-YHxDP1YKX6DPBgtR34jI3XKpvYsQZdgGiu8TnQ2dOFrA7mttsA1tMBdZtt9Hbmo6nk7BVyKKzCllujC9dPpZDfTnFSpYGNX-wT5TjV4RtLeZNiHnJNhXb-z2q1ogf1GX3wj323I6BI6Sjqs-zlaGQ7r_voqD7rF1XotTD-_-rFhP_awZ05Wr8C9HOFbb_VB715S7-1be-rcnn2-tu3GtcBbJQuQRVl4A3RGX4WIZ8BvWo6tTMugc54J2EDaxjun7DzPQab1GTDKPfCMCbmPV6YexdMj-fAY3lnhNsLJid9aPoVb97V7JezdV59Lk5cmsbyrxQzK6k2FWJpauzpqWBVg5a2ph5u5UqVMq17szaLv_7O4hl_AzbP6sv73tg_tFT2rzoSwF3lrE_oIcmmylnEH8iWI9oHCf0LYx2vQayZSOwUfKskCmwzW9tKoVpkyO-7seh4tx0qjru8lx0m1_X2sVbnMcPKTWY99XOZ2EjXzs0HsrPqqVPcVJw_4DieERqM4nFBKTsfBKaVx7ON7nAzJJBwF0XgcTWIyIfE4iB99_Gebgoxi-joKg0kQjGkcRePIx5AKO_0-uRm-HeWPfwHQwE--?type=png)](https://mermaid.live/edit#pako:eNqdlVFv0zAQx7-K5adUS0vsNFmJxKQNxHiAUm2oD1AejHM0Zq0dHKfbmPbdcepkSdeipfQpyf3-d-d_bd8D5ioFnOACfpcgObwTbKnZeiGR_eVMG8FFzqRBU8QKNAVzq_TNfnRWRWda5aoAjbw5W4mUGaUH--icVOwTgcgBhO4i9AAS7iLhQjpoOjw7myboPE2_aCYLxo1Q0jN3xEfmjtb9TJUBpDa2VYt-ALHMDHqDAuRdgoRCFIMm20qpHL23-YHxDP1YKX6DPBgtR34jI3XKpvYsQZdgGiu8TnQ2dOFrA7mttsA1tMBdZtt9Hbmo6nk7BVyKKzCllujC9dPpZDfTnFSpYGNX-wT5TjV4RtLeZNiHnJNhXb-z2q1ogf1GX3wj323I6BI6Sjqs-zlaGQ7r_voqD7rF1XotTD-_-rFhP_awZ05Wr8C9HOFbb_VB715S7-1be-rcnn2-tu3GtcBbJQuQRVl4A3RGX4WIZ8BvWo6tTMugc54J2EDaxjun7DzPQab1GTDKPfCMCbmPV6YexdMj-fAY3lnhNsLJid9aPoVb97V7JezdV59Lk5cmsbyrxQzK6k2FWJpauzpqWBVg5a2ph5u5UqVMq17szaLv_7O4hl_AzbP6sv73tg_tFT2rzoSwF3lrE_oIcmmylnEH8iWI9oHCf0LYx2vQayZSOwUfKskCmwzW9tKoVpkyO-7seh4tx0qjru8lx0m1_X2sVbnMcPKTWY99XOZ2EjXzs0HsrPqqVPcVJw_4DieERqM4nFBKTsfBKaVx7ON7nAzJJBwF0XgcTWIyIfE4iB99_Gebgoxi-joKg0kQjGkcRePIx5AKO_0-uRm-HeWPfwHQwE--)

## Build & run PoC
There is two modes of execution (containerized & native):
* `native`. Execute the following sequence of commands in terminal (Linux or Mac):
    1. Build dependencies in the root of the project: `go build && go run`
    2. Service will run scripted scenario of block production and validation by 3 validators  
* `containerized`. Executes the same sequence as above but within the short-living container to left your PC clean and avoid potential mismatch in dependency versions:
```bash
chmod +x run run_one_time_cntnr.sh
./run_one_time_cntnr.sh # run demo script and exit
```

Example output:
```bash
./run_one_time_cntnr.sh 
Block at height 1 added to blockchain
Validator 0 blockchain length: 2
Validator 1 blockchain length: 2
Validator 2 blockchain length: 2
Validator 3 blockchain length: 2
```
