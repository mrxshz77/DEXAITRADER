# 🤖 DEXAITRADER - Advanced DEX Trading Platform

**The most powerful AI-driven decentralized futures trading platform with autonomous bot management, advanced charting, and real-time AI co-pilot.**

## 🎯 Core Features

### 🔥 God Mode Trading Interface
- **Canvas Overlay**: Dynamic HTML5 Canvas on TradingView charts
- **Shift+Mouse Interaction**: Real-time risk-free line and stop-loss calculation
- **One-Click Execution**: Instant market orders and kill-switch
- **Auto-Close**: Automatic position closure at target profit %

### 🤖 AI Co-Pilot Agent
- **File System Access**: Read/write entire codebase
- **Strategy Generation**: Auto-create bots from natural language prompts
- **Local LLM Integration**: Ollama (Llama-3) for 0-latency analysis
- **Code Execution**: Run strategies in background with live results

### 🎮 Advanced Bot Factory
- **Code Mode**: Write raw Python/Pandas strategies
- **No-Code Mode**: Visual block builder for indicators
- **AI Model Mode**: Load pre-trained PyTorch (.pt) or ONNX models
- **Reinforcement Learning**: Gym environment for strategy self-optimization

### 💰 Advanced Features
- **Perpetual Futures**: With leverage, liquidation, and margin management
- **Arbitrage Bot**: Multi-DEX flash loan arbitrage with automated execution
- **Flash Loans**: Integration with Aave/Uniswap for capital-free arbitrage
- **Liquidation Hunting**: Identify and liquidate underwater positions for profit
- **Liquidity Pools**: Create, manage, and farm yield from LP tokens
- **Yield Farming**: Automated yield optimization across protocols
- **Backtesting**: Historical performance testing with realistic slippage
- **Paper Trading**: Risk-free simulation mode with zero latency

### 📊 Professional Chart Features
- **TradingView Lightweight Charts**: Highly customized for futures trading
- **Advanced Indicators**: RSI, Bollinger Bands, MACD, EMA, SMA, ATR, etc.
- **Drawing Tools**: Trendlines, channels, support/resistance levels
- **Multi-Timeframe**: Analyze multiple charts simultaneously
- **Real-time WebSocket**: Sub-second price updates

### 🔐 Security & Control
- **Non-custodial**: Your keys, your funds
- **Local Execution**: AI runs locally - no cloud dependencies
- **Simulation Mode**: Test everything before going live
- **Risk Management**: Built-in position sizing and stop-loss enforcement

---

## 📁 Project Structure

```
DEXAITRADER/
├── frontend/                    # Next.js 14 (App Router)
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── trading/
│   │   │   ├── page.tsx        # Main trading interface
│   │   │   ├── chart.tsx       # Chart component
│   │   │   └── layout.tsx
│   │   ├── ai-terminal/
│   │   │   ├── page.tsx        # AI Chat interface
│   │   │   └── layout.tsx
│   │   ├── bot-builder/
│   │   │   ├── page.tsx        # Bot creation UI
│   │   │   └── layout.tsx
│   │   └── settings/
│   │       └── page.tsx        # Configuration
│   ├── components/
│   │   ├── Chart.tsx           # TradingView integration
│   │   ├── CanvasOverlay.tsx   # Shift+Mouse logic
│   │   ├── OrderPanel.tsx      # Order management
│   │   ├── AITerminal.tsx      # Chat interface
│   │   └── BotBuilder.tsx      # Bot creation
│   ├── lib/
│   │   ├── websocket.ts        # WebSocket client
│   │   ├── api.ts              # API calls
│   │   └── types.ts            # TypeScript types
│   ├── styles/
│   │   └── globals.css         # Tailwind CSS
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
│
├── backend/                     # FastAPI (Python)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app
│   │   ├── routes/
│   │   │   ├── orders.py       # Order management
│   │   │   ├── positions.py    # Position tracking
│   │   │   ├── backtest.py     # Backtesting
│   │   │   └── websocket.py    # WebSocket streaming
│   │   ├── models/
│   │   │   ├── order.py        # Order data models
│   │   │   ├── position.py     # Position models
│   │   │   └── trade.py        # Trade models
│   │   ├── services/
│   │   │   ├── dex_connector.py    # DEX integration
│   │   │   ├── price_feed.py       # Price data
│   │   │   ├── order_executor.py   # Order execution
│   │   │   └── liquidation.py      # Liquidation logic
│   │   └── ai/
│   │       ├── agent.py            # LangChain agent
│   │       ├── strategies/         # Strategy store
│   │       └── models/             # ML models
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── contracts/                   # Solidity Smart Contracts
│   ├── src/
│   │   ├── PerpetualsDEX.sol   # Main perpetuals contract
│   │   ├── LiquidationPool.sol # Liquidation hunting
│   │   ├── FlashLoanArb.sol    # Flash loan arbitrage
│   │   └── YieldFarm.sol       # Yield farming
│   ├── test/
│   │   ├── PerpetualsDEX.t.sol
│   │   ├── FlashLoanArb.t.sol
│   │   └── YieldFarm.t.sol
│   ├── foundry.toml
│   └── script/
│       └── Deploy.s.sol
│
├── ai-agent/                    # Standalone AI Agent
│   ├── core/
│   │   ├── agent.py            # Main agent loop
│   │   ├── memory.py           # Chat history & context
│   │   └── code_executor.py    # Safe code execution
│   ├── strategies/
│   │   ├── generator.py        # Strategy generator
│   │   ├── backtester.py       # Backtesting engine
│   │   └── templates/          # Strategy templates
│   ├── rl_environment/
│   │   ├── gym_env.py          # Gym environment
│   │   ├── trader.py           # RL trader
│   │   └── models/             # Trained models
│   ├── prompts/
│   │   └── system_prompt.txt   # Master system prompt
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml          # Full stack orchestration
├── .env.example                # Environment variables
├── .gitignore
└── docs/
    ├── SETUP.md               # Setup guide
    ├── API.md                 # API documentation
    ├── SMART_CONTRACTS.md     # Contract documentation
    ├── AI_AGENT.md            # AI agent guide
    └── TRADING_GUIDE.md       # Trading guide
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/mrxshz77/DEXAITRADER.git
cd DEXAITRADER

# Copy environment
cp .env.example .env

# Start everything with Docker
docker-compose up -d

# Frontend runs on: http://localhost:3000
# Backend runs on: http://localhost:8000
# AI Agent runs on: http://localhost:8001
```

