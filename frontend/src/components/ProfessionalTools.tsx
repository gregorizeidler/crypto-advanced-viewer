"use client";

import { useState, useEffect } from 'react';
import { Activity, TrendingUp, Target, DollarSign, BarChart3, Calendar, AlertTriangle, Zap, Layers, Shield } from 'lucide-react';

interface ProfessionalToolsProps {
  ticker: string;
}

export default function ProfessionalTools({ ticker }: ProfessionalToolsProps) {
  const [activeTab, setActiveTab] = useState('technical');
  const [loading, setLoading] = useState(true);
  
  // Data states for each tool
  const [ichimoku, setIchimoku] = useState<any>(null);
  const [elliottWave, setElliottWave] = useState<any>(null);
  const [wyckoff, setWyckoff] = useState<any>(null);
  const [trendAlignment, setTrendAlignment] = useState<any>(null);
  const [candlestickPatterns, setCandlestickPatterns] = useState<any>(null);
  const [supportResistance, setSupportResistance] = useState<any>(null);
  const [monteCarlo, setMonteCarlo] = useState<any>(null);
  const [calendar, setCalendar] = useState<any>(null);
  const [drawdown, setDrawdown] = useState<any>(null);
  const [winRate, setWinRate] = useState<any>(null);
  const [confluence, setConfluence] = useState<any>(null);
  const [reversalProb, setReversalProb] = useState<any>(null);
  const [acceleration, setAcceleration] = useState<any>(null);
  const [volumeMomentum, setVolumeMomentum] = useState<any>(null);
  const [velocity, setVelocity] = useState<any>(null);
  const [positionSizing, setPositionSizing] = useState<any>(null);
  const [riskReward, setRiskReward] = useState<any>(null);
  const [technicalSetups, setTechnicalSetups] = useState<any>(null);

  const tabs = [
    { id: 'technical', name: 'Technical Analysis', icon: Activity },
    { id: 'patterns', name: 'Patterns & Setups', icon: Target },
    { id: 'statistics', name: 'Statistics & Probability', icon: BarChart3 },
    { id: 'momentum', name: 'Momentum & Velocity', icon: Zap },
    { id: 'risk', name: 'Risk Management', icon: Shield }
  ];

  useEffect(() => {
    if (!ticker) return;
    fetchAllData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ticker]);

  const fetchAllData = async () => {
    console.log('Fetching data for:', ticker);
    setLoading(true);
    const baseUrl = 'http://localhost:8000/api/professional';

    try {
      // Fetch all tools in parallel
      console.log('Starting parallel fetch...');
      const [
        ichimokuRes,
        elliottRes,
        wyckoffRes,
        trendRes,
        patternsRes,
        srRes,
        monteCarloRes,
        calendarRes,
        drawdownRes,
        winRateRes,
        confluenceRes,
        reversalRes,
        accelRes,
        volMomRes,
        velocityRes,
        positionRes,
        rrRes,
        setupsRes
      ] = await Promise.all([
        fetch(`${baseUrl}/ichimoku/${ticker}`),
        fetch(`${baseUrl}/elliott-wave/${ticker}`),
        fetch(`${baseUrl}/wyckoff/${ticker}`),
        fetch(`${baseUrl}/trend-alignment/${ticker}`),
        fetch(`${baseUrl}/candlestick-patterns/${ticker}`),
        fetch(`${baseUrl}/support-resistance/${ticker}`),
        fetch(`${baseUrl}/monte-carlo/${ticker}?days=30`),
        fetch(`${baseUrl}/calendar/${ticker}?period=2y`),
        fetch(`${baseUrl}/drawdown/${ticker}?period=1y`),
        fetch(`${baseUrl}/win-rate/${ticker}?period=1y`),
        fetch(`${baseUrl}/confluence/${ticker}`),
        fetch(`${baseUrl}/reversal-probability/${ticker}`),
        fetch(`${baseUrl}/acceleration/${ticker}`),
        fetch(`${baseUrl}/volume-momentum/${ticker}`),
        fetch(`${baseUrl}/velocity/${ticker}`),
        fetch(`${baseUrl}/position-sizing/${ticker}?account_size=10000&risk_pct=2&stop_loss_pct=5`),
        fetch(`${baseUrl}/risk-reward/${ticker}`),
        fetch(`${baseUrl}/technical-setups/${ticker}`)
      ]);

      console.log('Responses received, parsing JSON...');
      
      const ichimokuData = await ichimokuRes.json();
      console.log('✅ Ichimoku data:', ichimokuData);
      console.log('  - tenkan_sen:', ichimokuData.tenkan_sen);
      console.log('  - current_price:', ichimokuData.current_price);
      setIchimoku(ichimokuData);
      
      const srData = await srRes.json();
      console.log('✅ Support/Resistance:', srData);
      console.log('  - current_price:', srData.current_price);
      setSupportResistance(srData);
      
      const volMomData = await volMomRes.json();
      console.log('✅ Volume Momentum:', volMomData);
      console.log('  - volume_ratio:', volMomData.volume_ratio);
      console.log('  - current_volume:', volMomData.current_volume);
      setVolumeMomentum(volMomData);
      
      const velocityData = await velocityRes.json();
      console.log('✅ Velocity:', velocityData);
      console.log('  - return_24h:', velocityData.return_24h);
      setVelocity(velocityData);
      
      const positionData = await positionRes.json();
      console.log('✅ Position Sizing:', positionData);
      console.log('  - account_size:', positionData.account_size);
      console.log('  - entry_price:', positionData.entry_price);
      setPositionSizing(positionData);
      
      const accelData = await accelRes.json();
      console.log('✅ Acceleration:', accelData);
      console.log('  - velocity:', accelData.velocity);
      setAcceleration(accelData);
      
      setElliottWave(await elliottRes.json());
      setWyckoff(await wyckoffRes.json());
      setTrendAlignment(await trendRes.json());
      setCandlestickPatterns(await patternsRes.json());
      setMonteCarlo(await monteCarloRes.json());
      setCalendar(await calendarRes.json());
      setDrawdown(await drawdownRes.json());
      setWinRate(await winRateRes.json());
      setConfluence(await confluenceRes.json());
      setReversalProb(await reversalRes.json());
      setRiskReward(await rrRes.json());
      setTechnicalSetups(await setupsRes.json());

      console.log('All data loaded successfully!');
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p className="text-gray-400">Loading Professional Tools...</p>
              <p className="text-gray-500 text-sm mt-2">Check browser console (F12) for logs</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Debug: Check if we have any data
  console.log('🔍 RENDER CHECK:');
  console.log('  - ichimoku:', ichimoku ? 'LOADED' : 'NULL');
  console.log('  - ichimoku.tenkan_sen:', ichimoku?.tenkan_sen);
  console.log('  - ichimoku.current_price:', ichimoku?.current_price);
  console.log('  - supportResistance:', supportResistance ? 'LOADED' : 'NULL');
  console.log('  - supportResistance.current_price:', supportResistance?.current_price);
  console.log('  - volumeMomentum:', volumeMomentum ? 'LOADED' : 'NULL');
  console.log('  - volumeMomentum.volume_ratio:', volumeMomentum?.volume_ratio);
  console.log('  - acceleration:', acceleration ? 'LOADED' : 'NULL');
  console.log('  - acceleration.velocity:', acceleration?.velocity);
  console.log('Active tab:', activeTab);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
            <Layers className="w-10 h-10 text-blue-500" />
            Professional Trading Tools
          </h1>
          <p className="text-gray-400">
            Advanced analysis suite for {ticker} - 18 professional-grade tools
          </p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-2 mb-6 overflow-x-auto pb-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                <Icon className="w-5 h-5" />
                {tab.name}
              </button>
            );
          })}
        </div>

        {/* Content */}
        <div className="space-y-6">
          {/* Debug Info */}
          {!loading && !ichimoku && (
            <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6">
              <h3 className="text-xl font-bold text-red-400 mb-2">⚠️ No Data Loaded</h3>
              <p className="text-gray-300 mb-2">Data fetch may have failed. Check browser console (F12) for errors.</p>
              <p className="text-gray-400 text-sm">Backend: http://localhost:8000</p>
            </div>
          )}
          
          {/* TECHNICAL ANALYSIS TAB */}
          {activeTab === 'technical' && (
            <>
              {/* Ichimoku Cloud */}
              {ichimoku && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <TrendingUp className="w-6 h-6 text-blue-500" />
                    Ichimoku Cloud System
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Signal</p>
                      <p className={`text-2xl font-bold ${
                        ichimoku.signal?.includes('BUY') ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {ichimoku.signal}
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Strength</p>
                      <p className="text-2xl font-bold text-white">{ichimoku.strength}/3</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Cloud Status</p>
                      <p className={`text-xl font-bold ${ichimoku.cloud_bullish ? 'text-green-400' : 'text-red-400'}`}>
                        {ichimoku.cloud_bullish ? 'Bullish ☁️' : 'Bearish ☁️'}
                      </p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div>
                      <p className="text-gray-400">Tenkan-sen</p>
                      <p className="text-white font-semibold">${ichimoku.tenkan_sen?.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-400">Kijun-sen</p>
                      <p className="text-white font-semibold">${ichimoku.kijun_sen?.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-400">TK Cross</p>
                      <p className={ichimoku.tk_cross_bullish ? 'text-green-400' : 'text-red-400'}>
                        {ichimoku.tk_cross_bullish ? 'Bullish ✓' : 'Bearish ✗'}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-400">Price vs Cloud</p>
                      <p className={ichimoku.price_above_cloud ? 'text-green-400' : 'text-red-400'}>
                        {ichimoku.price_above_cloud ? 'Above ↑' : 'Below ↓'}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Trend Alignment */}
              {trendAlignment && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">📊 Trend Alignment Scanner</h2>
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-gray-400">Alignment Score</span>
                      <span className="text-2xl font-bold text-blue-400">{trendAlignment.score}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full transition-all ${
                          trendAlignment.score >= 80 ? 'bg-green-500' :
                          trendAlignment.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${trendAlignment.score}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {trendAlignment.checks?.map((check: any, idx: number) => (
                      <div key={idx} className="flex items-center justify-between bg-gray-900/50 p-3 rounded-lg">
                        <span className="text-gray-300">{check.name}</span>
                        <span className={`font-bold ${check.passed ? 'text-green-400' : 'text-red-400'}`}>
                          {check.passed ? '✓' : '✗'}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                    <p className="text-lg font-bold text-blue-400">Signal: {trendAlignment.signal}</p>
                  </div>
                </div>
              )}

              {/* Wyckoff Analysis */}
              {wyckoff && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🎭 Wyckoff Method Analysis</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm mb-1">Current Phase</p>
                      <p className="text-xl font-bold text-white">{wyckoff.phase}</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm mb-1">Signal</p>
                      <p className={`text-xl font-bold ${
                        wyckoff.signal === 'BULLISH' ? 'text-green-400' :
                        wyckoff.signal === 'BEARISH' ? 'text-red-400' : 'text-yellow-400'
                      }`}>
                        {wyckoff.signal}
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm mb-1">Spring Detected</p>
                      <p className={`text-xl font-bold ${wyckoff.spring_detected ? 'text-green-400' : 'text-gray-400'}`}>
                        {wyckoff.spring_detected ? 'YES 🚀' : 'NO'}
                      </p>
                    </div>
                  </div>
                  <div className="mt-4 grid grid-cols-2 gap-4">
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Volume Ratio</p>
                      <p className="text-lg font-bold text-white">{wyckoff.volume_ratio}x</p>
                    </div>
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Effort vs Result</p>
                      <p className="text-lg font-bold text-white">{wyckoff.effort_vs_result}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Support/Resistance Zones */}
              {supportResistance && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🎯 Support & Resistance Zones</h2>
                  <div className="mb-4 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                    <p className="text-sm text-gray-400 mb-1">Current Price</p>
                    <p className="text-2xl font-bold text-white">${supportResistance.current_price?.toLocaleString()}</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {supportResistance.nearest_support && (
                      <div className="bg-green-900/20 p-4 rounded-lg border border-green-500/30">
                        <p className="text-sm text-gray-400 mb-1">Nearest Support</p>
                        <p className="text-xl font-bold text-green-400">${supportResistance.nearest_support.price?.toLocaleString()}</p>
                        <p className="text-sm text-gray-400 mt-2">Distance: {supportResistance.nearest_support.distance_pct}%</p>
                        <p className="text-sm text-gray-400">Strength: {supportResistance.nearest_support.strength}/100</p>
                      </div>
                    )}
                    {supportResistance.nearest_resistance && (
                      <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
                        <p className="text-sm text-gray-400 mb-1">Nearest Resistance</p>
                        <p className="text-xl font-bold text-red-400">${supportResistance.nearest_resistance.price?.toLocaleString()}</p>
                        <p className="text-sm text-gray-400 mt-2">Distance: {supportResistance.nearest_resistance.distance_pct}%</p>
                        <p className="text-sm text-gray-400">Strength: {supportResistance.nearest_resistance.strength}/100</p>
                      </div>
                    )}
                  </div>
                  <div className="space-y-2">
                    <p className="text-gray-400 font-semibold mb-2">All Zones (sorted by proximity)</p>
                    {supportResistance.zones?.slice(0, 5).map((zone: any, idx: number) => (
                      <div key={idx} className={`p-3 rounded-lg ${
                        zone.type === 'SUPPORT' ? 'bg-green-900/10 border border-green-500/20' : 'bg-red-900/10 border border-red-500/20'
                      }`}>
                        <div className="flex justify-between items-center">
                          <div>
                            <span className={`font-bold ${zone.type === 'SUPPORT' ? 'text-green-400' : 'text-red-400'}`}>
                              {zone.type}
                            </span>
                            <span className="text-white ml-2">${zone.price?.toLocaleString()}</span>
                          </div>
                          <div className="text-right">
                            <p className="text-gray-400 text-sm">{zone.distance_pct}% away</p>
                            <p className="text-gray-500 text-xs">Touches: {zone.touches}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* PATTERNS & SETUPS TAB */}
          {activeTab === 'patterns' && (
            <>
              {/* Candlestick Patterns */}
              {candlestickPatterns && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <Target className="w-6 h-6 text-blue-500" />
                    Candlestick Pattern Library
                  </h2>
                  {candlestickPatterns.count > 0 ? (
                    <>
                      <div className="mb-4 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                        <p className="text-sm text-gray-400 mb-1">Patterns Detected</p>
                        <p className="text-3xl font-bold text-blue-400">{candlestickPatterns.count}</p>
                      </div>
                      <div className="space-y-3">
                        {candlestickPatterns.patterns?.map((pattern: any, idx: number) => (
                          <div key={idx} className={`p-4 rounded-lg border ${
                            pattern.type === 'BULLISH' ? 'bg-green-900/20 border-green-500/30' :
                            pattern.type === 'BEARISH' ? 'bg-red-900/20 border-red-500/30' :
                            'bg-yellow-900/20 border-yellow-500/30'
                          }`}>
                            <div className="flex justify-between items-start mb-2">
                              <div>
                                <h3 className="text-xl font-bold text-white">{pattern.name}</h3>
                                <p className={`text-sm font-semibold ${
                                  pattern.type === 'BULLISH' ? 'text-green-400' :
                                  pattern.type === 'BEARISH' ? 'text-red-400' : 'text-yellow-400'
                                }`}>
                                  {pattern.type}
                                </p>
                              </div>
                              <div className="text-right">
                                <p className="text-sm text-gray-400">Confidence</p>
                                <p className="text-2xl font-bold text-blue-400">{pattern.confidence}%</p>
                              </div>
                            </div>
                            <p className="text-gray-300">{pattern.description}</p>
                          </div>
                        ))}
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <p className="text-lg">No significant candlestick patterns detected</p>
                      <p className="text-sm mt-2">Patterns appear during specific market conditions</p>
                    </div>
                  )}
                </div>
              )}

              {/* Elliott Wave */}
              {elliottWave && elliottWave.waves_detected > 0 && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🌊 Elliott Wave Counter</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Waves Detected</p>
                      <p className="text-2xl font-bold text-white">{elliottWave.waves_detected}</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Current Wave</p>
                      <p className="text-2xl font-bold text-blue-400">{elliottWave.current_wave}</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {elliottWave.swings?.map((swing: any, idx: number) => (
                      <div key={idx} className="flex justify-between items-center bg-gray-900/50 p-3 rounded-lg">
                        <span className="text-gray-300">Wave {idx + 1} ({swing.type})</span>
                        <span className="font-bold text-white">${swing.price?.toLocaleString()}</span>
                        <span className="text-gray-400 text-sm">{swing.date}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 p-4 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                    <p className="text-blue-400">{elliottWave.analysis}</p>
                  </div>
                </div>
              )}

              {/* Technical Setups */}
              {technicalSetups && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🔍 Technical Setup Finder</h2>
                  {technicalSetups.count > 0 ? (
                    <div className="space-y-3">
                      {technicalSetups.setups?.map((setup: any, idx: number) => (
                        <div key={idx} className={`p-4 rounded-lg border ${
                          setup.type === 'BULLISH' ? 'bg-green-900/20 border-green-500/30' :
                          setup.type === 'BEARISH' ? 'bg-red-900/20 border-red-500/30' :
                          'bg-yellow-900/20 border-yellow-500/30'
                        }`}>
                          <div className="flex justify-between items-center">
                            <h3 className="text-lg font-bold text-white">{setup.name}</h3>
                            <div className="text-right">
                              <p className={`font-bold ${
                                setup.type === 'BULLISH' ? 'text-green-400' :
                                setup.type === 'BEARISH' ? 'text-red-400' : 'text-yellow-400'
                              }`}>
                                {setup.type}
                              </p>
                              <p className="text-sm text-gray-400">{setup.confidence}% confidence</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <p>No technical setups detected at the moment</p>
                    </div>
                  )}
                </div>
              )}

              {/* Confluence Detector */}
              {confluence && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🎯 Confluence Detector</h2>
                  <div className="mb-4 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                    <p className="text-sm text-gray-400 mb-1">Current Price</p>
                    <p className="text-2xl font-bold text-white">${confluence.current_price?.toLocaleString()}</p>
                  </div>
                  {confluence.confluences && confluence.confluences.length > 0 ? (
                    <div className="space-y-3">
                      {confluence.confluences.map((conf: any, idx: number) => (
                        <div key={idx} className="bg-gray-900/50 p-4 rounded-lg border border-purple-500/30">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <p className="text-2xl font-bold text-purple-400">${conf.price?.toLocaleString()}</p>
                              <p className="text-sm text-gray-400">{conf.distance_pct}% from current price</p>
                            </div>
                            <div className="text-right">
                              <p className="text-sm text-gray-400">Confluences</p>
                              <p className="text-2xl font-bold text-blue-400">{conf.count}</p>
                            </div>
                          </div>
                          <div className="mt-2">
                            <div className="w-full bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-purple-500 h-2 rounded-full"
                                style={{ width: `${conf.strength}%` }}
                              ></div>
                            </div>
                            <p className="text-xs text-gray-400 mt-1">Strength: {conf.strength}/100</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-400">
                      <p>No significant confluences detected</p>
                    </div>
                  )}
                </div>
              )}

              {/* Reversal Probability */}
              {reversalProb && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🔄 Reversal Probability</h2>
                  <div className="mb-6">
                    <div className="text-center mb-4">
                      <p className="text-6xl font-bold text-blue-400 mb-2">{reversalProb.probability}%</p>
                      <p className="text-2xl font-bold text-white">{reversalProb.signal}</p>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-4">
                      <div
                        className={`h-4 rounded-full transition-all ${
                          reversalProb.probability >= 75 ? 'bg-green-500' :
                          reversalProb.probability >= 60 ? 'bg-yellow-500' :
                          reversalProb.probability >= 40 ? 'bg-orange-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${reversalProb.probability}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <p className="text-gray-400 font-semibold mb-3">Contributing Factors:</p>
                    {reversalProb.factors?.map((factor: any, idx: number) => (
                      <div key={idx} className="flex justify-between items-center bg-gray-900/50 p-3 rounded-lg">
                        <span className="text-gray-300">{factor.name}</span>
                        <span className={`font-bold ${factor.weight > 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {factor.weight > 0 ? '+' : ''}{factor.weight}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 bg-gray-900/50 p-3 rounded-lg">
                    <p className="text-gray-400 text-sm">Current RSI</p>
                    <p className="text-xl font-bold text-white">{reversalProb.rsi}</p>
                  </div>
                </div>
              )}
            </>
          )}

          {/* STATISTICS & PROBABILITY TAB */}
          {activeTab === 'statistics' && (
            <>
              {/* Monte Carlo Simulation */}
              {monteCarlo && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <BarChart3 className="w-6 h-6 text-blue-500" />
                    Monte Carlo Simulation ({monteCarlo.simulations} runs)
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Current Price</p>
                      <p className="text-2xl font-bold text-white">${monteCarlo.current_price?.toLocaleString()}</p>
                    </div>
                    <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-500/30">
                      <p className="text-gray-400 text-sm">Expected Price (30d)</p>
                      <p className="text-2xl font-bold text-blue-400">${monteCarlo.expected_price?.toLocaleString()}</p>
                      <p className="text-sm text-gray-400 mt-1">50th percentile</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Potential Gain</p>
                      <p className={`text-2xl font-bold ${monteCarlo.potential_gain >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {monteCarlo.potential_gain >= 0 ? '+' : ''}{monteCarlo.potential_gain}%
                      </p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="bg-green-900/20 p-4 rounded-lg border border-green-500/30">
                      <p className="text-gray-400 text-sm">Best Case (95th percentile)</p>
                      <p className="text-xl font-bold text-green-400">${monteCarlo.best_case_95pct?.toLocaleString()}</p>
                    </div>
                    <div className="bg-yellow-900/20 p-4 rounded-lg border border-yellow-500/30">
                      <p className="text-gray-400 text-sm">75th Percentile</p>
                      <p className="text-xl font-bold text-yellow-400">${monteCarlo.predicted_prices?.['75th']?.toLocaleString()}</p>
                    </div>
                    <div className="bg-orange-900/20 p-4 rounded-lg border border-orange-500/30">
                      <p className="text-gray-400 text-sm">25th Percentile</p>
                      <p className="text-xl font-bold text-orange-400">${monteCarlo.predicted_prices?.['25th']?.toLocaleString()}</p>
                    </div>
                    <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
                      <p className="text-gray-400 text-sm">Worst Case (5th percentile)</p>
                      <p className="text-xl font-bold text-red-400">${monteCarlo.worst_case_5pct?.toLocaleString()}</p>
                      <p className="text-sm text-gray-400 mt-1">Potential Loss: {monteCarlo.potential_loss}%</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Historical Calendar */}
              {calendar && calendar.monthly_averages && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <Calendar className="w-6 h-6 text-blue-500" />
                    Historical Performance Calendar
                  </h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                    {Object.entries(calendar.monthly_averages).map(([month, avg]: any) => (
                      <div key={month} className={`p-3 rounded-lg ${
                        avg > 0 ? 'bg-green-900/20 border border-green-500/30' : 'bg-red-900/20 border border-red-500/30'
                      }`}>
                        <p className="text-gray-400 text-sm">{month}</p>
                        <p className={`text-lg font-bold ${avg > 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {avg > 0 ? '+' : ''}{avg}%
                        </p>
                      </div>
                    ))}
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {calendar.best_month && (
                      <div className="bg-green-900/20 p-4 rounded-lg border border-green-500/30">
                        <p className="text-gray-400 text-sm">Best Month</p>
                        <p className="text-xl font-bold text-green-400">{calendar.best_month.month}</p>
                        <p className="text-sm text-gray-300">Avg Return: +{calendar.best_month.avg_return}%</p>
                      </div>
                    )}
                    {calendar.worst_month && (
                      <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
                        <p className="text-gray-400 text-sm">Worst Month</p>
                        <p className="text-xl font-bold text-red-400">{calendar.worst_month.month}</p>
                        <p className="text-sm text-gray-300">Avg Return: {calendar.worst_month.avg_return}%</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Drawdown Analysis */}
              {drawdown && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">📉 Drawdown Analysis</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className={`p-4 rounded-lg border ${
                      drawdown.status === 'In Drawdown' ? 'bg-red-900/20 border-red-500/30' : 'bg-green-900/20 border-green-500/30'
                    }`}>
                      <p className="text-gray-400 text-sm">Status</p>
                      <p className={`text-xl font-bold ${
                        drawdown.status === 'In Drawdown' ? 'text-red-400' : 'text-green-400'
                      }`}>
                        {drawdown.status}
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Current Drawdown</p>
                      <p className="text-2xl font-bold text-red-400">{drawdown.current_drawdown}%</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Max Drawdown</p>
                      <p className="text-2xl font-bold text-red-400">{drawdown.max_drawdown}%</p>
                    </div>
                  </div>
                  <div className="bg-gray-900/50 p-4 rounded-lg mb-4">
                    <p className="text-gray-400 text-sm">Average Recovery Time</p>
                    <p className="text-xl font-bold text-white">{drawdown.avg_recovery_days} days</p>
                  </div>
                  {drawdown.drawdown_periods && drawdown.drawdown_periods.length > 0 && (
                    <div className="space-y-2">
                      <p className="text-gray-400 font-semibold mb-2">Historical Drawdowns (worst first)</p>
                      {drawdown.drawdown_periods.slice(0, 5).map((dd: any, idx: number) => (
                        <div key={idx} className="bg-gray-900/50 p-3 rounded-lg">
                          <div className="flex justify-between items-start mb-1">
                            <span className="text-red-400 font-bold">{dd.drawdown_pct}%</span>
                            <span className="text-gray-400 text-sm">{dd.duration_days} days</span>
                          </div>
                          <div className="text-sm text-gray-400">
                            <span>{dd.start_date}</span>
                            <span className="mx-2">→</span>
                            <span>{dd.end_date}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Win Rate by Time */}
              {winRate && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">📊 Win Rate by Day/Hour</h2>
                  
                  {/* Best/Worst Days */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {winRate.best_day && (
                      <div className="bg-green-900/20 p-4 rounded-lg border border-green-500/30">
                        <p className="text-gray-400 text-sm mb-2">Best Day</p>
                        <p className="text-2xl font-bold text-green-400">{winRate.best_day.day}</p>
                        <p className="text-sm text-gray-300 mt-1">Avg Return: +{winRate.best_day.avg_return}%</p>
                        <p className="text-sm text-gray-400">Win Rate: {winRate.best_day.win_rate}%</p>
                      </div>
                    )}
                    {winRate.worst_day && (
                      <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
                        <p className="text-gray-400 text-sm mb-2">Worst Day</p>
                        <p className="text-2xl font-bold text-red-400">{winRate.worst_day.day}</p>
                        <p className="text-sm text-gray-300 mt-1">Avg Return: {winRate.worst_day.avg_return}%</p>
                        <p className="text-sm text-gray-400">Win Rate: {winRate.worst_day.win_rate}%</p>
                      </div>
                    )}
                  </div>

                  {/* All Days */}
                  {winRate.by_day && (
                    <div className="mb-6">
                      <p className="text-gray-400 font-semibold mb-3">Performance by Day of Week</p>
                      <div className="space-y-2">
                        {Object.entries(winRate.by_day).map(([day, stats]: any) => (
                          <div key={day} className="bg-gray-900/50 p-3 rounded-lg flex justify-between items-center">
                            <span className="text-white font-semibold">{day}</span>
                            <div className="text-right">
                              <p className={`font-bold ${stats.avg_return > 0 ? 'text-green-400' : 'text-red-400'}`}>
                                {stats.avg_return > 0 ? '+' : ''}{stats.avg_return}%
                              </p>
                              <p className="text-xs text-gray-400">Win: {stats.win_rate}%</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          {/* MOMENTUM & VELOCITY TAB */}
          {activeTab === 'momentum' && (
            <>
              {/* Acceleration Indicator */}
              {acceleration && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <Zap className="w-6 h-6 text-yellow-500" />
                    Acceleration Indicator
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Velocity</p>
                      <p className={`text-2xl font-bold ${acceleration.velocity > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {acceleration.velocity > 0 ? '+' : ''}{acceleration.velocity}%
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Acceleration</p>
                      <p className={`text-2xl font-bold ${acceleration.acceleration > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {acceleration.acceleration > 0 ? '+' : ''}{acceleration.acceleration}
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Jerk</p>
                      <p className="text-xl font-bold text-white">{acceleration.jerk}</p>
                    </div>
                  </div>
                  <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-500/30 mb-4">
                    <p className="text-xl font-bold text-blue-400">{acceleration.trend}</p>
                    <p className="text-gray-300 mt-1">{acceleration.interpretation}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Avg Velocity</p>
                      <p className="text-white font-semibold">{acceleration.avg_velocity}%</p>
                    </div>
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Signal</p>
                      <p className={`font-semibold ${
                        acceleration.signal === 'STRONG' ? 'text-green-400' :
                        acceleration.signal === 'WEAK' ? 'text-red-400' : 'text-yellow-400'
                      }`}>
                        {acceleration.signal}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Volume Momentum */}
              {volumeMomentum && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">📊 Volume Momentum</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Current Volume</p>
                      <p className="text-xl font-bold text-white">{volumeMomentum.current_volume?.toLocaleString()}</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Volume Ratio</p>
                      <p className="text-2xl font-bold text-blue-400">{volumeMomentum.volume_ratio}x</p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Trend</p>
                      <p className={`text-xl font-bold ${
                        volumeMomentum.trend === 'INCREASING' ? 'text-green-400' :
                        volumeMomentum.trend === 'DECREASING' ? 'text-red-400' : 'text-yellow-400'
                      }`}>
                        {volumeMomentum.trend}
                      </p>
                    </div>
                  </div>
                  <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-500/30 mb-4">
                    <p className="text-gray-300">{volumeMomentum.interpretation}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Strength</p>
                      <p className="text-white font-semibold">{volumeMomentum.strength}</p>
                    </div>
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Price-Volume Corr</p>
                      <p className="text-white font-semibold">{volumeMomentum.price_volume_correlation}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Price Velocity Gauge */}
              {velocity && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🚀 Price Velocity Gauge</h2>
                  <div className="text-center mb-6">
                    <p className="text-6xl font-bold text-blue-400 mb-2">{velocity.speed_classification}</p>
                    <p className="text-gray-400">{velocity.interpretation}</p>
                  </div>
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-900/50 p-4 rounded-lg text-center">
                      <p className="text-gray-400 text-sm">24h Return</p>
                      <p className={`text-xl font-bold ${velocity.return_1d > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {velocity.return_1d > 0 ? '+' : ''}{velocity.return_1d}%
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg text-center">
                      <p className="text-gray-400 text-sm">7d Return</p>
                      <p className={`text-xl font-bold ${velocity.return_1w > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {velocity.return_1w > 0 ? '+' : ''}{velocity.return_1w}%
                      </p>
                    </div>
                    <div className="bg-gray-900/50 p-4 rounded-lg text-center">
                      <p className="text-gray-400 text-sm">30d Return</p>
                      <p className={`text-xl font-bold ${velocity.return_1m > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {velocity.return_1m > 0 ? '+' : ''}{velocity.return_1m}%
                      </p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Daily Velocity Ratio</p>
                      <p className="text-white font-semibold">{velocity.daily_velocity_ratio}x</p>
                    </div>
                    <div className="bg-gray-900/50 p-3 rounded-lg">
                      <p className="text-gray-400 text-sm">Weekly Velocity Ratio</p>
                      <p className="text-white font-semibold">{velocity.weekly_velocity_ratio}x</p>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {/* RISK MANAGEMENT TAB */}
          {activeTab === 'risk' && (
            <>
              {/* Position Sizing Calculator */}
              {positionSizing && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                    <Shield className="w-6 h-6 text-green-500" />
                    Position Sizing Calculator
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="bg-gray-900/50 p-4 rounded-lg">
                      <p className="text-gray-400 text-sm">Account Size</p>
                      <p className="text-2xl font-bold text-white">${positionSizing.account_size?.toLocaleString()}</p>
                    </div>
                    <div className="bg-red-900/20 p-4 rounded-lg border border-red-500/30">
                      <p className="text-gray-400 text-sm">Risk per Trade</p>
                      <p className="text-2xl font-bold text-red-400">${positionSizing.risk_amount?.toLocaleString()}</p>
                      <p className="text-sm text-gray-400">{positionSizing.risk_percentage}%</p>
                    </div>
                    <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-500/30">
                      <p className="text-gray-400 text-sm">Position Size</p>
                      <p className="text-2xl font-bold text-blue-400">{positionSizing.position_size}</p>
                      <p className="text-sm text-gray-400">{ticker}</p>
                    </div>
                  </div>

                  <div className="bg-gray-900/50 p-4 rounded-lg mb-6">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                      <div>
                        <p className="text-gray-400 text-sm">Entry Price</p>
                        <p className="text-lg font-bold text-white">${positionSizing.current_price?.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-sm">Stop Loss</p>
                        <p className="text-lg font-bold text-red-400">${positionSizing.stop_loss_price?.toLocaleString()}</p>
                        <p className="text-xs text-gray-400">(-{positionSizing.stop_loss_pct}%)</p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-sm">Position Value</p>
                        <p className="text-lg font-bold text-white">${positionSizing.position_value?.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-sm">% of Account</p>
                        <p className="text-lg font-bold text-blue-400">{positionSizing.position_pct_of_account}%</p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-3 mb-6">
                    <p className="text-gray-400 font-semibold">Risk/Reward Scenarios:</p>
                    {positionSizing.scenarios?.map((scenario: any, idx: number) => (
                      <div key={idx} className="bg-gray-900/50 p-4 rounded-lg border border-green-500/30">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-lg font-bold text-white">R:R {scenario.risk_reward}</span>
                          <span className="text-gray-400">Target: ${scenario.target_price?.toLocaleString()}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-gray-400">Target Gain</p>
                            <p className="text-green-400 font-semibold">+{scenario.target_pct}%</p>
                          </div>
                          <div>
                            <p className="text-gray-400">Potential Profit</p>
                            <p className="text-green-400 font-semibold">${scenario.potential_profit?.toLocaleString()} (+{scenario.potential_profit_pct}%)</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="bg-purple-900/20 p-4 rounded-lg border border-purple-500/30">
                    <p className="text-gray-400 text-sm mb-2">ATR-Based Stop Suggestion</p>
                    <p className="text-xl font-bold text-purple-400">${positionSizing.atr_stop_suggestion?.toLocaleString()}</p>
                    <p className="text-sm text-gray-400">({positionSizing.atr_stop_pct}% below current price)</p>
                  </div>
                </div>
              )}

              {/* Risk/Reward Heatmap */}
              {riskReward && riskReward.matrix && (
                <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
                  <h2 className="text-2xl font-bold text-white mb-4">🎯 Risk/Reward Heatmap</h2>
                  <div className="mb-4 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
                    <p className="text-sm text-gray-400">Current Price</p>
                    <p className="text-2xl font-bold text-white">${riskReward.current_price?.toLocaleString()}</p>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-gray-700">
                          <th className="p-2 text-left text-gray-400">Stop Loss</th>
                          {[5, 10, 15, 20, 25, 30].map(target => (
                            <th key={target} className="p-2 text-center text-gray-400">{target}% Target</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {riskReward.matrix.map((row: any[], rowIdx: number) => (
                          <tr key={rowIdx} className="border-b border-gray-700/50">
                            <td className="p-2 font-semibold text-white">{row[0].stop_pct}%</td>
                            {row.map((cell: any, cellIdx: number) => (
                              <td key={cellIdx} className={`p-2 text-center font-bold ${
                                cell.quality === 'EXCELLENT' ? 'bg-green-900/30 text-green-400' :
                                cell.quality === 'GOOD' ? 'bg-blue-900/30 text-blue-400' :
                                cell.quality === 'FAIR' ? 'bg-yellow-900/30 text-yellow-400' :
                                'bg-red-900/30 text-red-400'
                              }`}>
                                {cell.risk_reward}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="mt-4 p-4 bg-gray-900/50 rounded-lg">
                    <p className="text-gray-400 text-sm">{riskReward.recommended}</p>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

