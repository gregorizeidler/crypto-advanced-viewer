"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Zap, TrendingUp, TrendingDown, Activity } from "lucide-react";

interface FastMover {
  ticker: string;
  price: number;
  change_24h: number;
  volume_ratio: number;
  momentum_5d: number;
  alert_level: string;
}

export default function FastMoversWidget() {
  const [movers, setMovers] = useState<FastMover[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFastMovers();
    // Atualiza a cada 5 minutos
    const interval = setInterval(loadFastMovers, 300000);
    return () => clearInterval(interval);
  }, []);

  const loadFastMovers = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/crypto/advanced/fast-movers");
      const data = await res.json();
      setMovers(data.movers || []);
    } catch (error) {
      console.error("Error loading fast movers:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="w-5 h-5 text-yellow-500" />
          <h3 className="text-xl font-bold text-white">🔥 Fast Movers</h3>
        </div>
        <div className="flex justify-center items-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-yellow-500" />
          <h3 className="text-xl font-bold text-white">🔥 Fast Movers</h3>
        </div>
        <span className="text-sm text-gray-400">Last 24h</span>
      </div>

      {movers.length === 0 ? (
        <div className="text-center py-8 text-gray-400">
          No significant movement at the moment
        </div>
      ) : (
        <div className="space-y-3">
          {movers.map((mover, idx) => {
            const isUp = mover.change_24h > 0;
            
            return (
              <motion.div
                key={mover.ticker}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`p-4 rounded-lg border ${
                  mover.alert_level === "HIGH"
                    ? isUp
                      ? "bg-green-900/20 border-green-800/30"
                      : "bg-red-900/20 border-red-800/30"
                    : "bg-gray-800 border-gray-700"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white text-lg">
                      {mover.ticker.replace("-USD", "")}
                    </span>
                    {mover.alert_level === "HIGH" && (
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        isUp ? "bg-green-600" : "bg-red-600"
                      }`}>
                        HIGH
                      </span>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-white">
                      ${mover.price.toFixed(2)}
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1">
                      {isUp ? (
                        <TrendingUp className="w-4 h-4 text-green-500" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-red-500" />
                      )}
                      <span className={`font-semibold ${
                        isUp ? "text-green-500" : "text-red-500"
                      }`}>
                        {isUp ? "+" : ""}{mover.change_24h.toFixed(2)}%
                      </span>
                    </div>
                    <div className="flex items-center gap-1 text-gray-400">
                      <Activity className="w-4 h-4" />
                      <span>{mover.volume_ratio.toFixed(1)}x vol</span>
                    </div>
                  </div>
                  <div className="text-gray-500 text-xs">
                    5d: {mover.momentum_5d > 0 ? "+" : ""}{mover.momentum_5d.toFixed(1)}%
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      <button
        onClick={loadFastMovers}
        className="w-full mt-4 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm text-gray-300 transition-colors"
      >
        🔄 Refresh
      </button>
    </div>
  );
}

