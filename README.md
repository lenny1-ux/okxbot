# OKX BTC/USDT Spot Trading Bot

Production-grade automated **spot** trading bot for **BTC/USDT** on **OKX** with strict risk controls and deterministic execution. The system prioritizes capital preservation and operational safety over trade frequency.

## Objective

Build a robust, event-driven bot that trades **one position at a time**, with strict risk limits, explicit entry/exit logic, and production-safe execution.

## Core Features

- **OKX official REST + WebSocket APIs**
- **Spot only** (no leverage, no margin, no derivatives)
- **Single trading pair**: BTC/USDT
- **One open position at a time**

## Strategy Layer

- Rule-based (no ML)
- Timeframe: **5m or 15m** candles
- Deterministic entry/exit conditions
- No grid, martingale, or DCA logic

## Risk Management (Non‑Negotiable)

- **Max risk per trade ≤ 1%**
- **Hard stop‑loss required**
- **Daily max loss cap** (bot halts if breached)
- **Max trades/day limit**
- **Emergency kill switch** on API/logic failure

## Execution Rules

- **Market or limit orders only**
- **Confirm fills before state changes**
- **Partial fills handled safely**
- **Retry logic with strict rate‑limit compliance**

## System Architecture

- Modular components:
  - Data ingestion
  - Strategy
  - Risk engine
  - Execution
  - Logging
- Asynchronous execution (event-driven, not polling)
- API keys via env vars (withdrawals disabled)

## Backtesting & Validation

- Historical backtesting with realistic fees + slippage
- No look‑ahead bias / data leakage
- Out‑of‑sample validation required

## Deployment

- Containerized (Docker)
- Runs on Linux VPS
- Persistent logging to PostgreSQL or flat files

## Success Criteria

- Stable for weeks of paper trading
- Tight drawdown control
- Profitability is secondary to survival and correctness

---

## Environment Variables

```bash
OKX_API_KEY=...
OKX_API_SECRET=...
OKX_PASSPHRASE=...
OKX_ENV=paper   # or live
LOG_LEVEL=INFO
```

> **Security Note:** Never enable withdrawals on the API key.

---

## Disclaimer

This software is for educational and research purposes only. Trading carries risk. Use at your own risk.
