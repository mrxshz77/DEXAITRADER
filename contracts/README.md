# DEXAITRADER - Smart Contracts

## Overview

This directory contains all Solidity smart contracts for the DEXAITRADER platform.

### Contracts

1. **PerpetualsDEX.sol** - Main perpetual futures contract
   - Position opening/closing with leverage
   - Margin requirements and liquidation mechanics
   - Funding rates
   - Risk management

2. **FlashLoanArbitrage.sol** - Capital-free arbitrage
   - Aave flash loan integration
   - Multi-DEX arbitrage (Uniswap ↔ SushiSwap)
   - Automated profit capture

3. **LiquidationHunter.sol** - Liquidation opportunity bot
   - Monitor underwater positions
   - Identify liquidation targets
   - Execute and claim rewards

4. **YieldFarm.sol** - Yield farming & staking
   - LP token staking
   - Reward distribution
   - APY calculations

## Setup

### Installation

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Clone and setup
git clone https://github.com/mrxshz77/DEXAITRADER.git
cd contracts
forge install
```

### Compile Contracts

```bash
forge build
```

### Run Tests

```bash
forge test
```

### Deploy

```bash
# Deploy to testnet (Sepolia)
forge script script/Deploy.s.sol --rpc-url $SEPOLIA_RPC_URL --private-key $PRIVATE_KEY --broadcast

# Deploy to mainnet (be careful!)
forge script script/Deploy.s.sol --rpc-url $MAINNET_RPC_URL --private-key $PRIVATE_KEY --broadcast
```

## Environment Variables

Create `.env` file:

```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
MAINNET_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_key
```

## Security Considerations

⚠️ **IMPORTANT:**
- These contracts handle real funds - use testnet first
- Never commit private keys
- Get audited before mainnet deployment
- Test thoroughly with small amounts first
- Consider insurance for edge cases

## Contract Interactions

### Opening a Perpetual Position

```solidity
PerpetualsDEX dex = PerpetualsDEX(0x...);

dex.openPosition(
    OrderType.LONG,        // Long position
    50,                    // 50x leverage
    1000e18,              // 1000 USDT margin
    50000e18,             // Entry price
    49000e18,             // Stop loss
    60000e18              // Take profit
);
```

### Executing Flash Loan Arbitrage

```solidity
FlashLoanArbitrage arb = FlashLoanArbitrage(0x...);

arb.executeArbitrage(
    USDC,          // Token A
    DAI,           // Token B
    10000e6,       // 10k USDC
    true           // Uniswap first
);
```

### Staking for Yield

```solidity
YieldFarm farm = YieldFarm(0x...);

// Approve LP tokens
lpToken.approve(address(farm), amount);

// Stake
farm.stake(poolId, amount);

// Harvest rewards
farm.harvestRewards(poolId);
```

## Testing

```bash
# Test specific contract
forge test --match-contract PerpetualsDEXTest

# Test with logs
forge test -vvv

# Check coverage
forge coverage
```

## Gas Optimization Tips

- Use uint256 instead of smaller types when possible
- Batch operations together
- Use events instead of storage when tracking history
- Consider layer-2 deployment for lower fees

## Support

- [Solidity Docs](https://docs.soliditylang.org/)
- [Foundry Book](https://book.getfoundry.sh/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

---

**Last Updated:** 2026-05-20
