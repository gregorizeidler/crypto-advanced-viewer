"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { 
  TrendingUp, TrendingDown, Activity, Target, BarChart3, 
  Clock, AlertTriangle, Zap, Calendar, Shield, PieChart,
  LineChart, DollarSign, CheckCircle, XCircle, Clock3
} from "lucide-react";

interface AdvancedAnalysisProps {
  ticker: string;
}

export default function AdvancedAnalysis({ ticker }: AdvancedAnalysisProps) {
  const [activeTab, setActiveTab] = useState("overview");
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<any>({});

  const tabs = [
    { id: "overview", name: "Overview", icon: BarChart3 },
    { id: "signals", name: "Trading Signals", icon: Target },
    { id: "patterns", name: "Patterns", icon: Activity },
    { id: "statistics", name: "Statistics", icon: PieChart },
    { id: "risk", name: "Risk & Volatility", icon: Shield },
    { id: "tools", name: "Tools", icon: Zap },
  ];

  useEffect(() => {
    loadAllData();
  }, [ticker]);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const endpoints = [
        { key: "divergences", url: `/api/crypto/advanced/divergences/${ticker}` },
        { key: "gaps", url: `/api/crypto/advanced/gaps/${ticker}` },
        { key: "breakout", url: `/api/crypto/advanced/breakout/${ticker}` },
        { key: "support", url: `/api/crypto/advanced/support-resistance/${ticker}` },
        { key: "momentum", url: `/api/crypto/advanced/momentum-multi/${ticker}` },
        { key: "relativeStrength", url: `/api/crypto/advanced/relative-strength/${ticker}` },
        { key: "meanReversion", url: `/api/crypto/advanced/mean-reversion/${ticker}` },
        { key: "swingSignals", url: `/api/crypto/advanced/swing-signals/${ticker}` },
        { key: "seasonality", url: `/api/crypto/advanced/seasonality/${ticker}` },
        { key: "volatility", url: `/api/crypto/advanced/volatility-expanded/${ticker}` },
        { key: "patterns", url: `/api/crypto/advanced/price-patterns/${ticker}` },
        { key: "statistical", url: `/api/crypto/advanced/statistical/${ticker}` },
        { key: "anomalies", url: `/api/crypto/advanced/anomalies/${ticker}` },
        { key: "consensus", url: `/api/crypto/advanced/consensus/${ticker}` },
        { key: "tradePlan", url: `/api/crypto/advanced/trade-planner/${ticker}` },
        { key: "dcaSimulator", url: `/api/crypto/advanced/dca-simulator/${ticker}` },
        { key: "entryChecklist", url: `/api/crypto/advanced/entry-checklist/${ticker}` },
        { key: "fibonacciTime", url: `/api/crypto/advanced/fibonacci-time/${ticker}` },
      ];

      const promises = endpoints.map(async ({ key, url }) => {
        try {
          const res = await fetch(`http://localhost:8000${url}`);
          const json = await res.json();
          return { key, data: json };
        } catch (error) {
          console.error(`Error loading ${key}:`, error);
          return { key, data: null };
        }
      });

      const results = await Promise.all(promises);
      const newData: any = {};
      results.forEach(({ key, data }) => {
        newData[key] = data;
      });
      
      setData(newData);
    } catch (error) {
      console.error("Error loading advanced analysis:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-gray-900 rounded-lg p-8 border border-gray-800">
        <div className="flex flex-col items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-400">Loading advanced analysis...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-lg p-6 border border-purple-800/30">
        <h2 className="text-3xl font-bold text-white mb-2">
          📊 Advanced Analysis - {ticker}
        </h2>
        <p className="text-gray-400">
          20 professional analyses for intelligent decision making
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-400 hover:bg-gray-700"
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.name}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {activeTab === "overview" && <OverviewTab data={data} />}
        {activeTab === "signals" && <SignalsTab data={data} />}
        {activeTab === "patterns" && <PatternsTab data={data} />}
        {activeTab === "statistics" && <StatisticsTab data={data} />}
        {activeTab === "risk" && <RiskTab data={data} />}
        {activeTab === "tools" && <ToolsTab data={data} ticker={ticker} />}
      </motion.div>
    </div>
  );
}

