"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import AdvancedAnalysis from "@/components/AdvancedAnalysis";
import { Search, ArrowLeft, Microscope } from "lucide-react";

export default function AnaliseAvancadaPage() {
  const [ticker, setTicker] = useState("BTC-USD");
  const [searchInput, setSearchInput] = useState("");

  const popularCryptos = [
    { ticker: "BTC-USD", name: "Bitcoin" },
    { ticker: "ETH-USD", name: "Ethereum" },
    { ticker: "SOL-USD", name: "Solana" },
    { ticker: "ADA-USD", name: "Cardano" },
    { ticker: "DOT-USD", name: "Polkadot" },
    { ticker: "AVAX-USD", name: "Avalanche" },
    { ticker: "MATIC-USD", name: "Polygon" },
    { ticker: "LINK-USD", name: "Chainlink" },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      const formattedTicker = searchInput.includes("-USD") 
        ? searchInput 
        : `${searchInput.toUpperCase()}-USD`;
      setTicker(formattedTicker);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="p-8">
        {/* Back Button */}
        <Link href="/">
          <motion.button
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Dashboard
          </motion.button>
        </Link>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-2">
            <Microscope className="w-10 h-10 text-purple-500" />
            <h1 className="text-4xl font-bold gradient-text">
              Advanced Analysis
            </h1>
          </div>
          <p className="text-gray-400">
            20+ professional analyses for intelligent trading decisions
          </p>
        </motion.div>

        {/* Search and Quick Select */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 space-y-4"
        >
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="flex gap-2">
            <div className="flex-1 relative">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Enter ticker (e.g. BTC, ETH, SOL)..."
                className="w-full glass border border-gray-700 rounded-lg px-4 py-3 pl-10 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
              />
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            </div>
            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-lg font-semibold transition-all shadow-lg shadow-purple-500/50"
            >
              Analyze
            </button>
          </form>

          {/* Quick Select */}
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-400 flex items-center mr-2">Quick:</span>
            {popularCryptos.map((crypto) => (
              <motion.button
                key={crypto.ticker}
                onClick={() => setTicker(crypto.ticker)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${
                  ticker === crypto.ticker
                    ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg shadow-purple-500/50"
                    : "glass text-gray-400 hover:text-white border border-gray-700 hover:border-gray-600"
                }`}
              >
                {crypto.name}
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* Current Ticker Display */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-6 glass rounded-xl p-6 border border-purple-500/30"
        >
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-400">Analyzing</div>
              <div className="text-3xl font-bold gradient-text">{ticker}</div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-400">Available Analyses</div>
              <div className="text-2xl font-bold text-purple-400">20+</div>
              <div className="text-xs text-gray-500 mt-1">Real-time updates</div>
            </div>
          </div>
        </motion.div>

        {/* Advanced Analysis Component */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <AdvancedAnalysis ticker={ticker} />
        </motion.div>

        {/* Footer Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-12 glass rounded-xl p-6 border border-gray-800"
        >
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Microscope className="w-5 h-5 text-purple-500" />
            About the Analyses
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-400">
            <div>
              <div className="font-semibold text-white mb-1">1-7: Trend Analysis</div>
              <p>Divergences, Gaps, Breakouts, Support/Resistance, Momentum, Relative Strength, Mean Reversion</p>
            </div>
            <div>
              <div className="font-semibold text-white mb-1">8-14: Signals & Patterns</div>
              <p>Swing Trading, Seasonality, Volatility, Patterns, Statistics, Anomalies, Consensus</p>
            </div>
            <div>
              <div className="font-semibold text-white mb-1">15-20: Practical Tools</div>
              <p>Watchlist Compare, Trade Planner, Fast Movers, DCA Simulator, Entry Checklist, Fibonacci Time</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
