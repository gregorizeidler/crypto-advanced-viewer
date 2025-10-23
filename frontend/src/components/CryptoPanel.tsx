"use client";

import { motion } from "framer-motion";
import { Search } from "lucide-react";
import { useState } from "react";

interface Props {
  selectedTicker: string;
  onTickerChange: (ticker: string) => void;
}

const POPULAR_CRYPTOS = [
  // Top 10 by Market Cap
  { ticker: "BTC-USD", name: "Bitcoin" },
  { ticker: "ETH-USD", name: "Ethereum" },
  { ticker: "USDT-USD", name: "Tether" },
  { ticker: "BNB-USD", name: "Binance Coin" },
  { ticker: "SOL-USD", name: "Solana" },
  { ticker: "XRP-USD", name: "Ripple" },
  { ticker: "USDC-USD", name: "USD Coin" },
  { ticker: "ADA-USD", name: "Cardano" },
  { ticker: "DOGE-USD", name: "Dogecoin" },
  { ticker: "TRX-USD", name: "TRON" },
  
  // Layer 1 Blockchains
  { ticker: "AVAX-USD", name: "Avalanche" },
  { ticker: "DOT-USD", name: "Polkadot" },
  { ticker: "NEAR-USD", name: "NEAR Protocol" },
  { ticker: "ATOM-USD", name: "Cosmos" },
  { ticker: "FTM-USD", name: "Fantom" },
  { ticker: "ALGO-USD", name: "Algorand" },
  { ticker: "EGLD-USD", name: "MultiversX" },
  { ticker: "HBAR-USD", name: "Hedera" },
  { ticker: "VET-USD", name: "VeChain" },
  { ticker: "ICP-USD", name: "Internet Computer" },
  
  // DeFi Tokens
  { ticker: "LINK-USD", name: "Chainlink" },
  { ticker: "UNI-USD", name: "Uniswap" },
  { ticker: "AAVE-USD", name: "Aave" },
  { ticker: "MKR-USD", name: "Maker" },
  { ticker: "SNX-USD", name: "Synthetix" },
  { ticker: "COMP-USD", name: "Compound" },
  { ticker: "SUSHI-USD", name: "SushiSwap" },
  { ticker: "CRV-USD", name: "Curve DAO" },
  { ticker: "INJ-USD", name: "Injective" },
  { ticker: "RUNE-USD", name: "THORChain" },
  
  // Layer 2 & Scaling
  { ticker: "MATIC-USD", name: "Polygon" },
  { ticker: "OP-USD", name: "Optimism" },
  { ticker: "ARB-USD", name: "Arbitrum" },
  { ticker: "IMX-USD", name: "Immutable X" },
  { ticker: "LRC-USD", name: "Loopring" },
  
  // Memecoins
  { ticker: "SHIB-USD", name: "Shiba Inu" },
  { ticker: "PEPE-USD", name: "Pepe" },
  { ticker: "FLOKI-USD", name: "Floki Inu" },
  { ticker: "BONK-USD", name: "Bonk" },
  { ticker: "WIF-USD", name: "Dogwifhat" },
  
  // Gaming & Metaverse
  { ticker: "SAND-USD", name: "The Sandbox" },
  { ticker: "MANA-USD", name: "Decentraland" },
  { ticker: "AXS-USD", name: "Axie Infinity" },
  { ticker: "GALA-USD", name: "Gala" },
  { ticker: "ENJ-USD", name: "Enjin Coin" },
  { ticker: "CHZ-USD", name: "Chiliz" },
  
  // Classic Cryptos
  { ticker: "LTC-USD", name: "Litecoin" },
  { ticker: "BCH-USD", name: "Bitcoin Cash" },
  { ticker: "ETC-USD", name: "Ethereum Classic" },
  { ticker: "XLM-USD", name: "Stellar" },
  { ticker: "XMR-USD", name: "Monero" },
  { ticker: "ZEC-USD", name: "Zcash" },
  { ticker: "DASH-USD", name: "Dash" },
  
  // Storage & Infrastructure
  { ticker: "FIL-USD", name: "Filecoin" },
  { ticker: "STORJ-USD", name: "Storj" },
  { ticker: "THETA-USD", name: "Theta Network" },
  { ticker: "GRT-USD", name: "The Graph" },
  
  // Other Popular
  { ticker: "APT-USD", name: "Aptos" },
  { ticker: "FET-USD", name: "Fetch.ai" },
  { ticker: "OCEAN-USD", name: "Ocean Protocol" },
  { ticker: "ROSE-USD", name: "Oasis Network" },
  { ticker: "FLOW-USD", name: "Flow" },
  { ticker: "KSM-USD", name: "Kusama" },
  { ticker: "CELO-USD", name: "Celo" },
  { ticker: "ONE-USD", name: "Harmony" },
  { ticker: "KAVA-USD", name: "Kava" },
];

export default function CryptoPanel({ selectedTicker, onTickerChange }: Props) {
  const [search, setSearch] = useState("");

  const filteredCryptos = POPULAR_CRYPTOS.filter(
    (crypto) =>
      crypto.ticker.toLowerCase().includes(search.toLowerCase()) ||
      crypto.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-xl p-6"
    >
      <div className="mb-4">
        <h3 className="text-xl font-bold text-white mb-4">
          Select Crypto for Analysis
        </h3>
        
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search by ticker or name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Crypto Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2 max-h-[500px] overflow-y-auto custom-scrollbar">
        {filteredCryptos.map((crypto) => (
          <motion.button
            key={crypto.ticker}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onTickerChange(crypto.ticker)}
            className={`
              p-4 rounded-lg transition-all text-left
              ${
                selectedTicker === crypto.ticker
                  ? "bg-blue-600 border-2 border-blue-400"
                  : "bg-gray-800/50 border-2 border-transparent hover:bg-gray-800"
              }
            `}
          >
            <p className="font-bold text-white text-sm">{crypto.ticker}</p>
            <p className="text-xs text-gray-400 mt-1 truncate">{crypto.name}</p>
          </motion.button>
        ))}
      </div>

      {filteredCryptos.length === 0 && (
        <p className="text-center text-gray-400 py-8">
          No cryptocurrencies found
        </p>
      )}
    </motion.div>
  );
}