---

## 📚 Documentation

- [Setup & Installation](./docs/SETUP.md)
- [API Reference](./docs/API.md)
- [Smart Contracts](./docs/SMART_CONTRACTS.md)
- [AI Agent Guide](./docs/AI_AGENT.md)
- [Trading Guide](./docs/TRADING_GUIDE.md)

---

## 🎮 Usage Examples

### Manual Trading with Shift+Mouse
1. Open Trading interface
2. Hold **Left Shift**
3. Move mouse to set risk-free line
4. Click to set entry/SL/TP
5. Press **Open Position** button

### AI-Generated Bot
```
In AI Terminal:
"Create a bot using RSI + Bollinger Bands with 50x leverage on BTC/USDT"

→ AI writes strategy
→ Backtests automatically
→ Deploys and runs
→ Shows real-time P&L
```

### Arbitrage Bot
```
AI Terminal:
"Run arbitrage between Uniswap and SushiSwap for USDC/DAI with flash loans"

→ Monitors price differences
→ Executes flash loan
→ Swaps across DEXs
→ Repays + pockets profit
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, TradingView Charts |
| **Backend** | FastAPI, Python, WebSocket |
| **Blockchain** | Solidity, Foundry, Ethereum/Polygon |
| **AI** | LangChain, Ollama (Llama-3), PyTorch, Gym |
| **DevOps** | Docker, Docker Compose, GitHub Actions |

---

## ⚙️ Configuration

Edit `.env` file:

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Backend
BLOCKCHAIN_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
OLLAMA_URL=http://ollama:11434
REDIS_URL=redis://redis:6379

# Trading
SIMULATION_MODE=true  # Set to false for real trading
LEVERAGE_MAX=100x

# Wallet (For testing - NEVER use real keys!)
WALLET_PRIVATE_KEY=your_test_key_here
```

---

## 🤖 AI Agent Capabilities

The AI Agent can:
- ✅ Read entire codebase
- ✅ Write and update strategies
- ✅ Execute backtests
- ✅ Deploy bots
- ✅ Monitor live trades
- ✅ Fine-tune models
- ✅ Generate reports
- ✅ Manage liquidations
- ✅ Execute arbitrage

---

## 📊 Supported Features

- [x] Manual trading with advanced charts
- [x] Perpetual futures with leverage
- [x] One-click execution
- [x] Auto-close at target profit
- [x] AI bot generation
- [x] Backtesting engine
- [x] Flash loan integration
- [x] Liquidation hunting
- [x] Yield farming
- [x] Arbitrage automation
- [x] Real-time WebSocket updates
- [x] Paper trading mode
- [x] RL-based strategy optimization

---

## 🔐 Security Notes

⚠️ **IMPORTANT:**
- This is a development platform. Use on testnet first!
- Never commit real private keys
- Always use `.env` for sensitive data
- Run on testnet before mainnet
- Test all strategies on paper trading first

---

## 📝 License

MIT License - See LICENSE file

---

## 🤝 Support

- Docs: [./docs/](./docs/)
- Issues: [GitHub Issues](https://github.com/mrxshz77/DEXAITRADER/issues)
- Discussions: [GitHub Discussions](https://github.com/mrxshz77/DEXAITRADER/discussions)

---

## 🙏 Acknowledgments

Built with:
- [Next.js](https://nextjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [TradingView Lightweight Charts](https://www.tradingview.com/lightweight-charts/)
- [LangChain](https://www.langchain.com/)
- [Foundry](https://book.getfoundry.sh/)
- [Ollama](https://ollama.ai/)

---

**Ready to trade smarter with AI.** 🚀

Last updated: 2026-05-20
