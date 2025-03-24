# Task 3: Layer 2 In-Depth Analysis of Optimism vs StarkNet (aka zk-rollup)

# Optimism overview
Optimism is a L2-network for Ethereum. It utilizes optimistic rollups to enhance scalability while preserving Ethereum’s default security.

Etherum's cryptographic stack involves:
1. Ethereum uses ECDSA with the secp256k1 curve for securing transactions. Inherently, it results in large size of collective signatures, since ECDSA doesn't support signature aggregation unlike Shcnorr-based ones. Or requires implementation membership proofs through of Merkle proofs.  
2. Employs the Keccak-256 hashing algorithm [(a variant of SHA-3)](https://ethereum.stackexchange.com/questions/550/which-cryptographic-hash-function-does-ethereum-use). Keccak-256 belongs to SHA-3 hashing standards. For now, we are not know as much as critical attacks such [Length Extension attack on SHA-256](https://github.com/amlweems/hexpand).
3. Utilizes [Merkle Patricia trees](https://docs.alchemy.com/docs/patricia-merkle-tries) to construct poof memberships to ensure integrity [and existence](https://docs.optimism.io/stack/protocol/rollup/#data-availability) for transactions and accounts.
4. These algorithms are combined all together within consensus protocol to ensure finality and agreement on blocks and [prevent](https://dspstudents.com/ethereum-double-spending-does-each-node-maintain-a-list-of-unspent-transaction-references/) different sort of attacks like double spending.

Optimism’s security derived from Ethereum’s Layer 1, since it relies entirely on Ethereum’s consensus, with its own rollup-specific process. 

## Optimistic  rollups 
Optimism assumes transactions are valid unless challenged during a 7-day window, enforced by a fault proof system transitioning to interactive disputes. Disputes are resolved on Ethereum, leveraging its validator network. [Optimism Docs on Fault Proofs](https://docs.optimism.io/stack/protocol/fault-proofs/).
Transactions are executed off-chain, compressed into batches, and posted to Ethereum as a regular transactions, reducing load on L1. Keep it in mind, that Optimistic rollup do not produce a proof on each involved transaction.  

Ethereum’s Proof-of-Stake (PoS):
1. Post-Merge, Ethereum uses [PoS](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/) with validators staking ETH for block production and finality 
2. Optimism’s state is finalized on Ethereum after the challenge window.
3. Optimism’s [Rollup Consensus](https://docs.optimism.io/stack/protocol/rollup/):
   1. The Sequencer orders transactions and submits batches. Fault proofs ensure validity, with unchallenged states finalized via Ethereum’s PoS.
   2. Reference: Optimism Docs on Rollup Protocol
   3. Interactive Dispute Games. Replacing single-round [fault proofs](https://docs.optimism.io/stack/protocol/fault-proofs/), these reduce disputes to a single instruction which are verified on L1.

Optimism significantly boosts Ethereum’s throughput while keeping [full compatibility with Ethereum EVM](https://docs.optimism.io/stack/getting-started/#evm-equivalence).
Ethereum’s base layer handles ~15-30 TPS due to its [~12-second block time and gas limit](https://ethereum.org/en/developers/docs/blocks/). While Optimism achieves up to 2,000 TPS theoretically, with 2-second block times, by processing [transactions off-chain and batching them to L1](https://docs.optimism.io/stack/protocol/rollup/#transaction-flow).

Optimism offloads consensus to Ethereum’s PoS, using the Sequencer and fault proofs for efficiency. It's viable and proven solution behind well-known DeFi projects. But it exposes a lot of risks if not mitigated such as:
* It exposed to censorship or invalid submissions
* In theory, users can bypass this by submitting [directly to L1](https://docs.optimism.io/stack/rollup/outages#mitigation-1), though at higher cost and latency
* Sequencer overloading by spam transactions, also potentialy introducing forerunning attacks or insertion attacks
* The sequencer becomes prone to [outages](https://docs.optimism.io/stack/rollup/outages) due to sequencing of high influx of transactions at the time 
* Maybe targeted to potential attacks on realization logic by malicious transaction of fraud

**Risk mitigation**
Mitigation should include handling of potential security issues in dApp logic which may cost extra R&D hours.
Decentralized sequencing is planned (OP Stack roadmap). 

## Optimism-based DeFi projects: use case study 
[Uniswap](https://uniswap.org/) on Optimism processed ~1.5 million swaps in a month (March 2023 data), averaging ~500 TPS during peak usage, far exceeding Ethereum’s capacity.
On Ethereum, complex transactions like Uniswap swaps often cost $50-$100 during congestion (e.g., 2021 bull run, gas prices ~200 Gwei https://etherscan.io/gastracker). On Optimism, the same swap costs $0.10-$1, as seen in real-time data from [L2Fees.info](https://l2fees.info/). For instance, a Uniswap V3 swap on Ethereum might cost 150,000 gas ($75 at 100 Gwei), while Optimism batches reduce this to 5,000 gas equivalent ($0.50).
A USDC transfer on Ethereum can cost $10-$20 (e.g., 50,000 gas at 100 Gwei), while on Optimism, it’s ~$0.05-$0.20, enabling micro-transactions.
The 7-day challenge window delays L1 withdrawals unless bridged (for ex. Hop Protocol; https://hop.exchange/).
Known bottlenecks:
* Noted data bottleneck. Pre-EIP-4844, calldata costs limited batch sizes, post-EIP-4844, blobs improved this (https://docs.optimism.io/stack/protocol/eip-4844/).
* Sequencer bottleneck. Centralized sequencing caps throughput under extreme load
Optimism’s 10-100x TPS increase and gas savings (e.g., $50 to $0.50) make it a practical scaling solution, though latency and centralization remain challenges.

[Aave](https://aave.com/).
Offers lending/borrowing with fees dropping from $30-$70 to ~$0.30-$1 on Optimism (https://app.aave.com/markets/). Stablecoin transactions (for ex.) USDC and DAI transfers drop from $10-$20 on Ethereum to ~$0.05-$0.20 on Optimism.

[Arcadia Finance](https://arcadia.finance/).
Native Optimism protocol for margin trading, leveraging low fees for liquidations (~$0.50 vs. $50 on Ethereum).

We can see, that Optimism based DeFi's benefit from gas savings ($50 to $0.50) and much faster execution, but security risks associated with Optimistic rollup architecture should be kept in mind. 

# StarkNet overview
Starknet is a Layer 2 (L2) blockchain solution designed to scale Ethereum by leveraging advanced cryptographic techniques and innovative design principles. It's a permissionless ZK-Rollup Etherum L2 network (referred by authors as Validity Rollup).
Starknet aims to address Ethereum’s scalability limitations while adding additional layer of security.

Starknet’s security and scalability rooted on its use of Zero-Knowledge Scalable Transparent Arguments of Knowledge (ZK-STARKs), a cutting-edge cryptographic proof system developed by StarkWare, the company behind Starknet.
Unlike ZK-SNARKs (used by some other rollups), ZK-STARKs offer distinct advantages:
* ZK-STARKs provide logarithmic verification complexity and proof size, meaning the computational effort to verify a proof grows very slowly relative to the size of the computation being proven. This enables Starknet to bundle thousands of transactions into a single proof and reduce on-chain costs sufficiently.
* They are "transparent," requiring no trusted setup (unlike ZK-SNARKs), which enhances security and reduces complexity associated with bootsprapping of Trusted Setup (according to "STARKs vs. SNARKs" [Ref: https://hacken.io/discover/zk-snark-vs-zk-stark/])
* ZK-STARKs rely on collision-resistant hash functions and on specific polynomial constraints used to describe problem domain in terms of polynomials. This technical innovation results in two main things. The lower number of circuits needed to model domain problem with polynomial constraints then SNARK's QAP (quadratic arithmetic programms), which are similar but restricted to model domain problem through quadratic polynomials. Combination of polynomial based problems and hash functions makes StarkNet resistant to potential attacker with quantum computer. While SNARK's are utilizing elliptical curve cryptography which is unsecure under quantum attacker assumptions. Further details stated "Cryptographic Building Blocks" [Ref: https://docs.starknet.io/documentation/architecture_and_concepts/cryptography/]] and in the original STARK paper by Eli Ben-Sasson et al., "Scalable, Transparent, and Post-Quantum Secure Computational Integrity" (2018) [Ref: https://eprint.iacr.org/2018/046]. 

Starknet generates STARK proofs off-chain using a prover (e.g., the Stone Prover or its successor, [Stwo](https://github.com/starkware-libs/stwo)), which validates the integrity of a batch of transactions. These proofs are then submitted to Ethereum, where a Solidity-based STARK Verifier contract checks their validity. See "STARK Verifier" in Starknet docs [Ref: https://docs.starknet.io/architecture-and-concepts/provers-overview/] and "Introducing Stwo" (2024) [Ref: https://starkware.co/blog/introducing-stwo/].
The system itself uses Cairo, a Turing-complete programming language and virtual machine (VM) from StarkWare to write smart contracts and generate provable computations. Cairo’s intermediate representation (Sierra) ensures that every program execution can be proven efficiently. See "Cairo & Sierra" [Ref: https://docs.starknet.io/architecture-and-concepts/smart-contracts/cairo-and-sierra/].

The cryptography stack’s security is rooted in ZK-STARKs’ peer-reviewed properties [IACR 2018/046] and Starknet’s implementation specifics [starknet.io docs].

Security:
* By proving computational integrity off-chain and verifying it on-chain, Starknet inherits Ethereum’s L1 security
* Any invalid state transition is rejected because only proofs passing the STARK-verifier are accepted
* The use of state diffs (differences between consecutive states) published on-chain ensures data availability, allowing anyone to reconstruct and verify the Starknet state independently

## Starknet's Consensus Overview
Starknet’s consensus mechanism is evolving as it progresses toward decentralization roadmap [Ref: https://www.starknet.io/developers/roadmap/]. As of March 24, 2025, it operates as a Validity Rollup with a hybrid approach to consensus, leveraging Ethereum’s security while introducing its own mechanisms for L2 operations.

Current State (Centralized Sequencer):
Initially, Starknet relies on a single sequencer operated by StarkWare to order and batch transactions. The sequencer generates blocks, computes state transitions, and submits STARK proofs along with state diffs to Ethereum L1.
Ethereum’s Proof-of-Work (prior to the Merge) and now Proof-of-Stake (PoS) consensus secures these updates, as the STARK Verifier contract on L1 validates the proofs ("How Starknet Works" [Ref: https://docs.starknet.io/documentation/getting_started/how_starknet_works/]). This ensures that Starknet’s state transitions are as secure as Ethereum’s, with no possibility of invalid transactions being accepted.
Documentation reference: The Starknet documentation outlines this process under "How Starknet Works" (available on starknet.io), emphasizing the sequencer’s role and Ethereum’s settlement layer.

Transition to Decentralization (Announced in "Starknet Decentralization Update" (2024) [Ref: https://www.starknet.io/blog/decentralized-starknet-2025/]). Starknet is on a roadmap to become fully decentralized, with plans to replace the centralized sequencer with a decentralized network of sequencers and provers. As of early 2025, the first stage of staking has gone live, marking the beginning of its migration to a Proof-of-Stake (PoS) model on L2.
In this future state, the Starknet token (STRK) will be used for staking, allowing participants to secure the network and participate in consensus. The decentralized sequencer layer will be censorship-resistant, with STARK proofs ensuring validity.
The decentralization proposal (detailed in Starknet’s governance documentation on starknet.io) describes how STRK will incentivize honest behavior among sequencers and provers, with slashing mechanisms for malicious actors.

Key Features:
Permissionless Participation: Once decentralized, anyone can run a sequencer or prover, enhancing censorship resistance.
Low Hardware Requirements: STARK proofs allow state verification with minimal computational resources, making it feasible for a wide range of participants to validate the chain.
Parallel Execution: Starknet has introduced parallel transaction execution, enabling multiple transactions to be processed simultaneously, which boosts throughput without compromising security. See "Parallel Execution on Starknet" [Ref: https://starkware.co/blog/parallel-execution-on-starknet/].

In essence, Starknet’s consensus currently relies on Ethereum’s robust L1 security via a centralized sequencer, but its ongoing decentralization efforts aim to introduce a PoS-based L2 consensus that maintains security and scalability. The exact timeline and final design are still evolving, with updates tracked in Starknet’s official documentation and community discussions.

Starknet’s primary goal is to overcome Ethereum’s scalability limitations—namely, its low throughput (around 15-30 transactions per second) and high gas costs. Here’s how it addresses these challenges:
1. In theory, Starknet can bundle up to 12,000–500,000 transactions (depending on type) into a single STARK proof (per the 2024 blog post [Ref: https://starkware.co/blog/parallel-execution-on-starknet/]), achieving a throughput increase of up to 1000x compared to Ethereum L1 (Starknet Performance Metrics" (2024) [Ref: https://starkware.co/blog/starknet-performance-metrics-2024/]). Recent tests have demonstrated sustained network capacity breaking L2 records, with confirmation times as low as 2 seconds.
2. Parallel execution introduced in 2024. This mechanism allows Starknet to process multiple transactions concurrently, further enhancing throughput. This is particularly effective for complex dApps requiring high transaction volumes.
3. Combination of previous factors results in amortizing of gas costs across thousands of transactions. Starknet reduces fees to fraction of cent per transaction, making it economically viable for microtransactions and high-frequency use cases (noted in "Starknet Economics" [Ref: https://docs.starknet.io/documentation/economics/].). 
4. Unlike Optimistic Rollups, which rely on fraud proofs and a challenge period, Starknet’s validity proofs provide immediate finality. This eliminates delays and boosts throughput while maintaining security.
5. Starknet supports application-specific appchains, allowing developers to tailor block size, latency, and consensus parameters to specific use cases. This enables customized throughput optimization.

**Scaling Challenges**.
* Starknet also inherits centralized sequencer bottleneck. Until full decentralization is achieved, the single sequencer could become a throughput limiter under extreme load or a point of failure if offline. The roadmap to decentralized sequencers aims to mitigate this. See [sequencer](https://docs.starknet.io/architecture-and-concepts/network-architecture/starknet-architecture-overview/#sequencers).
* Starknet publishes all state diffs on Ethereum, ensuring security but potentially facing Ethereum’s data capacity constraints. Future integration with Ethereum’s danksharding (EIP-4844) or alternative data availability solutions could address this.
* Generating STARK proofs is computationally intensive, though advancements like the Stwo Prover (using Circle STARKs) have reduced latency and costs ([anounced in 2025](https://www.binance.com/en/square/post/01-02-2025-starknet-2025-940-stwo-18397397206314)). Balancing prover efficiency with throughput remains an ongoing challenge.

Overall, Starknet’s throughput and scaling capabilities are exceptional among L2 solutions, driven by ZK-STARKs and parallel execution. However, its reliance on Ethereum’s infrastructure and the transition to decentralization introduce trade-offs that are actively being addressed.

## Optimism-based DeFi projects: DeFi use case study

Starknet’s combination of security, scalability, and low costs makes it particularly suited for finance-related applications. Below are notable use cases:

DeFi trading platform [dYdX](https://www.dydx.xyz/). Is highly benefit from Starknet's performance.
            
Bitcoin + DeFi (Starknet on Bitcoin and Ethereum (2025) [Ref: https://www.starknet.io/blog/starknet-bitcoin-scaling/]). Starknet is poised to become the first L2 to settle on both Ethereum and Bitcoin (announced in early 2025). This opens the door to Bitcoin-native DeFi, such as using BTC as collateral for loans or trading derivatives.
With Bitcoin’s vast user base (potentially a billion users), Starknet can bring financial-grade functionality to a largely static asset.
The trustless bridge (enabled by STARK proofs and potential Bitcoin covenants via OP_CAT, ensures Bitcoiners retain sovereignty while accessing DeFi, aligning with Bitcoin’s ethos. Bitcoin’s 7 TPS limit is bypassed, enabling complex financial applications without clogging the base layer.

[Braavos](https://braavos.app/). Starknet wallet, integrates Bitcoin Lightning Network payments using STRK, allowing tap-and-pay functionality without extra setup. Reduced confirmation times and high throughput support real-time payments, rivaling traditional systems like Visa. Fraction of cent fees make cross-border remittances viable.
        
These use cases highlight Starknet’s ability to handle finance applications where security (via ZK-STARKs and Ethereum) and scalability (via throughput and low fees) are paramount. Its expansion to Bitcoin further amplifies its relevance in the financial blockchain space.

# Sum up
I can see a great potential by using both solution based whether on StarkNet or Optimism. Both projects are not so mature and being actively developed. Potential Optimism based solution can be ready to-go with faster early time-to-market and lower development efforts due to full EVM compatibility. But I believe it lacks security and reliability in a long term. And, I suspect it would be costly to compete with well-established projects like Uniswap and Aave.
My actual bet would be on Starknet. It's a growing technology which can be harnessed while its ecosystem not so saturated with competitors. It's a great investment in future and long-run for readiness to face a hypothetical quantum computer. Not a lot of blockchain can offer such trait, especially if consider [ECC/RSA deprication since 2030](https://www.keyfactor.com/blog/nist-drops-new-deadline-for-pqc-transition/). 
