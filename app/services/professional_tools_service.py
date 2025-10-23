"""
Professional Tools Service
28 advanced trading analysis tools
All tools use only Yahoo Finance OHLCV data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


def safe_float(value):
    """Convert numpy types to Python float safely"""
    if pd.isna(value):
        return None
    return float(value)


def safe_int(value):
    """Convert numpy types to Python int safely"""
    if pd.isna(value):
        return None
    return int(value)


def safe_bool(value):
    """Convert numpy types to Python bool safely"""
    if pd.isna(value):
        return None
    return bool(value)


class ProfessionalToolsService:
    """Professional trading analysis tools"""
    
    # ============= 1. ICHIMOKU CLOUD COMPLETE =============
    
    @staticmethod
    def ichimoku_cloud(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Complete Ichimoku Cloud system
        """
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # Tenkan-sen (Conversion Line): 9-period high-low average
        period9_high = high.rolling(window=9).max()
        period9_low = low.rolling(window=9).min()
        tenkan_sen = (period9_high + period9_low) / 2
        
        # Kijun-sen (Base Line): 26-period high-low average
        period26_high = high.rolling(window=26).max()
        period26_low = low.rolling(window=26).min()
        kijun_sen = (period26_high + period26_low) / 2
        
        # Senkou Span A (Leading Span A): Average of Tenkan and Kijun, plotted 26 periods ahead
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
        
        # Senkou Span B (Leading Span B): 52-period high-low average, plotted 26 periods ahead
        period52_high = high.rolling(window=52).max()
        period52_low = low.rolling(window=52).min()
        senkou_span_b = ((period52_high + period52_low) / 2).shift(26)
        
        # Chikou Span (Lagging Span): Close plotted 26 periods in the past
        chikou_span = close.shift(-26)
        
        # Current values
        current_price = close.iloc[-1]
        current_tenkan = tenkan_sen.iloc[-1]
        current_kijun = kijun_sen.iloc[-1]
        current_span_a = senkou_span_a.iloc[-1] if not pd.isna(senkou_span_a.iloc[-1]) else 0
        current_span_b = senkou_span_b.iloc[-1] if not pd.isna(senkou_span_b.iloc[-1]) else 0
        
        # Signals
        tk_cross_bullish = current_tenkan > current_kijun
        price_above_cloud = current_price > max(current_span_a, current_span_b) if current_span_a and current_span_b else False
        cloud_is_bullish = current_span_a > current_span_b
        
        # Overall signal
        bullish_signals = sum([tk_cross_bullish, price_above_cloud, cloud_is_bullish])
        
        if bullish_signals >= 2:
            signal = "STRONG BUY"
        elif bullish_signals == 1:
            signal = "BUY"
        elif bullish_signals == 0:
            signal = "SELL"
        else:
            signal = "NEUTRAL"
        
        # Historical data for chart
        history = []
        for i in range(max(0, len(data) - 100), len(data)):
            if i < len(tenkan_sen) and not pd.isna(tenkan_sen.iloc[i]):
                history.append({
                    'date': data.index[i].strftime('%Y-%m-%d'),
                    'price': float(close.iloc[i]),
                    'tenkan': float(tenkan_sen.iloc[i]),
                    'kijun': float(kijun_sen.iloc[i]),
                    'span_a': float(senkou_span_a.iloc[i]) if i < len(senkou_span_a) and not pd.isna(senkou_span_a.iloc[i]) else None,
                    'span_b': float(senkou_span_b.iloc[i]) if i < len(senkou_span_b) and not pd.isna(senkou_span_b.iloc[i]) else None
                })
        
        return {
            "current_price": safe_float(current_price),
            "tenkan_sen": safe_float(current_tenkan),
            "kijun_sen": safe_float(current_kijun),
            "senkou_span_a": safe_float(current_span_a) if current_span_a else None,
            "senkou_span_b": safe_float(current_span_b) if current_span_b else None,
            "cloud_bullish": safe_bool(cloud_is_bullish),
            "tk_cross_bullish": safe_bool(tk_cross_bullish),
            "price_above_cloud": safe_bool(price_above_cloud),
            "signal": signal,
            "strength": int(bullish_signals),
            "history": history
        }
    
    # ============= 2. ELLIOTT WAVE COUNTER =============
    
    @staticmethod
    def elliott_wave_counter(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Simplified Elliott Wave detection
        """
        close = data['Close'].values
        
        # Find swing highs and lows
        swings = []
        window = 5
        
        for i in range(window, len(close) - window):
            if close[i] == max(close[i-window:i+window+1]):
                swings.append({'type': 'high', 'index': i, 'price': close[i]})
            elif close[i] == min(close[i-window:i+window+1]):
                swings.append({'type': 'low', 'index': i, 'price': close[i]})
        
        # Simple wave counting (alternating highs and lows)
        if len(swings) >= 5:
            last_5 = swings[-5:]
            
            # Check if it's an impulse wave pattern (5 waves)
            wave_pattern = [s['type'] for s in last_5]
            
            return {
                "waves_detected": len(last_5),
                "pattern": wave_pattern,
                "current_wave": "Wave 5" if len(wave_pattern) == 5 else f"Wave {len(wave_pattern)}",
                "swings": [
                    {
                        'date': data.index[s['index']].strftime('%Y-%m-%d'),
                        'type': s['type'],
                        'price': float(s['price'])
                    }
                    for s in last_5
                ],
                "analysis": "Potential impulse wave detected" if len(wave_pattern) >= 5 else "Collecting wave data"
            }
        
        return {
            "waves_detected": 0,
            "message": "Insufficient data for wave counting"
        }
    
    # ============= 3. WYCKOFF METHOD =============
    
    @staticmethod
    def wyckoff_analysis(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Wyckoff Method analysis
        """
        close = data['Close']
        volume = data['Volume']
        high = data['High']
        low = data['Low']
        
        # Price spread
        spread = high - low
        avg_spread = spread.rolling(20).mean()
        
        # Volume analysis
        avg_volume = volume.rolling(20).mean()
        volume_ratio = volume / avg_volume
        
        # Effort vs Result
        recent_spread = spread.iloc[-10:].mean()
        recent_volume = volume.iloc[-10:].mean()
        recent_price_change = abs(close.iloc[-1] - close.iloc[-10])
        
        # Detect phases
        high_volume_no_progress = (volume_ratio.iloc[-5:] > 1.5).any() and recent_price_change < recent_spread
        
        if high_volume_no_progress:
            phase = "Potential Distribution/Accumulation"
            signal = "CAUTION"
        elif volume_ratio.iloc[-1] > 1.5 and close.iloc[-1] > close.iloc[-2]:
            phase = "Markup Phase"
            signal = "BULLISH"
        elif volume_ratio.iloc[-1] > 1.5 and close.iloc[-1] < close.iloc[-2]:
            phase = "Markdown Phase"  
            signal = "BEARISH"
        else:
            phase = "Neutral"
            signal = "WAIT"
        
        # Spring detection (false breakdown with high volume)
        recent_low = low.iloc[-20:].min()
        is_spring = (low.iloc[-5:].min() <= recent_low * 1.01) and (volume.iloc[-5:].max() > avg_volume.iloc[-5:].max() * 1.5)
        
        return {
            "phase": phase,
            "signal": signal,
            "effort_vs_result": "High effort, low result" if high_volume_no_progress else "Balanced",
            "spring_detected": bool(is_spring),
            "volume_ratio": round(float(volume_ratio.iloc[-1]), 2),
            "avg_spread": round(float(avg_spread.iloc[-1]), 2),
            "analysis": "Watch for reversal" if is_spring else "Continue monitoring"
        }
    
    # ============= 4. MULTI-TIMEFRAME DASHBOARD =============
    
    @staticmethod
    def multi_timeframe_analysis(ticker: str, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Analyze multiple timeframes
        Expects data_dict with keys: '1h', '4h', '1d', '1w'
        """
        timeframes = {}
        
        for tf, data in data_dict.items():
            if len(data) < 50:
                continue
                
            close = data['Close']
            sma20 = close.rolling(20).mean()
            sma50 = close.rolling(50).mean()
            
            current_price = close.iloc[-1]
            current_sma20 = sma20.iloc[-1]
            current_sma50 = sma50.iloc[-1] if len(data) >= 50 else current_sma20
            
            trend = "BULLISH" if current_sma20 > current_sma50 else "BEARISH"
            price_vs_sma20 = "ABOVE" if current_price > current_sma20 else "BELOW"
            
            timeframes[tf] = {
                "price": float(current_price),
                "sma20": float(current_sma20),
                "sma50": float(current_sma50) if not pd.isna(current_sma50) else None,
                "trend": trend,
                "price_position": price_vs_sma20,
                "aligned": trend == "BULLISH" and price_vs_sma20 == "ABOVE"
            }
        
        # Overall alignment
        aligned_count = sum(1 for tf in timeframes.values() if tf.get('aligned', False))
        total_count = len(timeframes)
        
        alignment_score = (aligned_count / total_count * 100) if total_count > 0 else 0
        
        if alignment_score >= 75:
            overall_signal = "STRONG BULLISH"
        elif alignment_score >= 50:
            overall_signal = "BULLISH"
        elif alignment_score >= 25:
            overall_signal = "NEUTRAL"
        else:
            overall_signal = "BEARISH"
        
        return {
            "timeframes": timeframes,
            "aligned_count": aligned_count,
            "total_count": total_count,
            "alignment_score": round(alignment_score, 1),
            "overall_signal": overall_signal
        }
    
    # ============= 5. TREND ALIGNMENT SCANNER =============
    
    @staticmethod
    def trend_alignment_scanner(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Check trend alignment across indicators
        """
        close = data['Close']
        
        # Multiple SMAs
        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]
        sma100 = close.rolling(100).mean().iloc[-1] if len(data) >= 100 else sma50
        sma200 = close.rolling(200).mean().iloc[-1] if len(data) >= 200 else sma100
        
        current_price = close.iloc[-1]
        
        # Check alignments
        checks = {
            "price_above_sma20": current_price > sma20,
            "price_above_sma50": current_price > sma50,
            "sma20_above_sma50": sma20 > sma50,
            "sma50_above_sma100": sma50 > sma100,
            "sma100_above_sma200": sma100 > sma200
        }
        
        aligned = sum(checks.values())
        total = len(checks)
        score = (aligned / total) * 100
        
        return {
            "checks": [
                {"name": "Price > SMA20", "passed": bool(checks["price_above_sma20"])},
                {"name": "Price > SMA50", "passed": bool(checks["price_above_sma50"])},
                {"name": "SMA20 > SMA50", "passed": bool(checks["sma20_above_sma50"])},
                {"name": "SMA50 > SMA100", "passed": bool(checks["sma50_above_sma100"])},
                {"name": "SMA100 > SMA200", "passed": bool(checks["sma100_above_sma200"])}
            ],
            "aligned": int(aligned),
            "total": int(total),
            "score": round(float(score), 1),
            "signal": "STRONG BULLISH" if score >= 80 else "BULLISH" if score >= 60 else "NEUTRAL" if score >= 40 else "BEARISH"
        }
    
    # ============= 6. CORRELATION MATRIX =============
    
    @staticmethod
    def correlation_matrix(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Calculate correlation matrix between multiple cryptos
        """
        # Extract close prices
        prices = {}
        for ticker, data in data_dict.items():
            if len(data) > 0:
                prices[ticker] = data['Close']
        
        # Create DataFrame
        df = pd.DataFrame(prices)
        
        # Calculate correlation
        corr_matrix = df.corr()
        
        # Convert to dict
        matrix = {}
        for ticker1 in corr_matrix.columns:
            matrix[ticker1] = {}
            for ticker2 in corr_matrix.columns:
                matrix[ticker1][ticker2] = round(float(corr_matrix.loc[ticker1, ticker2]), 3)
        
        # Find highest and lowest correlations (excluding self-correlation)
        pairs = []
        tickers = list(corr_matrix.columns)
        for i, t1 in enumerate(tickers):
            for t2 in tickers[i+1:]:
                corr_val = corr_matrix.loc[t1, t2]
                pairs.append({
                    'pair': f"{t1} - {t2}",
                    'correlation': round(float(corr_val), 3)
                })
        
        pairs = sorted(pairs, key=lambda x: abs(x['correlation']), reverse=True)
        
        return {
            "matrix": matrix,
            "top_correlated": pairs[:5],
            "least_correlated": sorted(pairs, key=lambda x: abs(x['correlation']))[:5]
        }
    
    # ============= 7. SECTOR ROTATION =============
    
    @staticmethod
    def sector_rotation_analysis(sectors_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Analyze rotation between crypto sectors
        """
        sectors = {}
        
        for sector_name, data in sectors_data.items():
            if len(data) < 5:
                continue
            
            close = data['Close']
            volume = data['Volume']
            
            # Performance
            perf_1d = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) >= 2 else 0
            perf_7d = ((close.iloc[-1] - close.iloc[-8]) / close.iloc[-8] * 100) if len(close) >= 8 else 0
            perf_30d = ((close.iloc[-1] - close.iloc[-31]) / close.iloc[-31] * 100) if len(close) >= 31 else 0
            
            # Volume trend
            avg_volume_recent = volume.iloc[-5:].mean()
            avg_volume_older = volume.iloc[-15:-5].mean() if len(volume) >= 15 else avg_volume_recent
            volume_trend = "INCREASING" if avg_volume_recent > avg_volume_older * 1.1 else "DECREASING" if avg_volume_recent < avg_volume_older * 0.9 else "STABLE"
            
            sectors[sector_name] = {
                "perf_1d": round(float(perf_1d), 2),
                "perf_7d": round(float(perf_7d), 2),
                "perf_30d": round(float(perf_30d), 2),
                "volume_trend": volume_trend,
                "score": round(float(perf_7d * 0.5 + perf_30d * 0.5), 2)
            }
        
        # Rank sectors
        ranked = sorted(sectors.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return {
            "sectors": sectors,
            "rankings": [{"sector": name, **data} for name, data in ranked],
            "hot_sector": ranked[0][0] if ranked else None,
            "cold_sector": ranked[-1][0] if ranked else None
        }
    
    # ============= 8. CANDLESTICK PATTERN LIBRARY =============
    
    @staticmethod
    def candlestick_pattern_library(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive candlestick pattern detection
        """
        open_p = data['Open']
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        patterns_found = []
        
        # Need at least 3 candles
        if len(data) < 3:
            return {"patterns": [], "count": 0}
        
        # Last 3 candles
        o1, o2, o3 = open_p.iloc[-3], open_p.iloc[-2], open_p.iloc[-1]
        h1, h2, h3 = high.iloc[-3], high.iloc[-2], high.iloc[-1]
        l1, l2, l3 = low.iloc[-3], low.iloc[-2], low.iloc[-1]
        c1, c2, c3 = close.iloc[-3], close.iloc[-2], close.iloc[-1]
        
        # Body sizes
        body1 = abs(c1 - o1)
        body2 = abs(c2 - o2)
        body3 = abs(c3 - o3)
        
        # Morning Star (3 candles: bear, small, bull)
        if c1 < o1 and body2 < body1 * 0.3 and c3 > o3 and c3 > (c1 + o1) / 2:
            patterns_found.append({
                "name": "Morning Star",
                "type": "BULLISH",
                "confidence": 85,
                "description": "Strong bullish reversal pattern"
            })
        
        # Evening Star (3 candles: bull, small, bear)
        if c1 > o1 and body2 < body1 * 0.3 and c3 < o3 and c3 < (c1 + o1) / 2:
            patterns_found.append({
                "name": "Evening Star",
                "type": "BEARISH",
                "confidence": 85,
                "description": "Strong bearish reversal pattern"
            })
        
        # Three White Soldiers (3 consecutive strong bullish candles)
        if c1 > o1 and c2 > o2 and c3 > o3:
            if c2 > c1 and c3 > c2:
                patterns_found.append({
                    "name": "Three White Soldiers",
                    "type": "BULLISH",
                    "confidence": 80,
                    "description": "Strong uptrend continuation"
                })
        
        # Three Black Crows (3 consecutive strong bearish candles)
        if c1 < o1 and c2 < o2 and c3 < o3:
            if c2 < c1 and c3 < c2:
                patterns_found.append({
                    "name": "Three Black Crows",
                    "type": "BEARISH",
                    "confidence": 80,
                    "description": "Strong downtrend continuation"
                })
        
        # Hammer (last candle only)
        lower_shadow = min(o3, c3) - l3
        upper_shadow = h3 - max(o3, c3)
        if lower_shadow > body3 * 2 and upper_shadow < body3 * 0.3:
            patterns_found.append({
                "name": "Hammer",
                "type": "BULLISH",
                "confidence": 70,
                "description": "Potential bullish reversal"
            })
        
        # Shooting Star
        if upper_shadow > body3 * 2 and lower_shadow < body3 * 0.3:
            patterns_found.append({
                "name": "Shooting Star",
                "type": "BEARISH",
                "confidence": 70,
                "description": "Potential bearish reversal"
            })
        
        # Doji (very small body)
        if body3 < (h3 - l3) * 0.1:
            patterns_found.append({
                "name": "Doji",
                "type": "NEUTRAL",
                "confidence": 60,
                "description": "Indecision, potential reversal"
            })
        
        # Engulfing patterns
        if c3 > o3 and c2 < o2:  # Current is bullish, previous was bearish
            if o3 < c2 and c3 > o2:  # Engulfs previous
                patterns_found.append({
                    "name": "Bullish Engulfing",
                    "type": "BULLISH",
                    "confidence": 75,
                    "description": "Strong bullish reversal signal"
                })
        
        if c3 < o3 and c2 > o2:  # Current is bearish, previous was bullish
            if o3 > c2 and c3 < o2:  # Engulfs previous
                patterns_found.append({
                    "name": "Bearish Engulfing",
                    "type": "BEARISH",
                    "confidence": 75,
                    "description": "Strong bearish reversal signal"
                })
        
        return {
            "patterns": patterns_found,
            "count": len(patterns_found),
            "most_significant": max(patterns_found, key=lambda x: x['confidence']) if patterns_found else None
        }
    
    # ============= 9. SUPPORT/RESISTANCE ZONES =============
    
    @staticmethod
    def support_resistance_zones(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Advanced support and resistance zones
        """
        high = data['High'].values
        low = data['Low'].values
        close = data['Close'].values
        
        # Find pivot points
        zones = []
        window = 10
        
        for i in range(window, len(data) - window):
            # Resistance (high point)
            if high[i] == max(high[i-window:i+window+1]):
                price_level = high[i]
                # Count touches
                touches = sum(1 for j in range(len(high)) if abs(high[j] - price_level) / price_level < 0.02)
                zones.append({
                    'type': 'RESISTANCE',
                    'price': float(price_level),
                    'touches': touches,
                    'strength': min(touches * 20, 100),
                    'date': data.index[i].strftime('%Y-%m-%d')
                })
            
            # Support (low point)
            if low[i] == min(low[i-window:i+window+1]):
                price_level = low[i]
                touches = sum(1 for j in range(len(low)) if abs(low[j] - price_level) / price_level < 0.02)
                zones.append({
                    'type': 'SUPPORT',
                    'price': float(price_level),
                    'touches': touches,
                    'strength': min(touches * 20, 100),
                    'date': data.index[i].strftime('%Y-%m-%d')
                })
        
        # Remove duplicates and sort by strength
        unique_zones = []
        for zone in zones:
            is_duplicate = False
            for uz in unique_zones:
                if uz['type'] == zone['type'] and abs(uz['price'] - zone['price']) / zone['price'] < 0.01:
                    # Update if stronger
                    if zone['touches'] > uz['touches']:
                        uz['touches'] = zone['touches']
                        uz['strength'] = zone['strength']
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_zones.append(zone)
        
        # Sort by distance to current price
        current_price = close[-1]
        for zone in unique_zones:
            zone['distance_pct'] = round(((zone['price'] - current_price) / current_price) * 100, 2)
        
        unique_zones = sorted(unique_zones, key=lambda x: abs(x['distance_pct']))
        
        # Get nearest support and resistance
        nearest_support = next((z for z in unique_zones if z['type'] == 'SUPPORT' and z['price'] < current_price), None)
        nearest_resistance = next((z for z in unique_zones if z['type'] == 'RESISTANCE' and z['price'] > current_price), None)
        
        return {
            "zones": unique_zones[:10],  # Top 10
            "nearest_support": nearest_support,
            "nearest_resistance": nearest_resistance,
            "current_price": float(current_price)
        }
    
    # ============= 10. MONTE CARLO SIMULATION =============
    
    @staticmethod
    def monte_carlo_simulation(data: pd.DataFrame, days: int = 30, simulations: int = 1000) -> Dict[str, Any]:
        """
        Monte Carlo price simulation
        """
        returns = data['Close'].pct_change().dropna()
        
        mean_return = returns.mean()
        std_return = returns.std()
        
        last_price = data['Close'].iloc[-1]
        
        # Run simulations
        results = []
        for _ in range(simulations):
            prices = [last_price]
            for _ in range(days):
                daily_return = np.random.normal(mean_return, std_return)
                new_price = prices[-1] * (1 + daily_return)
                prices.append(new_price)
            results.append(prices[-1])
        
        # Calculate percentiles
        percentiles = {
            "5th": float(np.percentile(results, 5)),
            "25th": float(np.percentile(results, 25)),
            "50th": float(np.percentile(results, 50)),
            "75th": float(np.percentile(results, 75)),
            "95th": float(np.percentile(results, 95))
        }
        
        return {
            "current_price": float(last_price),
            "simulations": simulations,
            "days_ahead": days,
            "mean_return": round(float(mean_return * 100), 4),
            "std_return": round(float(std_return * 100), 4),
            "predicted_prices": percentiles,
            "expected_price": round(percentiles["50th"], 2),
            "worst_case_5pct": round(percentiles["5th"], 2),
            "best_case_95pct": round(percentiles["95th"], 2),
            "potential_gain": round(((percentiles["50th"] - last_price) / last_price) * 100, 2),
            "potential_loss": round(((percentiles["5th"] - last_price) / last_price) * 100, 2)
        }
    
    # ============= 11. HISTORICAL PERFORMANCE CALENDAR =============
    
    @staticmethod
    def historical_performance_calendar(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calendar heatmap of returns
        """
        data = data.copy()
        data['Return'] = data['Close'].pct_change() * 100
        data['Year'] = data.index.year
        data['Month'] = data.index.month
        data['Day'] = data.index.day
        
        # Monthly returns
        monthly = data.groupby(['Year', 'Month'])['Return'].sum().reset_index()
        
        # Create calendar structure
        calendar = {}
        for _, row in monthly.iterrows():
            year = int(row['Year'])
            month = int(row['Month'])
            ret = round(float(row['Return']), 2)
            
            if year not in calendar:
                calendar[year] = {}
            calendar[year][month] = ret
        
        # Calculate averages per month
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg = {}
        
        for month in range(1, 13):
            month_data = monthly[monthly['Month'] == month]['Return']
            if len(month_data) > 0:
                monthly_avg[month_names[month-1]] = round(float(month_data.mean()), 2)
        
        # Best and worst months
        best_month = max(monthly_avg.items(), key=lambda x: x[1]) if monthly_avg else None
        worst_month = min(monthly_avg.items(), key=lambda x: x[1]) if monthly_avg else None
        
        return {
            "calendar": calendar,
            "monthly_averages": monthly_avg,
            "best_month": {"month": best_month[0], "avg_return": best_month[1]} if best_month else None,
            "worst_month": {"month": worst_month[0], "avg_return": worst_month[1]} if worst_month else None
        }
    
    # ============= 12. DRAWDOWN ANALYSIS =============
    
    @staticmethod
    def drawdown_analysis(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive drawdown analysis
        """
        close = data['Close']
        
        # Calculate running maximum
        running_max = close.expanding().max()
        drawdown = (close - running_max) / running_max * 100
        
        # Current drawdown
        current_drawdown = float(drawdown.iloc[-1])
        max_drawdown = float(drawdown.min())
        
        # Find all drawdown periods
        drawdowns = []
        in_drawdown = False
        start_idx = 0
        
        for i in range(len(drawdown)):
            if drawdown.iloc[i] < -1 and not in_drawdown:  # Start of drawdown
                in_drawdown = True
                start_idx = i
            elif drawdown.iloc[i] >= -0.1 and in_drawdown:  # End of drawdown (recovered)
                peak = close.iloc[start_idx]
                trough = close.iloc[start_idx:i].min()
                recovery = close.iloc[i]
                dd_pct = ((trough - peak) / peak) * 100
                duration = i - start_idx
                
                drawdowns.append({
                    'start_date': data.index[start_idx].strftime('%Y-%m-%d'),
                    'end_date': data.index[i].strftime('%Y-%m-%d'),
                    'drawdown_pct': round(float(dd_pct), 2),
                    'duration_days': int(duration),
                    'peak_price': round(float(peak), 2),
                    'trough_price': round(float(trough), 2)
                })
                in_drawdown = False
        
        # Sort by severity
        drawdowns = sorted(drawdowns, key=lambda x: x['drawdown_pct'])[:10]
        
        # Average recovery time
        avg_recovery = np.mean([d['duration_days'] for d in drawdowns]) if drawdowns else 0
        
        return {
            "current_drawdown": round(current_drawdown, 2),
            "max_drawdown": round(max_drawdown, 2),
            "drawdown_periods": drawdowns,
            "total_drawdowns": len(drawdowns),
            "avg_recovery_days": round(float(avg_recovery), 1),
            "status": "In Drawdown" if current_drawdown < -5 else "Near Peak"
        }
    
    # ============= 13. WIN RATE BY DAY/HOUR =============
    
    @staticmethod
    def win_rate_by_time(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Win rate analysis by day and hour
        """
        data = data.copy()
        data['Return'] = data['Close'].pct_change() * 100
        data['DayOfWeek'] = data.index.day_name()
        data['Hour'] = data.index.hour
        
        # By day of week
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_stats = {}
        
        for day in days_order:
            day_data = data[data['DayOfWeek'] == day]['Return'].dropna()
            if len(day_data) > 0:
                wins = len(day_data[day_data > 0])
                total = len(day_data)
                win_rate = (wins / total) * 100 if total > 0 else 0
                avg_return = day_data.mean()
                
                day_stats[day] = {
                    'win_rate': round(float(win_rate), 2),
                    'avg_return': round(float(avg_return), 3),
                    'total_days': int(total)
                }
        
        # By hour
        hour_stats = {}
        for hour in range(24):
            hour_data = data[data['Hour'] == hour]['Return'].dropna()
            if len(hour_data) > 0:
                wins = len(hour_data[hour_data > 0])
                total = len(hour_data)
                win_rate = (wins / total) * 100 if total > 0 else 0
                avg_return = hour_data.mean()
                
                hour_stats[hour] = {
                    'win_rate': round(float(win_rate), 2),
                    'avg_return': round(float(avg_return), 3),
                    'total_periods': int(total)
                }
        
        # Best and worst
        best_day = max(day_stats.items(), key=lambda x: x[1]['avg_return']) if day_stats else None
        worst_day = min(day_stats.items(), key=lambda x: x[1]['avg_return']) if day_stats else None
        best_hour = max(hour_stats.items(), key=lambda x: x[1]['avg_return']) if hour_stats else None
        worst_hour = min(hour_stats.items(), key=lambda x: x[1]['avg_return']) if hour_stats else None
        
        return {
            "by_day": day_stats,
            "by_hour": hour_stats,
            "best_day": {"day": best_day[0], **best_day[1]} if best_day else None,
            "worst_day": {"day": worst_day[0], **worst_day[1]} if worst_day else None,
            "best_hour": {"hour": best_hour[0], **best_hour[1]} if best_hour else None,
            "worst_hour": {"hour": worst_hour[0], **worst_hour[1]} if worst_hour else None
        }
    
    # ============= 14. CONFLUENCE DETECTOR =============
    
    @staticmethod
    def confluence_detector(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect price levels with multiple confluences
        """
        close = data['Close']
        high = data['High']
        low = data['Low']
        
        current_price = close.iloc[-1]
        
        # Calculate key levels
        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]
        sma200 = close.rolling(200).mean().iloc[-1] if len(data) >= 200 else sma50
        
        # Fibonacci levels
        high_52w = high.iloc[-252:].max() if len(high) >= 252 else high.max()
        low_52w = low.iloc[-252:].min() if len(low) >= 252 else low.min()
        fib_range = high_52w - low_52w
        
        fib_levels = {
            '0%': low_52w,
            '23.6%': low_52w + fib_range * 0.236,
            '38.2%': low_52w + fib_range * 0.382,
            '50%': low_52w + fib_range * 0.50,
            '61.8%': low_52w + fib_range * 0.618,
            '78.6%': low_52w + fib_range * 0.786,
            '100%': high_52w
        }
        
        # Previous highs/lows
        swing_highs = []
        swing_lows = []
        window = 10
        
        for i in range(window, len(data) - window):
            if high.iloc[i] == high.iloc[i-window:i+window+1].max():
                swing_highs.append(float(high.iloc[i]))
            if low.iloc[i] == low.iloc[i-window:i+window+1].min():
                swing_lows.append(float(low.iloc[i]))
        
        # Find confluences
        all_levels = [sma20, sma50, sma200] + list(fib_levels.values()) + swing_highs[-5:] + swing_lows[-5:]
        
        confluences = []
        threshold = current_price * 0.02  # 2% range
        
        for level in all_levels:
            if pd.isna(level):
                continue
            
            # Find all levels near this one
            nearby = []
            for other_level in all_levels:
                if pd.isna(other_level):
                    continue
                if abs(level - other_level) < threshold and level != other_level:
                    nearby.append(other_level)
            
            if len(nearby) >= 2:  # At least 2 confluences
                avg_level = np.mean([level] + nearby)
                distance = ((avg_level - current_price) / current_price) * 100
                
                confluences.append({
                    'price': round(float(avg_level), 2),
                    'count': len(nearby) + 1,
                    'distance_pct': round(float(distance), 2),
                    'strength': min(len(nearby) * 25, 100)
                })
        
        # Remove duplicates and sort
        unique_confluences = []
        for conf in confluences:
            is_duplicate = False
            for uc in unique_confluences:
                if abs(uc['price'] - conf['price']) < threshold:
                    if conf['count'] > uc['count']:
                        unique_confluences.remove(uc)
                    else:
                        is_duplicate = True
                    break
            if not is_duplicate:
                unique_confluences.append(conf)
        
        unique_confluences = sorted(unique_confluences, key=lambda x: x['count'], reverse=True)[:5]
        
        return {
            "confluences": unique_confluences,
            "current_price": float(current_price),
            "strongest_confluence": unique_confluences[0] if unique_confluences else None
        }
    
    # ============= 15. REVERSAL PROBABILITY =============
    
    @staticmethod
    def reversal_probability(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate reversal probability
        """
        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume']
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]
        
        # Factors
        factors = []
        score = 50  # Start neutral
        
        # Factor 1: RSI extreme
        if current_rsi < 30:
            factors.append({"name": "RSI Oversold", "weight": +20})
            score += 20
        elif current_rsi > 70:
            factors.append({"name": "RSI Overbought", "weight": +20})
            score += 20
        
        # Factor 2: At support/resistance
        high_52w = high.iloc[-252:].max() if len(high) >= 252 else high.max()
        low_52w = low.iloc[-252:].min() if len(low) >= 252 else low.min()
        current_price = close.iloc[-1]
        
        if abs(current_price - low_52w) / low_52w < 0.05:
            factors.append({"name": "Near 52-week low", "weight": +15})
            score += 15
        elif abs(current_price - high_52w) / high_52w < 0.05:
            factors.append({"name": "Near 52-week high", "weight": +15})
            score += 15
        
        # Factor 3: Volume spike
        avg_volume = volume.rolling(20).mean().iloc[-1]
        if volume.iloc[-1] > avg_volume * 1.5:
            factors.append({"name": "High volume", "weight": +10})
            score += 10
        
        # Factor 4: Price action
        recent_change = ((close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]) * 100 if len(close) >= 5 else 0
        if abs(recent_change) > 10:
            factors.append({"name": "Extreme price move", "weight": +10})
            score += 10
        
        # Factor 5: Divergence check (simplified)
        if len(close) >= 20:
            price_trend = (close.iloc[-1] - close.iloc[-20]) / close.iloc[-20]
            rsi_trend = (rsi.iloc[-1] - rsi.iloc[-20]) / rsi.iloc[-20]
            
            if (price_trend < 0 and rsi_trend > 0) or (price_trend > 0 and rsi_trend < 0):
                factors.append({"name": "RSI Divergence", "weight": +15})
                score += 15
        
        # Cap score
        score = min(score, 95)
        score = max(score, 5)
        
        # Determine signal
        if score >= 75:
            signal = "HIGH PROBABILITY"
        elif score >= 60:
            signal = "MODERATE PROBABILITY"
        elif score >= 40:
            signal = "LOW PROBABILITY"
        else:
            signal = "UNLIKELY"
        
        return {
            "probability": round(score, 1),
            "signal": signal,
            "factors": factors,
            "total_factors": len(factors),
            "rsi": round(float(current_rsi), 2)
        }
    
    # ============= 16. ACCELERATION INDICATOR =============
    
    @staticmethod
    def acceleration_indicator(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Measure price acceleration
        """
        close = data['Close']
        
        # Calculate rate of change
        roc = close.pct_change() * 100
        
        # Acceleration (change in rate of change)
        acceleration = roc.diff()
        
        # Jerk (change in acceleration)
        jerk = acceleration.diff()
        
        # Current values
        current_roc = roc.iloc[-1]
        current_accel = acceleration.iloc[-1]
        current_jerk = jerk.iloc[-1]
        
        # Averages
        avg_roc = roc.iloc[-20:].mean()
        avg_accel = acceleration.iloc[-20:].mean()
        
        # Analysis
        if current_accel > avg_accel * 2:
            trend = "ACCELERATING FAST"
            signal = "STRONG"
        elif current_accel > avg_accel:
            trend = "ACCELERATING"
            signal = "MODERATE"
        elif current_accel < avg_accel * -2:
            trend = "DECELERATING FAST"
            signal = "WEAK"
        else:
            trend = "STABLE"
            signal = "NEUTRAL"
        
        return {
            "velocity": round(float(current_roc), 3),
            "acceleration": round(float(current_accel), 3),
            "jerk": round(float(current_jerk), 3),
            "avg_velocity": round(float(avg_roc), 3),
            "avg_acceleration": round(float(avg_accel), 3),
            "trend": trend,
            "signal": signal,
            "interpretation": f"Price is moving {abs(current_roc):.2f}% per period with {'increasing' if current_accel > 0 else 'decreasing'} momentum"
        }
    
    # ============= 17. VOLUME MOMENTUM =============
    
    @staticmethod
    def volume_momentum(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze volume momentum
        """
        volume = data['Volume']
        close = data['Close']
        
        # Volume moving averages
        vol_sma5 = volume.rolling(5).mean()
        vol_sma20 = volume.rolling(20).mean()
        vol_sma50 = volume.rolling(50).mean()
        
        current_vol = volume.iloc[-1]
        current_sma5 = vol_sma5.iloc[-1]
        current_sma20 = vol_sma20.iloc[-1]
        current_sma50 = vol_sma50.iloc[-1]
        
        # Volume trend
        if current_sma5 > current_sma20 > current_sma50:
            vol_trend = "INCREASING"
            strength = "STRONG"
        elif current_sma5 > current_sma20:
            vol_trend = "RISING"
            strength = "MODERATE"
        elif current_sma5 < current_sma20 < current_sma50:
            vol_trend = "DECREASING"
            strength = "WEAK"
        else:
            vol_trend = "MIXED"
            strength = "NEUTRAL"
        
        # Volume profile
        avg_vol = volume.mean()
        vol_ratio = current_vol / avg_vol
        
        # Price-volume correlation
        recent_returns = close.pct_change().iloc[-20:]
        recent_vol = volume.iloc[-20:]
        correlation = recent_returns.corr(recent_vol)
        
        return {
            "current_volume": float(current_vol),
            "avg_volume": float(avg_vol),
            "volume_ratio": round(float(vol_ratio), 2),
            "trend": vol_trend,
            "strength": strength,
            "price_volume_correlation": round(float(correlation), 3) if not pd.isna(correlation) else 0,
            "interpretation": f"Volume is {vol_ratio:.1f}x average and {vol_trend.lower()}"
        }
    
    # ============= 18. PRICE VELOCITY GAUGE =============
    
    @staticmethod
    def price_velocity_gauge(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Measure price velocity
        """
        close = data['Close']
        
        # Calculate various period returns
        ret_1d = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) >= 2 else 0
        ret_1w = ((close.iloc[-1] - close.iloc[-8]) / close.iloc[-8] * 100) if len(close) >= 8 else 0
        ret_1m = ((close.iloc[-1] - close.iloc[-31]) / close.iloc[-31] * 100) if len(close) >= 31 else 0
        
        # Historical averages
        daily_returns = close.pct_change() * 100
        avg_daily = daily_returns.mean()
        
        weekly_returns = close.pct_change(7) * 100
        avg_weekly = weekly_returns.mean()
        
        # Velocity ratios
        daily_velocity_ratio = ret_1d / avg_daily if avg_daily != 0 else 1
        weekly_velocity_ratio = ret_1w / avg_weekly if avg_weekly != 0 else 1
        
        # Classification
        if abs(weekly_velocity_ratio) > 3:
            speed = "PARABOLIC"
        elif abs(weekly_velocity_ratio) > 2:
            speed = "FAST"
        elif abs(weekly_velocity_ratio) > 1.5:
            speed = "ABOVE AVERAGE"
        elif abs(weekly_velocity_ratio) > 0.5:
            speed = "NORMAL"
        else:
            speed = "SLOW"
        
        return {
            "return_1d": round(float(ret_1d), 2),
            "return_1w": round(float(ret_1w), 2),
            "return_1m": round(float(ret_1m), 2),
            "avg_daily_return": round(float(avg_daily), 3),
            "avg_weekly_return": round(float(avg_weekly), 3),
            "daily_velocity_ratio": round(float(daily_velocity_ratio), 2),
            "weekly_velocity_ratio": round(float(weekly_velocity_ratio), 2),
            "speed_classification": speed,
            "interpretation": f"Moving {abs(weekly_velocity_ratio):.1f}x faster than average"
        }
    
    # ============= 19. POSITION SIZING CALCULATOR =============
    
    @staticmethod
    def position_sizing_calculator(
        data: pd.DataFrame,
        account_size: float,
        risk_pct: float,
        stop_loss_pct: float
    ) -> Dict[str, Any]:
        """
        Calculate optimal position size
        """
        current_price = float(data['Close'].iloc[-1])
        
        # Calculate position size
        risk_amount = account_size * (risk_pct / 100)
        stop_loss_distance = current_price * (stop_loss_pct / 100)
        position_size = risk_amount / stop_loss_distance
        position_value = position_size * current_price
        position_pct = (position_value / account_size) * 100
        
        # Calculate various risk/reward scenarios
        scenarios = []
        for rr in [1, 2, 3]:
            target_pct = stop_loss_pct * rr
            target_price = current_price * (1 + target_pct / 100)
            potential_profit = risk_amount * rr
            potential_profit_pct = (potential_profit / account_size) * 100
            
            scenarios.append({
                "risk_reward": f"1:{rr}",
                "target_price": round(target_price, 2),
                "target_pct": round(target_pct, 2),
                "potential_profit": round(potential_profit, 2),
                "potential_profit_pct": round(potential_profit_pct, 2)
            })
        
        # ATR-based stop
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
        
        atr_stop_distance = atr * 2
        atr_stop_price = current_price - atr_stop_distance
        
        return {
            "account_size": account_size,
            "risk_percentage": risk_pct,
            "risk_amount": round(risk_amount, 2),
            "current_price": round(current_price, 2),
            "stop_loss_pct": stop_loss_pct,
            "stop_loss_price": round(current_price * (1 - stop_loss_pct / 100), 2),
            "position_size": round(position_size, 6),
            "position_value": round(position_value, 2),
            "position_pct_of_account": round(position_pct, 2),
            "scenarios": scenarios,
            "atr_stop_suggestion": round(float(atr_stop_price), 2),
            "atr_stop_pct": round(float((atr_stop_distance / current_price) * 100), 2)
        }
    
    # ============= 20. RISK/REWARD HEATMAP =============
    
    @staticmethod
    def risk_reward_heatmap(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate risk/reward heatmap
        """
        current_price = float(data['Close'].iloc[-1])
        
        # Generate matrix
        stop_losses = [2, 3, 5, 7, 10]  # Percentage
        targets = [5, 10, 15, 20, 25, 30]  # Percentage
        
        matrix = []
        
        for stop in stop_losses:
            row = []
            for target in targets:
                rr_ratio = target / stop
                stop_price = current_price * (1 - stop / 100)
                target_price = current_price * (1 + target / 100)
                
                # Quality assessment
                if rr_ratio >= 3:
                    quality = "EXCELLENT"
                elif rr_ratio >= 2:
                    quality = "GOOD"
                elif rr_ratio >= 1:
                    quality = "FAIR"
                else:
                    quality = "POOR"
                
                row.append({
                    "stop_pct": stop,
                    "target_pct": target,
                    "risk_reward": round(rr_ratio, 2),
                    "quality": quality,
                    "stop_price": round(stop_price, 2),
                    "target_price": round(target_price, 2)
                })
            matrix.append(row)
        
        return {
            "current_price": round(current_price, 2),
            "matrix": matrix,
            "recommended": "Look for R:R >= 2:1 (green zones)"
        }
    
    # ============= 21-28: REMAINING TOOLS =============
    
    @staticmethod
    def custom_screener(data_dict: Dict[str, pd.DataFrame], conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Custom screener - apply user-defined conditions"""
        matches = []
        
        for ticker, data in data_dict.items():
            if len(data) < 50:
                continue
                
            close = data['Close']
            volume = data['Volume']
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Check conditions
            passes = True
            
            if 'rsi_min' in conditions and rsi.iloc[-1] < conditions['rsi_min']:
                passes = False
            if 'rsi_max' in conditions and rsi.iloc[-1] > conditions['rsi_max']:
                passes = False
            if 'volume_min' in conditions:
                avg_vol = volume.mean()
                if volume.iloc[-1] / avg_vol < conditions['volume_min']:
                    passes = False
            
            if passes:
                matches.append({
                    'ticker': ticker,
                    'price': float(close.iloc[-1]),
                    'rsi': round(float(rsi.iloc[-1]), 2),
                    'volume_ratio': round(float(volume.iloc[-1] / volume.mean()), 2)
                })
        
        return {
            "matches": matches,
            "total": len(matches),
            "conditions": conditions
        }
    
    @staticmethod
    def top_movers_matrix(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Top movers across timeframes"""
        results = []
        
        for ticker, data in data_dict.items():
            close = data['Close']
            if len(close) < 31:
                continue
            
            perf_24h = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100) if len(close) >= 2 else 0
            perf_7d = ((close.iloc[-1] - close.iloc[-8]) / close.iloc[-8] * 100) if len(close) >= 8 else 0
            perf_30d = ((close.iloc[-1] - close.iloc[-31]) / close.iloc[-31] * 100) if len(close) >= 31 else 0
            
            results.append({
                'ticker': ticker,
                'price': float(close.iloc[-1]),
                'perf_24h': round(float(perf_24h), 2),
                'perf_7d': round(float(perf_7d), 2),
                'perf_30d': round(float(perf_30d), 2)
            })
        
        return {
            "top_24h": sorted(results, key=lambda x: x['perf_24h'], reverse=True)[:5],
            "top_7d": sorted(results, key=lambda x: x['perf_7d'], reverse=True)[:5],
            "top_30d": sorted(results, key=lambda x: x['perf_30d'], reverse=True)[:5],
            "bottom_24h": sorted(results, key=lambda x: x['perf_24h'])[:5]
        }
    
    @staticmethod
    def technical_setup_finder(data: pd.DataFrame) -> Dict[str, Any]:
        """Find technical setups"""
        close = data['Close']
        volume = data['Volume']
        
        setups = []
        
        # Golden Cross
        sma50 = close.rolling(50).mean()
        sma200 = close.rolling(200).mean() if len(close) >= 200 else sma50
        
        if len(sma50) >= 2 and len(sma200) >= 2:
            if sma50.iloc[-2] < sma200.iloc[-2] and sma50.iloc[-1] > sma200.iloc[-1]:
                setups.append({
                    "name": "Golden Cross",
                    "type": "BULLISH",
                    "confidence": 85
                })
        
        # RSI Oversold
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        if rsi.iloc[-1] < 30:
            setups.append({
                "name": "RSI Oversold",
                "type": "BULLISH",
                "confidence": 70
            })
        
        # Volume Breakout
        avg_vol = volume.rolling(20).mean().iloc[-1]
        if volume.iloc[-1] > avg_vol * 2:
            setups.append({
                "name": "Volume Spike",
                "type": "ATTENTION",
                "confidence": 75
            })
        
        return {
            "setups": setups,
            "count": len(setups)
        }


# Singleton
professional_tools_service = ProfessionalToolsService()

