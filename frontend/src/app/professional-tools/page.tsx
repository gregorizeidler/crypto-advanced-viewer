"use client";

import { useState } from 'react';
import { ArrowLeft, Search } from 'lucide-react';
import Link from 'next/link';
import ProfessionalTools from '@/components/ProfessionalTools';

export default function ProfessionalToolsPage() {
  const [ticker, setTicker] = useState('BTC-USD');
  const [searchInput, setSearchInput] = useState('');

  const popularCryptos = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'ADA-USD',
    'DOGE-USD', 'XRP-USD', 'DOT-USD', 'MATIC-USD', 'AVAX-USD'
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      // Ensure ticker has -USD suffix if not present
      const formattedTicker = searchInput.toUpperCase().includes('-USD') 
        ? searchInput.toUpperCase() 
        : `${searchInput.toUpperCase()}-USD`;
      setTicker(formattedTicker);
      setSearchInput('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      {/* Top Navigation */}
      <div className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <Link 
              href="/"
              className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="font-semibold">Back to Dashboard</span>
            </Link>

            {/* Current Ticker Display */}
            <div className="hidden md:block">
              <div className="bg-blue-600/20 px-4 py-2 rounded-lg border border-blue-500/30">
                <p className="text-sm text-gray-400">Analyzing</p>
                <p className="text-xl font-bold text-blue-400">{ticker}</p>
              </div>
            </div>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="flex items-center gap-2">
              <div className="relative">
                <input
                  type="text"
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  placeholder="Search crypto..."
                  className="bg-gray-700/50 text-white px-4 py-2 pr-10 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 w-48"
                />
                <button 
                  type="submit"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                >
                  <Search className="w-5 h-5" />
                </button>
              </div>
            </form>
          </div>

          {/* Quick Select Cryptos */}
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-gray-400 text-sm mr-2 self-center">Quick Select:</span>
            {popularCryptos.map((crypto) => (
              <button
                key={crypto}
                onClick={() => setTicker(crypto)}
                className={`px-3 py-1 rounded-lg text-sm font-semibold transition-all ${
                  ticker === crypto
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {crypto.replace('-USD', '')}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <ProfessionalTools ticker={ticker} />
    </div>
  );
}

