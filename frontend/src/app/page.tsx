"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Sidebar from "@/components/Sidebar";
import CandlestickChart from "@/components/CandlestickChart";
import IndicatorsChart from "@/components/IndicatorsChart";
import SectorsHeatmap from "@/components/SectorsHeatmap";
import CryptoRanking from "@/components/CryptoRanking";
import ComparisonChart from "@/components/ComparisonChart";
import CryptoPanel from "@/components/CryptoPanel";
import CryptoChart from "@/components/CryptoChart";
import LiveMarketFeed from "@/components/LiveMarketFeed";
import { TrendingUp, Activity, BarChart3, Microscope } from "lucide-react";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedTicker, setSelectedTicker] = useState("BTC-USD");
  const [period, setPeriod] = useState("1y");
  const [loading, setLoading] = useState(false);

  // State for data
  const [stockData, setStockData] = useState<any>(null);
  const [sectors, setSectors] = useState<any[]>([]);
  const [ranking, setRanking] = useState<any[]>([]);
  const [comparison, setComparison] = useState<any>(null);
  const [sp500Index, setSP500Index] = useState<any>(null);

  // Load selected stock data
  useEffect(() => {
    loadStockData();
  }, [selectedTicker, period]);

  // Load general data
  useEffect(() => {
    loadGeneralData();
  }, []);

  const loadStockData = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/sp500/stock/${selectedTicker}?period=${period}`
      );
      const data = await response.json();
      setStockData(data);
    } catch (error) {
      console.error("Error loading stock data:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadGeneralData = async () => {
    try {
      // Load sectors
      const resSectors = await fetch("http://localhost:8000/api/sp500/sectors");
      const dataSectors = await resSectors.json();
      setSectors(dataSectors.sectors || []);

      // Load ranking
      const resRanking = await fetch("http://localhost:8000/api/sp500/ranking?type=change");
      const dataRanking = await resRanking.json();
      setRanking(dataRanking.ranking || []);

      // Load Bitcoin index
      const resIndex = await fetch("http://localhost:8000/api/sp500/index?period=1y");
      const dataIndex = await resIndex.json();
      setSP500Index(dataIndex);

      // Load comparison (TOP 10 Cryptos by market cap)
      const comparisonTickers = "BTC-USD,ETH-USD,BNB-USD,SOL-USD,XRP-USD,ADA-USD,DOGE-USD,MATIC-USD,DOT-USD,AVAX-USD";
      const resComp = await fetch(
        `http://localhost:8000/api/sp500/comparison?tickers=${comparisonTickers}&period=1y`
      );
      const dataComp = await resComp.json();
      setComparison(dataComp);
    } catch (error) {
      console.error("Error loading general data:", error);
    }
  };

  const periods = [
    { value: "1mo", label: "1M" },
    { value: "3mo", label: "3M" },
    { value: "6mo", label: "6M" },
    { value: "1y", label: "1Y" },
    { value: "2y", label: "2Y" },
    { value: "5y", label: "5Y" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      
      <div className="ml-64 p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Crypto Viewer - Bitcoin & Altcoins
          </h1>
          <p className="text-gray-400">
            Advanced Cryptocurrency Market Analysis Platform - 100+ Cryptos
          </p>
        </motion.div>

        {/* Main Content */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            {/* Quick Access Buttons */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              <motion.a
                href="/analise"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="glass rounded-xl p-6 hover:bg-gray-800/60 transition-all group cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg group-hover:scale-110 transition-transform">
                    <Activity className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-1">Technical Analysis</h3>
                    <p className="text-sm text-gray-400">
                      Technical score, candle patterns, volume profile and indicators
                    </p>
                  </div>
                </div>
              </motion.a>

              <motion.a
                href="/analise-avancada"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="glass rounded-xl p-6 hover:bg-gray-800/60 transition-all group cursor-pointer border-2 border-purple-500/30"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg group-hover:scale-110 transition-transform">
                    <Microscope className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-1">Advanced Analysis 🔬</h3>
                    <p className="text-sm text-gray-400">
                      20+ professional analyses: gaps, breakouts, DCA simulator, and more
                    </p>
                  </div>
                </div>
              </motion.a>

              <motion.a
                href="/professional-tools"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
                className="glass rounded-xl p-6 hover:bg-gray-800/60 transition-all group cursor-pointer border-2 border-cyan-500/30"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-gradient-to-br from-cyan-600 to-blue-600 rounded-lg group-hover:scale-110 transition-transform">
                    <TrendingUp className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-1">Professional Tools 🚀</h3>
                    <p className="text-sm text-gray-400">
                      18 advanced tools: Ichimoku, Monte Carlo, risk management and more
                    </p>
                  </div>
                </div>
              </motion.a>

              <motion.a
                href="/ferramentas"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="glass rounded-xl p-6 hover:bg-gray-800/60 transition-all group cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-gradient-to-br from-orange-600 to-red-600 rounded-lg group-hover:scale-110 transition-transform">
                    <BarChart3 className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-1">Advanced Tools</h3>
                    <p className="text-sm text-gray-400">
                      Crypto screener, comparator and market cap treemap
                    </p>
                  </div>
                </div>
              </motion.a>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-400">Bitcoin (BTC)</h3>
                  <TrendingUp className="w-5 h-5 text-blue-400" />
                </div>
                {sp500Index && (
                  <>
                    <p className="text-2xl font-bold text-white">
                      ${sp500Index.data[sp500Index.data.length - 1]?.close.toLocaleString('en-US')}
                    </p>
                    <p className={`text-sm font-medium mt-1 ${
                      sp500Index.day_change >= 0 ? "text-green-400" : "text-red-400"
                    }`}>
                      {sp500Index.day_change >= 0 ? "+" : ""}
                      {sp500Index.day_change}% today
                    </p>
                  </>
                )}
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 }}
                className="glass rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-400">Categories Up</h3>
                  <Activity className="w-5 h-5 text-green-400" />
                </div>
                <p className="text-2xl font-bold text-white">
                  {sectors.filter(s => s.change > 0).length}
                </p>
                <p className="text-sm text-gray-400 mt-1">
                  of {sectors.length} categories
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="glass rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-medium text-gray-400">Cryptos Monitored</h3>
                  <BarChart3 className="w-5 h-5 text-purple-400" />
                </div>
                <p className="text-2xl font-bold text-white">100+</p>
                <p className="text-sm text-gray-400 mt-1">Cryptocurrencies available</p>
              </motion.div>
            </div>

            {/* Bitcoin Chart */}
            {sp500Index && (
              <CryptoChart data={sp500Index.data} change={sp500Index.period_change} />
            )}

            {/* Live Market Feed */}
            <LiveMarketFeed />

            {/* Charts Grid */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <SectorsHeatmap sectors={sectors} />
              <CryptoRanking stocks={ranking.slice(0, 20)} type="change" />
            </div>

            {/* Stock Comparison */}
            {comparison && (
              <ComparisonChart 
                data={comparison.comparison} 
                tickers={comparison.tickers}
              />
            )}
          </div>
        )}

        {activeTab === "analysis" && (
          <div className="space-y-6">
            {/* Crypto Selector */}
            <CryptoPanel 
              selectedTicker={selectedTicker}
              onTickerChange={setSelectedTicker}
            />

            {/* Period Controls */}
            <div className="glass rounded-xl p-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-white">Analysis Period</h3>
                <div className="flex gap-2">
                  {periods.map((p) => (
                    <button
                      key={p.value}
                      onClick={() => setPeriod(p.value)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                        period === p.value
                          ? "bg-blue-600 text-white"
                          : "bg-gray-700 text-gray-300 hover:bg-gray-600"
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Candlestick Chart */}
            {stockData && !loading && (
              <>
                <CandlestickChart
                  ticker={selectedTicker}
                  data={stockData.data}
                  showVolume={true}
                  height={500}
                />

                {/* Technical Indicators */}
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                  <IndicatorsChart
                    data={stockData.data}
                    type="rsi"
                    ticker={selectedTicker}
                  />
                  <IndicatorsChart
                    data={stockData.data}
                    type="macd"
                    ticker={selectedTicker}
                  />
                </div>

                <IndicatorsChart
                  data={stockData.data}
                  type="bollinger"
                  ticker={selectedTicker}
                />
              </>
            )}

            {loading && (
              <div className="glass rounded-xl p-12 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                <p className="text-gray-400 mt-4">Loading data...</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "ranking" && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <CryptoRanking stocks={ranking} type="change" />
              {/* Can add volume ranking here */}
            </div>
          </div>
        )}

        {activeTab === "sectors" && (
          <div className="space-y-6">
            <SectorsHeatmap sectors={sectors} />
            
            {/* Category Details */}
            <div className="glass rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">
                Detailed Analysis by Category
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {sectors.map((sector, index) => (
                  <motion.div
                    key={sector.sector}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="bg-gray-800/50 rounded-lg p-4"
                  >
                    <h4 className="font-semibold text-white mb-2">{sector.sector}</h4>
                    <p className={`text-2xl font-bold ${
                      sector.change >= 0 ? "text-green-400" : "text-red-400"
                    }`}>
                      {sector.change >= 0 ? "+" : ""}
                      {sector.change.toFixed(2)}%
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "comparison" && comparison && (
          <div className="space-y-6">
            <ComparisonChart 
              data={comparison.comparison} 
              tickers={comparison.tickers}
            />
          </div>
        )}
      </div>
    </div>
  );
}