// ===== OVERVIEW TAB =====
function OverviewTab({ data }: { data: any }) {
  const consensus = data.consensus || {};
  const momentum = data.momentum || {};
  const breakout = data.breakout || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Multi-Indicator Consensus */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Target className="w-5 h-5" />
          Multi-Indicator Consensus
        </h3>
        
        {consensus.recommendation && (
          <div className="space-y-4">
            <div className="text-center p-6 bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-lg border border-purple-800/30">
              <div className={`text-4xl font-bold mb-2 ${
                consensus.score > 40 ? "text-green-500" :
                consensus.score < -40 ? "text-red-500" : "text-yellow-500"
              }`}>
                {consensus.score > 0 ? "+" : ""}{consensus.score}
              </div>
              <div className="text-2xl font-semibold text-white">
                {consensus.recommendation}
              </div>
              <div className="text-sm text-gray-400 mt-2">
                Strength: {consensus.strength}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-green-900/20 p-4 rounded-lg border border-green-800/30">
                <div className="text-2xl font-bold text-green-500">{consensus.votes?.BUY || 0}</div>
                <div className="text-sm text-gray-400">BUY Votes</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-2xl font-bold text-gray-400">{consensus.votes?.NEUTRAL || 0}</div>
                <div className="text-sm text-gray-400">Neutral</div>
              </div>
              <div className="bg-red-900/20 p-4 rounded-lg border border-red-800/30">
                <div className="text-2xl font-bold text-red-500">{consensus.votes?.SELL || 0}</div>
                <div className="text-sm text-gray-400">SELL Votes</div>
              </div>
            </div>

            <div className="space-y-2">
              {consensus.signals?.map((signal: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-300">{signal.indicator}</span>
                  <div className="flex items-center gap-2">
                    <span className={`font-semibold ${
                      signal.signal === "BUY" ? "text-green-500" :
                      signal.signal === "SELL" ? "text-red-500" : "text-gray-400"
                    }`}>
                      {signal.signal}
                    </span>
                    <span className="text-sm text-gray-500">{signal.value}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Momentum Multi-Timeframe */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          Momentum Multi-Timeframe
        </h3>
        
        {momentum.momentum && (
          <div className="space-y-4">
            <div className="text-center p-6 bg-gradient-to-r from-blue-900/20 to-cyan-900/20 rounded-lg border border-blue-800/30">
              <div className={`text-4xl font-bold mb-2 ${
                momentum.weighted_score > 20 ? "text-green-500" :
                momentum.weighted_score < -20 ? "text-red-500" : "text-yellow-500"
              }`}>
                {momentum.weighted_score > 0 ? "+" : ""}{momentum.weighted_score}
              </div>
              <div className="text-2xl font-semibold text-white">
                {momentum.classification}
              </div>
              <div className="text-sm text-gray-400 mt-2">
                Trend: {momentum.trend}
              </div>
            </div>

            <div className="space-y-2">
              {Object.entries(momentum.momentum).map(([period, val]: [string, any]) => (
                <div key={period} className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
                  <span className="text-gray-300 capitalize">{period.replace("_", " ")}</span>
                  <div className="flex items-center gap-2">
                    <div className={`font-semibold ${
                      val.change_percent > 0 ? "text-green-500" : "text-red-500"
                    }`}>
                      {val.change_percent > 0 ? "+" : ""}{val.change_percent}%
                    </div>
                    <div className="text-sm text-gray-500">
                      Score: {val.score}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Breakout Scanner */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5" />
          Breakout Scanner
        </h3>
        
        {breakout.breakout !== undefined && (
          <div className="space-y-4">
            {breakout.breakout ? (
              <div className={`p-4 rounded-lg border ${
                breakout.type === "Bullish" 
                  ? "bg-green-900/20 border-green-800/30" 
                  : "bg-red-900/20 border-red-800/30"
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-lg font-semibold text-white">
                    Breakout {breakout.type} Detected!
                  </span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    breakout.signal === "STRONG" ? "bg-green-600" :
                    breakout.signal === "MODERATE" ? "bg-yellow-600" : "bg-gray-600"
                  }`}>
                    {breakout.signal}
                  </span>
                </div>
                <div className="text-2xl font-bold text-white mb-2">
                  Score: {breakout.strength_score}/100
                </div>
              </div>
            ) : (
              <div className="p-4 bg-gray-800 rounded-lg border border-gray-700 text-center">
                <p className="text-gray-400">No breakout detected at the moment</p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400 mb-1">Current Price</div>
                <div className="text-xl font-bold text-white">${breakout.current_price}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400 mb-1">Volume Ratio</div>
                <div className={`text-xl font-bold ${
                  breakout.volume_ratio > 1.5 ? "text-green-500" : "text-gray-400"
                }`}>
                  {breakout.volume_ratio}x
                </div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400 mb-1">Máxima 52s</div>
                <div className="text-lg text-white">${breakout.high_52w}</div>
                <div className="text-xs text-gray-500">{breakout.distance_to_high}% away</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400 mb-1">Mínima 52s</div>
                <div className="text-lg text-white">${breakout.low_52w}</div>
                <div className="text-xs text-gray-500">{breakout.distance_to_low}% above</div>
              </div>
            </div>

            {breakout.consolidating && (
              <div className="p-3 bg-yellow-900/20 border border-yellow-800/30 rounded-lg">
                <p className="text-yellow-500 text-sm flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  Consolidação detectada - potencial breakout iminente
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Mean Reversion */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          Mean Reversion (Z-Score)
        </h3>
        
        {data.meanReversion && (
          <div className="space-y-4">
            <div className="text-center p-6 bg-gradient-to-r from-orange-900/20 to-red-900/20 rounded-lg border border-orange-800/30">
              <div className={`text-5xl font-bold mb-2 ${
                Math.abs(data.meanReversion.z_score) > 2 ? "text-red-500" :
                Math.abs(data.meanReversion.z_score) > 1 ? "text-yellow-500" : "text-green-500"
              }`}>
                {data.meanReversion.z_score}
              </div>
              <div className="text-xl font-semibold text-white">
                {data.meanReversion.signal}
              </div>
              <div className="text-sm text-gray-400 mt-2">
                Reversion Probability: {data.meanReversion.reversion_probability}%
              </div>
            </div>

            <div className="p-4 bg-gray-800 rounded-lg">
              <p className="text-gray-300 mb-2">💡 {data.meanReversion.recommendation}</p>
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <div className="text-sm text-gray-400">Current Price</div>
                  <div className="text-lg font-bold text-white">${data.meanReversion.current_price}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">SMA 20</div>
                  <div className="text-lg font-bold text-white">${data.meanReversion.sma}</div>
                </div>
              </div>
            </div>

            <div className="p-4 bg-gray-800 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Bollinger %B</div>
              <div className="w-full bg-gray-700 rounded-full h-4 relative">
                <div 
                  className={`h-full rounded-full ${
                    data.meanReversion.bb_percent > 80 ? "bg-red-500" :
                    data.meanReversion.bb_percent < 20 ? "bg-green-500" : "bg-yellow-500"
                  }`}
                  style={{ width: `${Math.min(100, Math.max(0, data.meanReversion.bb_percent))}%` }}
                ></div>
                <div className="text-xs text-white text-center mt-1">
                  {data.meanReversion.bb_percent}%
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ===== SIGNALS TAB =====
function SignalsTab({ data }: { data: any }) {
  const swingSignals = data.swingSignals || {};
  const tradePlan = data.tradePlan || {};
  const entryChecklist = data.entryChecklist || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Swing Trading Signals */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Target className="w-5 h-5" />
          Swing Trading Signals
        </h3>
        
        {swingSignals.setup_found ? (
          <div className="space-y-4">
            <div className={`p-4 rounded-lg border ${
              swingSignals.type === "BULLISH"
                ? "bg-green-900/20 border-green-800/30"
                : "bg-red-900/20 border-red-800/30"
            }`}>
              <div className="text-xl font-bold text-white mb-2">
                Setup {swingSignals.type} Found!
              </div>
              <div className="text-gray-300">
                Confidence: {swingSignals.confidence}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Entry</div>
                <div className="text-xl font-bold text-white">${swingSignals.entry}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Stop Loss</div>
                <div className="text-xl font-bold text-red-500">${swingSignals.stop_loss}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Take Profit</div>
                <div className="text-xl font-bold text-green-500">${swingSignals.take_profit}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">R:R Ratio</div>
                <div className="text-xl font-bold text-blue-500">1:{swingSignals.risk_reward_ratio}</div>
              </div>
            </div>

            <div className="p-4 bg-gray-800 rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-400">Risk</div>
                  <div className="text-lg text-red-400">${swingSignals.risk}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Reward</div>
                  <div className="text-lg text-green-400">${swingSignals.reward}</div>
                </div>
              </div>
            </div>

            <div className="p-3 bg-blue-900/20 border border-blue-800/30 rounded-lg">
              <p className="text-blue-400 text-sm">
                ⏰ Validity: {swingSignals.validity_days} days
              </p>
            </div>
          </div>
        ) : (
          <div className="p-4 bg-gray-800 rounded-lg text-center">
            <p className="text-gray-400">No swing trading setup at the moment</p>
            {swingSignals.reason && (
              <p className="text-sm text-gray-500 mt-2">{swingSignals.reason}</p>
            )}
          </div>
        )}
      </div>

      {/* Trade Planner */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <LineChart className="w-5 h-5" />
          Trade Planner
        </h3>
        
        {tradePlan.direction && (
          <div className="space-y-4">
            <div className={`p-4 rounded-lg border ${
              tradePlan.direction === "LONG"
                ? "bg-green-900/20 border-green-800/30"
                : "bg-red-900/20 border-red-800/30"
            }`}>
              <div className="text-xl font-bold text-white mb-2">
                Direction: {tradePlan.direction}
              </div>
              <div className="text-lg text-gray-300">
                Current Price: ${tradePlan.current_price}
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Entry Zone</div>
              <div className="flex justify-between items-center">
                <div className="text-green-500">${tradePlan.entry_zone?.low}</div>
                <div className="text-gray-500">→</div>
                <div className="text-green-500">${tradePlan.entry_zone?.high}</div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-red-900/20 p-4 rounded-lg border border-red-800/30">
                <div className="text-sm text-gray-400">Stop Loss</div>
                <div className="text-xl font-bold text-red-500">${tradePlan.stop_loss}</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">ATR</div>
                <div className="text-xl font-bold text-white">${tradePlan.atr}</div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="bg-green-900/20 p-4 rounded-lg border border-green-800/30">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">Target 1</span>
                  <span className="text-sm text-gray-400">R:R {tradePlan.risk_reward_1}</span>
                </div>
                <div className="text-xl font-bold text-green-500">${tradePlan.targets?.target_1}</div>
                <div className="text-sm text-gray-400">Reward: ${tradePlan.reward_1}</div>
              </div>

              <div className="bg-green-900/20 p-4 rounded-lg border border-green-800/30">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-400">Target 2</span>
                  <span className="text-sm text-gray-400">R:R {tradePlan.risk_reward_2}</span>
                </div>
                <div className="text-xl font-bold text-green-500">${tradePlan.targets?.target_2}</div>
                <div className="text-sm text-gray-400">Reward: ${tradePlan.reward_2}</div>
              </div>
            </div>

            <div className="p-3 bg-blue-900/20 border border-blue-800/30 rounded-lg">
              <div className="text-sm text-gray-400">Total Risk</div>
              <div className="text-lg font-bold text-white">${tradePlan.risk}</div>
            </div>
          </div>
        )}
      </div>

      {/* Entry Checklist */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 lg:col-span-2">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <CheckCircle className="w-5 h-5" />
          Entry Checklist
        </h3>
        
        {entryChecklist.checks && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded-lg text-center">
                <div className="text-3xl font-bold text-white">{entryChecklist.score}</div>
                <div className="text-sm text-gray-400">Score</div>
              </div>
              <div className={`p-4 rounded-lg text-center ${
                entryChecklist.decision === "GO" ? "bg-green-900/20 border border-green-800/30" :
                entryChecklist.decision === "GO WITH CAUTION" ? "bg-yellow-900/20 border border-yellow-800/30" :
                "bg-red-900/20 border border-red-800/30"
              }`}>
                <div className={`text-2xl font-bold ${
                  entryChecklist.decision === "GO" ? "text-green-500" :
                  entryChecklist.decision === "GO WITH CAUTION" ? "text-yellow-500" :
                  "text-red-500"
                }`}>
                  {entryChecklist.decision}
                </div>
                <div className="text-sm text-gray-400">Decision</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-white">{entryChecklist.confidence}</div>
                <div className="text-sm text-gray-400">Confidence</div>
              </div>
            </div>

            <div className="space-y-2">
              {entryChecklist.checks.map((check: any, idx: number) => (
                <div 
                  key={idx}
                  className={`flex items-center justify-between p-4 rounded-lg ${
                    check.status === "PASS" ? "bg-green-900/20 border border-green-800/30" :
                    check.status === "WARNING" ? "bg-yellow-900/20 border border-yellow-800/30" :
                    "bg-red-900/20 border border-red-800/30"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {check.status === "PASS" ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : check.status === "WARNING" ? (
                      <AlertTriangle className="w-5 h-5 text-yellow-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500" />
                    )}
                    <span className="font-semibold text-white">{check.check}</span>
                  </div>
                  <span className="text-sm text-gray-400">{check.detail}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ===== PATTERNS TAB =====
function PatternsTab({ data }: { data: any }) {
  const patterns = data.patterns || {};
  const divergences = data.divergences || {};
  const gaps = data.gaps || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Price Action Patterns */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          Price Action Patterns
        </h3>
        
        {patterns.patterns && patterns.patterns.length > 0 ? (
          <div className="space-y-3">
            {patterns.patterns.map((pattern: any, idx: number) => (
              <div 
                key={idx}
                className={`p-4 rounded-lg border ${
                  pattern.type === "Bullish"
                    ? "bg-green-900/20 border-green-800/30"
                    : "bg-red-900/20 border-red-800/30"
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="text-lg font-bold text-white">{pattern.pattern}</div>
                    <div className="text-sm text-gray-400">{pattern.type}</div>
                  </div>
                  <span className="px-3 py-1 bg-gray-800 rounded-full text-sm">
                    {pattern.confidence}% confiança
                  </span>
                </div>
                <p className="text-gray-300 text-sm mb-2">{pattern.description}</p>
                {pattern.target && (
                  <div className="text-sm">
                    <span className="text-gray-400">Target: </span>
                    <span className="text-white font-semibold">${pattern.target}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4 bg-gray-800 rounded-lg text-center">
            <p className="text-gray-400">No patterns detected at the moment</p>
          </div>
        )}
      </div>

      {/* Divergências */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          Divergences (RSI vs Price)
        </h3>
        
        {divergences.divergences && divergences.divergences.length > 0 ? (
          <div className="space-y-3">
            {divergences.divergences.slice(0, 5).map((div: any, idx: number) => (
              <div 
                key={idx}
                className={`p-4 rounded-lg border ${
                  div.type === "Bullish"
                    ? "bg-green-900/20 border-green-800/30"
                    : "bg-red-900/20 border-red-800/30"
                }`}
              >
                <div className="flex justify-between items-center mb-2">
                  <span className="font-bold text-white">{div.type} Divergence</span>
                  <span className="text-sm text-gray-400">{div.date}</span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">Preço: </span>
                    <span className="text-white">${div.price}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">RSI: </span>
                    <span className="text-white">{div.rsi}</span>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500">
                  Strength: {div.strength.toFixed(1)}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4 bg-gray-800 rounded-lg text-center">
            <p className="text-gray-400">No recent divergences</p>
          </div>
        )}
      </div>

      {/* Gaps */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 lg:col-span-2">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Gap Analysis
        </h3>
        
        {gaps.all_gaps && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded-lg text-center">
                <div className="text-3xl font-bold text-white">{gaps.total_gaps}</div>
                <div className="text-sm text-gray-400">Total Gaps</div>
              </div>
              <div className="bg-red-900/20 p-4 rounded-lg border border-red-800/30 text-center">
                <div className="text-3xl font-bold text-red-500">{gaps.unfilled_count}</div>
                <div className="text-sm text-gray-400">Unfilled</div>
              </div>
              <div className="bg-green-900/20 p-4 rounded-lg border border-green-800/30 text-center">
                <div className="text-3xl font-bold text-green-500">{gaps.fill_rate}%</div>
                <div className="text-sm text-gray-400">Fill Rate</div>
              </div>
            </div>

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {gaps.unfilled_gaps?.slice(0, 10).map((gap: any, idx: number) => (
                <div key={idx} className="flex items-center justify-between p-4 bg-gray-800 rounded-lg">
                  <div>
                    <div className={`font-bold ${
                      gap.type === "Gap Up" ? "text-green-500" : "text-red-500"
                    }`}>
                      {gap.type}
                    </div>
                    <div className="text-sm text-gray-400">{gap.date}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-white font-semibold">
                      {gap.gap_percent > 0 ? "+" : ""}{gap.gap_percent}%
                    </div>
                    <div className="text-xs text-gray-500">
                      ${gap.prev_close} → ${gap.open}
                    </div>
                  </div>
                  <div className="px-3 py-1 bg-red-900/30 text-red-400 rounded-full text-xs">
                    Unfilled
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ===== STATISTICS TAB =====
function StatisticsTab({ data }: { data: any }) {
  const stats = data.statistical || {};
  const seasonality = data.seasonality || {};
  const anomalies = data.anomalies || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Statistical Dashboard */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <PieChart className="w-5 h-5" />
          Dashboard Estatístico
        </h3>
        
        {stats.mean_return !== undefined && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Retorno Médio</div>
                <div className={`text-xl font-bold ${
                  stats.mean_return > 0 ? "text-green-500" : "text-red-500"
                }`}>
                  {stats.mean_return}%
                </div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Mediana</div>
                <div className="text-xl font-bold text-white">{stats.median_return}%</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Desvio Padrão</div>
                <div className="text-xl font-bold text-white">{stats.std_deviation}%</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Win Rate</div>
                <div className="text-xl font-bold text-green-500">{stats.win_rate}%</div>
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-400">Positive Days</div>
                  <div className="text-lg font-bold text-green-500">{stats.positive_days}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Negative Days</div>
                  <div className="text-lg font-bold text-red-500">{stats.negative_days}</div>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="bg-green-900/20 p-3 rounded-lg border border-green-800/30">
                <div className="text-sm text-gray-400">Máximo Retorno</div>
                <div className="text-xl font-bold text-green-500">+{stats.max_return}%</div>
              </div>
              <div className="bg-red-900/20 p-3 rounded-lg border border-red-800/30">
                <div className="text-sm text-gray-400">Mínimo Retorno</div>
                <div className="text-xl font-bold text-red-500">{stats.min_return}%</div>
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Value at Risk (VaR)</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-xs text-gray-500">95%</div>
                  <div className="text-lg font-bold text-red-400">{stats.var_95}%</div>
                </div>
                <div>
                  <div className="text-xs text-gray-500">99%</div>
                  <div className="text-lg font-bold text-red-500">{stats.var_99}%</div>
                </div>
              </div>
            </div>

            {stats.interpretation && (
              <div className="p-4 bg-blue-900/20 border border-blue-800/30 rounded-lg">
                <div className="text-sm text-gray-300">
                  <div>📊 {stats.interpretation.skewness}</div>
                  <div className="mt-1">📈 {stats.interpretation.kurtosis}</div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Seasonality */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Calendar className="w-5 h-5" />
          Análise de Sazonalidade
        </h3>
        
        {seasonality.monthly && (
          <div className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-sm text-gray-400">Best Month</div>
                  <div className="text-lg font-bold text-green-500">{seasonality.best_month}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Worst Month</div>
                  <div className="text-lg font-bold text-red-500">{seasonality.worst_month}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Best Day</div>
                  <div className="text-lg font-bold text-green-500">{seasonality.best_day}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Worst Day</div>
                  <div className="text-lg font-bold text-red-500">{seasonality.worst_day}</div>
                </div>
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-400 mb-2">Monthly Performance</div>
              <div className="space-y-1 max-h-64 overflow-y-auto">
                {seasonality.monthly.map((month: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-2 bg-gray-800 rounded">
                    <span className="text-sm text-gray-300">{month.month}</span>
                    <span className={`text-sm font-semibold ${
                      month.avg_return > 0 ? "text-green-500" : "text-red-500"
                    }`}>
                      {month.avg_return > 0 ? "+" : ""}{month.avg_return}%
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-400 mb-2">Performance by Day of Week</div>
              <div className="space-y-1">
                {seasonality.weekday?.map((day: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-2 bg-gray-800 rounded">
                    <span className="text-sm text-gray-300">{day.day}</span>
                    <span className={`text-sm font-semibold ${
                      day.avg_return > 0 ? "text-green-500" : "text-red-500"
                    }`}>
                      {day.avg_return > 0 ? "+" : ""}{day.avg_return}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Anomalias */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 lg:col-span-2">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5" />
          Anomaly Detection
        </h3>
        
        {anomalies.anomalies && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded-lg text-center">
                <div className="text-3xl font-bold text-white">{anomalies.total}</div>
                <div className="text-sm text-gray-400">Total Anomalies</div>
              </div>
              <div className="bg-yellow-900/20 p-4 rounded-lg border border-yellow-800/30 text-center">
                <div className="text-3xl font-bold text-yellow-500">{anomalies.recent_count}</div>
                <div className="text-sm text-gray-400">Last 30 days</div>
              </div>
            </div>

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {anomalies.anomalies.slice(0, 15).map((anomaly: any, idx: number) => (
                <div key={idx} className="p-4 bg-gray-800 rounded-lg border border-yellow-800/30">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <div className="text-white font-semibold">{anomaly.date}</div>
                      <div className="text-sm text-gray-400">${anomaly.price}</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-lg font-bold ${
                        anomaly.change > 0 ? "text-green-500" : "text-red-500"
                      }`}>
                        {anomaly.change > 0 ? "+" : ""}{anomaly.change}%
                      </span>
                      <span className="px-2 py-1 bg-yellow-900/30 text-yellow-500 rounded text-xs">
                        Score: {anomaly.score}
                      </span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    {anomaly.reasons.map((reason: string, rIdx: number) => (
                      <div key={rIdx} className="text-xs text-gray-400 flex items-center gap-1">
                        <span className="text-yellow-500">•</span>
                        {reason}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ===== RISK TAB =====
function RiskTab({ data }: { data: any }) {
  const volatility = data.volatility || {};
  const support = data.support || {};
  const relativeStrength = data.relativeStrength || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Volatility Analysis */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          Volatility Analysis
        </h3>
        
        {volatility.current_volatility !== undefined && (
          <div className="space-y-4">
            <div className="text-center p-6 bg-gradient-to-r from-purple-900/20 to-pink-900/20 rounded-lg border border-purple-800/30">
              <div className="text-4xl font-bold text-white mb-2">
                {volatility.current_volatility}%
              </div>
              <div className="text-xl font-semibold text-purple-400">
                {volatility.classification}
              </div>
              <div className="text-sm text-gray-400 mt-2">
                {volatility.signal}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Vol. Histórica</div>
                <div className="text-xl font-bold text-white">{volatility.historical_avg}%</div>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Percentil</div>
                <div className="text-xl font-bold text-white">{volatility.volatility_percentile}%</div>
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">ATR (Average True Range)</div>
              <div className="text-2xl font-bold text-white mb-1">${volatility.atr}</div>
              <div className="text-sm text-gray-500">{volatility.atr_percent}% do preço</div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Bollinger Band Width</div>
              <div className="flex justify-between items-center mb-1">
                <span className="text-white">Current: {volatility.bb_width_current}%</span>
                <span className="text-gray-500">Average: {volatility.bb_width_avg}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-purple-500 h-full rounded-full"
                  style={{ width: `${Math.min(100, (volatility.bb_width_current / volatility.bb_width_avg) * 100)}%` }}
                ></div>
              </div>
            </div>

            {volatility.squeeze_detected && (
              <div className="p-3 bg-yellow-900/20 border border-yellow-800/30 rounded-lg">
                <p className="text-yellow-500 text-sm flex items-center gap-2">
                  <Zap className="w-4 h-4" />
                  Squeeze detectado - movimento forte esperado!
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Support & Resistance Advanced */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Shield className="w-5 h-5" />
          Advanced Support Suporte & Resistência Avançado Resistance
        </h3>
        
        {support.current_price && (
          <div className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg text-center">
              <div className="text-sm text-gray-400 mb-1">Current Price</div>
              <div className="text-3xl font-bold text-white">${support.current_price}</div>
            </div>

            <div>
              <div className="text-sm text-gray-400 mb-2 flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-green-500" />
                Supports (strength)
              </div>
              <div className="space-y-2">
                {support.supports?.slice(0, 5).map((sup: any, idx: number) => (
                  <div key={idx} className="bg-green-900/20 p-3 rounded-lg border border-green-800/30">
                    <div className="flex justify-between items-center">
                      <span className="text-white font-semibold">${sup.price.toFixed(2)}</span>
                      <div className="text-right">
                        <div className="text-sm text-gray-400">{sup.touches} touches</div>
                        <div className="text-xs text-green-500">{sup.distance_percent}% away</div>
                      </div>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                      <div 
                        className="bg-green-500 h-full rounded-full"
                        style={{ width: `${sup.strength}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="text-sm text-gray-400 mb-2 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-red-500" />
                Resistances (strength)
              </div>
              <div className="space-y-2">
                {support.resistances?.slice(0, 5).map((res: any, idx: number) => (
                  <div key={idx} className="bg-red-900/20 p-3 rounded-lg border border-red-800/30">
                    <div className="flex justify-between items-center">
                      <span className="text-white font-semibold">${res.price.toFixed(2)}</span>
                      <div className="text-right">
                        <div className="text-sm text-gray-400">{res.touches} touches</div>
                        <div className="text-xs text-red-500">+{res.distance_percent}% away</div>
                      </div>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                      <div 
                        className="bg-red-500 h-full rounded-full"
                        style={{ width: `${res.strength}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {support.psychological_levels && support.psychological_levels.length > 0 && (
              <div className="p-3 bg-blue-900/20 border border-blue-800/30 rounded-lg">
                <div className="text-sm text-gray-400 mb-2">Níveis Psicológicos</div>
                <div className="flex flex-wrap gap-2">
                  {support.psychological_levels.map((level: number, idx: number) => (
                    <span key={idx} className="px-3 py-1 bg-blue-900/30 text-blue-400 rounded-full text-sm">
                      ${level}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Relative Strength vs BTC */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 lg:col-span-2">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <BarChart3 className="w-5 h-5" />
          Relative Strength vs Bitcoin
        </h3>
        
        {relativeStrength.rs_current && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-gray-800 p-4 rounded-lg text-center">
                <div className="text-sm text-gray-400 mb-1">Current RS</div>
                <div className="text-2xl font-bold text-white">{relativeStrength.rs_current}</div>
              </div>
              <div className={`p-4 rounded-lg text-center ${
                relativeStrength.rs_change_1m > 0 
                  ? "bg-green-900/20 border border-green-800/30" 
                  : "bg-red-900/20 border border-red-800/30"
              }`}>
                <div className="text-sm text-gray-400 mb-1">1M Change</div>
                <div className={`text-2xl font-bold ${
                  relativeStrength.rs_change_1m > 0 ? "text-green-500" : "text-red-500"
                }`}>
                  {relativeStrength.rs_change_1m > 0 ? "+" : ""}{relativeStrength.rs_change_1m}%
                </div>
              </div>
              <div className={`p-4 rounded-lg text-center ${
                relativeStrength.rs_change_3m > 0 
                  ? "bg-green-900/20 border border-green-800/30" 
                  : "bg-red-900/20 border border-red-800/30"
              }`}>
                <div className="text-sm text-gray-400 mb-1">3M Change</div>
                <div className={`text-2xl font-bold ${
                  relativeStrength.rs_change_3m > 0 ? "text-green-500" : "text-red-500"
                }`}>
                  {relativeStrength.rs_change_3m > 0 ? "+" : ""}{relativeStrength.rs_change_3m}%
                </div>
              </div>
              <div className={`p-4 rounded-lg text-center ${
                relativeStrength.is_outperforming 
                  ? "bg-green-900/20 border border-green-800/30" 
                  : "bg-red-900/20 border border-red-800/30"
              }`}>
                <div className="text-sm text-gray-400 mb-1">vs BTC</div>
                <div className={`text-2xl font-bold ${
                  relativeStrength.is_outperforming ? "text-green-500" : "text-red-500"
                }`}>
                  {relativeStrength.is_outperforming ? "Outperforming" : "Underperforming"}
                </div>
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Strength: {relativeStrength.strength}</div>
              <div className="text-lg text-white">
                Performance vs BTC: 
                <span className={`ml-2 font-bold ${
                  relativeStrength.outperformance > 0 ? "text-green-500" : "text-red-500"
                }`}>
                  {relativeStrength.outperformance > 0 ? "+" : ""}{relativeStrength.outperformance}%
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ===== TOOLS TAB =====
function ToolsTab({ data, ticker }: { data: any; ticker: string }) {
  const dcaSimulator = data.dcaSimulator || {};
  const fibonacciTime = data.fibonacciTime || {};

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* DCA Simulator */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <DollarSign className="w-5 h-5" />
          Simulador DCA (Dollar-Cost Averaging)
        </h3>
        
        {dcaSimulator.total_invested && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 p-4 rounded-lg">
                <div className="text-sm text-gray-400">Invested</div>
                <div className="text-xl font-bold text-white">${dcaSimulator.total_invested}</div>
              </div>
              <div className={`p-4 rounded-lg ${
                dcaSimulator.profit >= 0 
                  ? "bg-green-900/20 border border-green-800/30" 
                  : "bg-red-900/20 border border-red-800/30"
              }`}>
                <div className="text-sm text-gray-400">Current Value</div>
                <div className={`text-xl font-bold ${
                  dcaSimulator.profit >= 0 ? "text-green-500" : "text-red-500"
                }`}>
                  ${dcaSimulator.current_value}
                </div>
              </div>
            </div>

            <div className="text-center p-6 bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-lg border border-blue-800/30">
              <div className={`text-4xl font-bold mb-2 ${
                dcaSimulator.return_percent >= 0 ? "text-green-500" : "text-red-500"
              }`}>
                {dcaSimulator.return_percent >= 0 ? "+" : ""}{dcaSimulator.return_percent}%
              </div>
              <div className="text-lg text-white">
                Profit: ${dcaSimulator.profit}
              </div>
            </div>

            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-400">Average Price</div>
                  <div className="text-lg font-bold text-white">${dcaSimulator.avg_price}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400">Total Units</div>
                  <div className="text-lg font-bold text-white">{dcaSimulator.total_units}</div>
                </div>
              </div>
            </div>

            {dcaSimulator.lump_sum_comparison && (
              <div className="p-4 bg-blue-900/20 border border-blue-800/30 rounded-lg">
                <div className="text-sm text-gray-400 mb-2">vs Lump Sum</div>
                <div className="flex justify-between items-center">
                  <span className="text-white">
                    Lump Sum: {dcaSimulator.lump_sum_comparison.lump_sum_return}%
                  </span>
                  <span className={`font-bold ${
                    dcaSimulator.lump_sum_comparison.difference >= 0 ? "text-green-500" : "text-red-500"
                  }`}>
                    {dcaSimulator.lump_sum_comparison.difference >= 0 ? "+" : ""}
                    {dcaSimulator.lump_sum_comparison.difference}%
                  </span>
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  Better Strategy: {dcaSimulator.lump_sum_comparison.better_strategy}
                </div>
              </div>
            )}

            <div className="max-h-48 overflow-y-auto space-y-2">
              {dcaSimulator.investments?.map((inv: any, idx: number) => (
                <div key={idx} className="flex justify-between items-center p-2 bg-gray-800 rounded text-sm">
                  <span className="text-gray-400">{inv.date}</span>
                  <span className="text-white">${inv.price}</span>
                  <span className="text-gray-500">{inv.units_bought} units</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Fibonacci Time Zones */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Clock3 className="w-5 h-5" />
          Fibonacci Time Zones
        </h3>
        
        {fibonacciTime.swing_low_date && (
          <div className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <div className="text-sm text-gray-400 mb-2">Reference Swing Low</div>
              <div className="flex justify-between items-center">
                <span className="text-white">{fibonacciTime.swing_low_date}</span>
                <span className="text-lg font-bold text-white">${fibonacciTime.swing_low_price}</span>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {fibonacciTime.days_since_low} days atrás
              </div>
            </div>

            {fibonacciTime.next_important_date && (
              <div className="p-4 bg-yellow-900/20 border border-yellow-800/30 rounded-lg">
                <div className="text-sm text-gray-400 mb-1">Next Important Date</div>
                <div className="text-xl font-bold text-yellow-500">
                  {fibonacciTime.next_important_date}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Possível ponto de virada
                </div>
              </div>
            )}

            <div className="space-y-2 max-h-64 overflow-y-auto">
              {fibonacciTime.time_zones?.map((zone: any, idx: number) => (
                <div 
                  key={idx}
                  className={`p-3 rounded-lg ${
                    zone.status === "FUTURE" 
                      ? "bg-blue-900/20 border border-blue-800/30" 
                      : "bg-gray-800"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="text-white font-semibold">{zone.fib_days} days</div>
                      <div className="text-xs text-gray-400">{zone.target_date}</div>
                    </div>
                    {zone.status === "PAST" ? (
                      <div>
                        <div className="text-white">${zone.actual_price}</div>
                        {zone.significant_move && (
                          <div className="text-xs text-green-500">Significant move</div>
                        )}
                      </div>
                    ) : (
                      <div>
                        <span className="px-2 py-1 bg-blue-900/30 text-blue-400 rounded text-xs">
                          In {zone.days_ahead} days
                        </span>
                      </div>
                    )}
                  </div>
                  {zone.note && (
                    <div className="text-xs text-gray-500 mt-1">{zone.note}</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

