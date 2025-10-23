"""
Advanced Analysis Service
Implementa 20+ análises avançadas para criptomoedas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class AdvancedAnalysisService:
    """Serviço de análises técnicas avançadas"""
    
    # ============= 1. DIVERGENCE DETECTION =============
    
    @staticmethod
    def detect_divergences(data: pd.DataFrame, lookback: int = 20) -> Dict[str, Any]:
        """
        Detecta divergências entre preço e RSI
        """
        divergences = []
        
        if len(data) < lookback * 2:
            return {"divergences": [], "total": 0}
        
        # Encontra swing highs e lows
        close = data['Close'].values
        rsi = data['RSI'].values if 'RSI' in data.columns else np.zeros(len(data))
        
        for i in range(lookback, len(data) - lookback):
            # Swing High
            if close[i] == max(close[i-lookback:i+lookback+1]):
                # Procura swing high anterior
                for j in range(i-lookback*2, i-lookback):
                    if j > 0 and close[j] == max(close[max(0, j-lookback):min(len(close), j+lookback+1)]):
                        # Bearish Divergence: Preço sobe, RSI desce
                        if close[i] > close[j] and rsi[i] < rsi[j]:
                            divergences.append({
                                'type': 'Bearish',
                                'date': data.index[i].strftime('%Y-%m-%d'),
                                'price': float(close[i]),
                                'rsi': float(rsi[i]),
                                'strength': abs(rsi[j] - rsi[i])
                            })
                        break
            
            # Swing Low
            if close[i] == min(close[i-lookback:i+lookback+1]):
                # Procura swing low anterior
                for j in range(i-lookback*2, i-lookback):
                    if j > 0 and close[j] == min(close[max(0, j-lookback):min(len(close), j+lookback+1)]):
                        # Bullish Divergence: Preço desce, RSI sobe
                        if close[i] < close[j] and rsi[i] > rsi[j]:
                            divergences.append({
                                'type': 'Bullish',
                                'date': data.index[i].strftime('%Y-%m-%d'),
                                'price': float(close[i]),
                                'rsi': float(rsi[i]),
                                'strength': abs(rsi[i] - rsi[j])
                            })
                        break
        
        # Últimas 10 divergências
        divergences = sorted(divergences, key=lambda x: x['date'], reverse=True)[:10]
        
        return {
            "divergences": divergences,
            "total": len(divergences),
            "last_signal": divergences[0] if divergences else None
        }
    
    # ============= 2. GAP ANALYSIS =============
    
    @staticmethod
    def analyze_gaps(data: pd.DataFrame, min_gap_percent: float = 2.0) -> Dict[str, Any]:
        """
        Analisa gaps de preço
        """
        gaps = []
        
        for i in range(1, len(data)):
            prev_close = data['Close'].iloc[i-1]
            curr_open = data['Open'].iloc[i]
            curr_high = data['High'].iloc[i]
            curr_low = data['Low'].iloc[i]
            curr_close = data['Close'].iloc[i]
            
            gap_percent = ((curr_open - prev_close) / prev_close) * 100
            
            if abs(gap_percent) >= min_gap_percent:
                # Verifica se o gap foi preenchido
                filled = False
                fill_date = None
                
                if gap_percent > 0:  # Gap Up
                    # Gap preenchido se preço voltar ao close anterior
                    for j in range(i, len(data)):
                        if data['Low'].iloc[j] <= prev_close:
                            filled = True
                            fill_date = data.index[j].strftime('%Y-%m-%d')
                            break
                else:  # Gap Down
                    for j in range(i, len(data)):
                        if data['High'].iloc[j] >= prev_close:
                            filled = True
                            fill_date = data.index[j].strftime('%Y-%m-%d')
                            break
                
                gaps.append({
                    'date': data.index[i].strftime('%Y-%m-%d'),
                    'type': 'Gap Up' if gap_percent > 0 else 'Gap Down',
                    'gap_percent': round(gap_percent, 2),
                    'prev_close': float(prev_close),
                    'open': float(curr_open),
                    'filled': filled,
                    'fill_date': fill_date,
                    'days_to_fill': (pd.to_datetime(fill_date) - data.index[i]).days if filled else None
                })
        
        unfilled_gaps = [g for g in gaps if not g['filled']]
        
        return {
            "all_gaps": sorted(gaps, key=lambda x: x['date'], reverse=True)[:20],
            "unfilled_gaps": sorted(unfilled_gaps, key=lambda x: x['date'], reverse=True),
            "total_gaps": len(gaps),
            "unfilled_count": len(unfilled_gaps),
            "fill_rate": round((len(gaps) - len(unfilled_gaps)) / len(gaps) * 100, 1) if gaps else 0
        }
    
    # ============= 3. BREAKOUT SCANNER =============
    
    @staticmethod
    def detect_breakouts(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detecta breakouts de preço
        """
        if len(data) < 252:
            return {"breakout": False, "type": None}
        
        current_price = data['Close'].iloc[-1]
        high_52w = data['High'].iloc[-252:].max()
        low_52w = data['Low'].iloc[-252:].min()
        
        # Volume médio 20 dias
        avg_volume = data['Volume'].iloc[-20:].mean()
        current_volume = data['Volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # ATR para medir volatilidade
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(14).mean().iloc[-1]
        atr_percent = (atr / current_price) * 100
        
        # Detecta breakout
        breakout_up = current_price >= high_52w * 0.998  # 0.2% de tolerância
        breakout_down = current_price <= low_52w * 1.002
        
        # Consolidação (range < 5% nas últimas 20 velas)
        recent_high = data['High'].iloc[-20:].max()
        recent_low = data['Low'].iloc[-20:].min()
        consolidation_range = ((recent_high - recent_low) / recent_low) * 100
        consolidating = consolidation_range < 5
        
        # Score de força do breakout
        score = 0
        if breakout_up or breakout_down:
            score += 30
        if volume_ratio > 1.5:
            score += 30
        if atr_percent > 2:
            score += 20
        if consolidating:
            score += 20
        
        return {
            "breakout": bool(breakout_up or breakout_down),
            "type": "Bullish" if breakout_up else "Bearish" if breakout_down else None,
            "current_price": float(current_price),
            "high_52w": float(high_52w),
            "low_52w": float(low_52w),
            "distance_to_high": round(float(((high_52w - current_price) / current_price) * 100), 2),
            "distance_to_low": round(float(((current_price - low_52w) / low_52w) * 100), 2),
            "volume_ratio": round(float(volume_ratio), 2),
            "consolidating": bool(consolidating),
            "consolidation_range": round(float(consolidation_range), 2),
            "atr_percent": round(float(atr_percent), 2),
            "strength_score": int(score),
            "signal": "STRONG" if score > 70 else "MODERATE" if score > 50 else "WEAK"
        }
    
    # ============= 4. ADVANCED SUPPORT/RESISTANCE =============
    
    @staticmethod
    def advanced_support_resistance(data: pd.DataFrame, num_levels: int = 5) -> Dict[str, Any]:
        """
        Detecta suporte e resistência com cluster analysis
        """
        current_price = data['Close'].iloc[-1]
        
        # Combina highs e lows
        price_levels = pd.concat([data['High'], data['Low']]).values
        
        # Agrupa preços em bins (1% de largura)
        bin_size = current_price * 0.01
        bins = np.arange(price_levels.min(), price_levels.max() + bin_size, bin_size)
        hist, edges = np.histogram(price_levels, bins=bins)
        
        # Encontra os bins com mais toques
        significant_indices = np.argsort(hist)[-num_levels*2:]
        
        levels = []
        for idx in significant_indices:
            level_price = (edges[idx] + edges[idx + 1]) / 2
            touches = int(hist[idx])
            
            # Calcula volume médio nesse nível
            mask = (data['Low'] <= level_price) & (data['High'] >= level_price)
            avg_volume = data.loc[mask, 'Volume'].mean() if mask.any() else 0
            
            # Determina se é suporte ou resistência
            is_support = level_price < current_price
            
            levels.append({
                'price': float(level_price),
                'touches': touches,
                'type': 'Support' if is_support else 'Resistance',
                'strength': min(touches / 10 * 100, 100),  # Normaliza para 0-100
                'distance_percent': round(((level_price - current_price) / current_price) * 100, 2),
                'avg_volume': float(avg_volume)
            })
        
        # Separa suportes e resistências
        supports = sorted([l for l in levels if l['type'] == 'Support'], 
                         key=lambda x: x['price'], reverse=True)[:num_levels]
        resistances = sorted([l for l in levels if l['type'] == 'Resistance'], 
                            key=lambda x: x['price'])[:num_levels]
        
        # Níveis psicológicos (números redondos)
        psychological = []
        for multiplier in [1, 10, 100, 1000, 10000]:
            for base in [1, 2, 5]:
                level = base * multiplier
                if data['Low'].min() < level < data['High'].max():
                    psychological.append(level)
        
        psychological = [p for p in psychological if abs((p - current_price) / current_price) < 0.2][:5]
        
        return {
            "current_price": float(current_price),
            "supports": supports,
            "resistances": resistances,
            "psychological_levels": [float(p) for p in psychological],
            "nearest_support": supports[0] if supports else None,
            "nearest_resistance": resistances[0] if resistances else None
        }
    
    # ============= 5. MOMENTUM MULTI-TIMEFRAME =============
    
    @staticmethod
    def momentum_multi_timeframe(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula momentum em múltiplos períodos
        """
        current_price = data['Close'].iloc[-1]
        
        periods = {
            '1_week': 5,
            '1_month': 20,
            '3_months': 60,
            '6_months': 120,
            '1_year': 252
        }
        
        momentum = {}
        weights = {'1_week': 0.1, '1_month': 0.2, '3_months': 0.3, '6_months': 0.25, '1_year': 0.15}
        
        weighted_score = 0
        
        for period_name, days in periods.items():
            if len(data) >= days:
                past_price = data['Close'].iloc[-days]
                change_percent = ((current_price - past_price) / past_price) * 100
                
                # Score: -100 a +100
                score = max(min(change_percent * 2, 100), -100)
                
                momentum[period_name] = {
                    'change_percent': round(change_percent, 2),
                    'score': round(score, 1)
                }
                
                weighted_score += score * weights[period_name]
        
        # Classificação
        if weighted_score > 50:
            classification = "VERY STRONG"
        elif weighted_score > 20:
            classification = "STRONG"
        elif weighted_score > -20:
            classification = "NEUTRAL"
        elif weighted_score > -50:
            classification = "WEAK"
        else:
            classification = "VERY WEAK"
        
        return {
            "momentum": momentum,
            "weighted_score": round(weighted_score, 1),
            "classification": classification,
            "trend": "Bullish" if weighted_score > 0 else "Bearish"
        }
    
    # ============= 6. RELATIVE STRENGTH RANKING =============
    
    @staticmethod
    def calculate_relative_strength(crypto_data: pd.DataFrame, btc_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula força relativa vs Bitcoin
        """
        if len(crypto_data) < 20 or len(btc_data) < 20:
            return {"error": "Insufficient data"}
        
        # Alinha datas
        common_dates = crypto_data.index.intersection(btc_data.index)
        crypto_aligned = crypto_data.loc[common_dates, 'Close']
        btc_aligned = btc_data.loc[common_dates, 'Close']
        
        # Calcula RS Line
        rs_line = (crypto_aligned / btc_aligned) * 100
        
        # Mudança da RS Line
        rs_change_1m = ((rs_line.iloc[-1] / rs_line.iloc[-20]) - 1) * 100 if len(rs_line) >= 20 else 0
        rs_change_3m = ((rs_line.iloc[-1] / rs_line.iloc[-60]) - 1) * 100 if len(rs_line) >= 60 else 0
        
        # Performance vs BTC
        crypto_return = ((crypto_aligned.iloc[-1] / crypto_aligned.iloc[0]) - 1) * 100
        btc_return = ((btc_aligned.iloc[-1] / btc_aligned.iloc[0]) - 1) * 100
        outperformance = crypto_return - btc_return
        
        return {
            "rs_current": round(float(rs_line.iloc[-1]), 2),
            "rs_change_1m": round(rs_change_1m, 2),
            "rs_change_3m": round(rs_change_3m, 2),
            "outperformance": round(outperformance, 2),
            "is_outperforming": outperformance > 0,
            "strength": "Strong" if rs_change_1m > 5 else "Weak" if rs_change_1m < -5 else "Neutral",
            "rs_line_data": [
                {"date": idx.strftime('%Y-%m-%d'), "value": round(float(val), 2)}
                for idx, val in rs_line.iloc[-60:].items()
            ]
        }
    
    # ============= 7. MEAN REVERSION Z-SCORE =============
    
    @staticmethod
    def mean_reversion_zscore(data: pd.DataFrame, window: int = 20) -> Dict[str, Any]:
        """
        Calcula Z-Score para mean reversion
        """
        close = data['Close']
        
        # Calcula SMA e StdDev
        sma = close.rolling(window).mean()
        std = close.rolling(window).std()
        
        # Z-Score
        z_score = (close - sma) / std
        current_z = z_score.iloc[-1]
        
        # Bollinger %B
        bb_upper = sma + (2 * std)
        bb_lower = sma - (2 * std)
        bb_percent = ((close - bb_lower) / (bb_upper - bb_lower)) * 100
        current_bb = bb_percent.iloc[-1]
        
        # Signal
        if current_z > 2:
            signal = "OVERBOUGHT"
            recommendation = "Consider selling"
            probability = 75
        elif current_z < -2:
            signal = "OVERSOLD"
            recommendation = "Consider buying"
            probability = 75
        elif abs(current_z) > 1:
            signal = "MODERATE"
            recommendation = "Watch for reversal"
            probability = 50
        else:
            signal = "NEUTRAL"
            recommendation = "No clear signal"
            probability = 30
        
        # Histórico
        history = [
            {
                "date": idx.strftime('%Y-%m-%d'),
                "price": float(data['Close'].loc[idx]),
                "z_score": round(float(z_score.loc[idx]), 2),
                "sma": round(float(sma.loc[idx]), 2)
            }
            for idx in data.index[-60:]
            if not np.isnan(z_score.loc[idx])
        ]
        
        return {
            "current_price": float(close.iloc[-1]),
            "sma": float(sma.iloc[-1]),
            "z_score": round(float(current_z), 2),
            "bb_percent": round(float(current_bb), 1),
            "signal": signal,
            "recommendation": recommendation,
            "reversion_probability": probability,
            "history": history
        }
    
    # ============= 8. SWING TRADING SIGNALS =============
    
    @staticmethod
    def swing_trading_signals(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Identifica setups de swing trading
        """
        if len(data) < 50:
            return {"setup_found": False}
        
        current_price = data['Close'].iloc[-1]
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(50).mean().iloc[-1]
        rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns else 50
        
        # Encontra swing low recente (últimos 10 dias)
        recent_low = data['Low'].iloc[-10:].min()
        recent_high = data['High'].iloc[-10:].max()
        
        # Setup de compra (Bullish)
        bullish_setup = (
            current_price > sma_20 and
            sma_20 > sma_50 and
            rsi < 60 and rsi > 40 and
            current_price < recent_high * 0.98
        )
        
        # Setup de venda (Bearish)
        bearish_setup = (
            current_price < sma_20 and
            sma_20 < sma_50 and
            rsi > 40 and rsi < 60 and
            current_price > recent_low * 1.02
        )
        
        if bullish_setup:
            entry = current_price
            stop_loss = recent_low * 0.98
            take_profit = current_price + (current_price - stop_loss) * 2  # R:R 1:2
            risk = entry - stop_loss
            reward = take_profit - entry
            
            return {
                "setup_found": True,
                "type": "BULLISH",
                "entry": round(float(entry), 2),
                "stop_loss": round(float(stop_loss), 2),
                "take_profit": round(float(take_profit), 2),
                "risk": round(float(risk), 2),
                "reward": round(float(reward), 2),
                "risk_reward_ratio": round(reward / risk, 2) if risk > 0 else 0,
                "validity_days": 3,
                "confidence": "HIGH" if rsi < 50 else "MODERATE"
            }
        elif bearish_setup:
            entry = current_price
            stop_loss = recent_high * 1.02
            take_profit = current_price - (stop_loss - current_price) * 2
            risk = stop_loss - entry
            reward = entry - take_profit
            
            return {
                "setup_found": True,
                "type": "BEARISH",
                "entry": round(float(entry), 2),
                "stop_loss": round(float(stop_loss), 2),
                "take_profit": round(float(take_profit), 2),
                "risk": round(float(risk), 2),
                "reward": round(float(reward), 2),
                "risk_reward_ratio": round(reward / risk, 2) if risk > 0 else 0,
                "validity_days": 3,
                "confidence": "HIGH" if rsi > 50 else "MODERATE"
            }
        
        return {
            "setup_found": False,
            "reason": "No clear setup at the moment"
        }
    
    # ============= 9. SEASONALITY ANALYSIS =============
    
    @staticmethod
    def seasonality_analysis(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analisa padrões sazonais
        """
        if len(data) < 365:
            return {"error": "Need at least 1 year of data"}
        
        # Adiciona colunas de tempo
        df = data.copy()
        df['Month'] = df.index.month
        df['Weekday'] = df.index.dayofweek
        df['Returns'] = df['Close'].pct_change() * 100
        
        # Performance por mês
        monthly_perf = df.groupby('Month')['Returns'].agg(['mean', 'count']).to_dict()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        monthly_data = [
            {
                "month": month_names[i],
                "avg_return": round(monthly_perf['mean'].get(i+1, 0), 2),
                "count": int(monthly_perf['count'].get(i+1, 0))
            }
            for i in range(12)
        ]
        
        # Performance por dia da semana
        weekday_perf = df.groupby('Weekday')['Returns'].mean().to_dict()
        weekday_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        weekday_data = [
            {
                "day": weekday_names[i],
                "avg_return": round(weekday_perf.get(i, 0), 2)
            }
            for i in range(7)
        ]
        
        # Melhor e pior mês
        best_month_idx = max(monthly_perf['mean'].items(), key=lambda x: x[1])[0] - 1
        worst_month_idx = min(monthly_perf['mean'].items(), key=lambda x: x[1])[0] - 1
        
        # Melhor e pior dia
        best_day_idx = max(weekday_perf.items(), key=lambda x: x[1])[0]
        worst_day_idx = min(weekday_perf.items(), key=lambda x: x[1])[0]
        
        return {
            "monthly": monthly_data,
            "weekday": weekday_data,
            "best_month": month_names[best_month_idx],
            "worst_month": month_names[worst_month_idx],
            "best_day": weekday_names[best_day_idx],
            "worst_day": weekday_names[worst_day_idx]
        }
    
    # ============= 10. VOLATILITY ANALYSIS EXPANDED =============
    
    @staticmethod
    def volatility_analysis_expanded(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Análise expandida de volatilidade
        """
        returns = data['Close'].pct_change().dropna()
        
        # Volatilidade histórica (anualizada)
        current_vol = returns.iloc[-20:].std() * np.sqrt(252) * 100
        hist_vol_mean = returns.std() * np.sqrt(252) * 100
        hist_vol_std = returns.rolling(20).std().std() * np.sqrt(252) * 100
        
        # Volatility Percentile
        rolling_vol = returns.rolling(20).std() * np.sqrt(252) * 100
        vol_percentile = (rolling_vol < current_vol).sum() / len(rolling_vol) * 100
        
        # Bollinger Band Width
        if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns and 'BB_Middle' in data.columns:
            bb_width = ((data['BB_Upper'] - data['BB_Lower']) / data['BB_Middle']) * 100
            current_bb_width = bb_width.iloc[-1]
            avg_bb_width = bb_width.mean()
            
            # Squeeze detection
            squeeze = current_bb_width < avg_bb_width * 0.7
        else:
            current_bb_width = 0
            avg_bb_width = 0
            squeeze = False
        
        # ATR
        if 'High' in data.columns and 'Low' in data.columns:
            high_low = data['High'] - data['Low']
            high_close = np.abs(data['High'] - data['Close'].shift())
            low_close = np.abs(data['Low'] - data['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            atr = true_range.rolling(14).mean()
            current_atr = atr.iloc[-1]
            atr_percent = (current_atr / data['Close'].iloc[-1]) * 100
        else:
            current_atr = 0
            atr_percent = 0
        
        # Classificação
        if vol_percentile > 80:
            classification = "VERY HIGH"
            signal = "Expect mean reversion"
        elif vol_percentile > 60:
            classification = "HIGH"
            signal = "Above average volatility"
        elif vol_percentile > 40:
            classification = "NORMAL"
            signal = "Average volatility"
        elif vol_percentile > 20:
            classification = "LOW"
            signal = "Below average volatility"
        else:
            classification = "VERY LOW"
            signal = "Potential breakout coming"
        
        return {
            "current_volatility": round(float(current_vol), 2),
            "historical_avg": round(float(hist_vol_mean), 2),
            "volatility_percentile": round(float(vol_percentile), 1),
            "classification": classification,
            "signal": signal,
            "bb_width_current": round(float(current_bb_width), 2),
            "bb_width_avg": round(float(avg_bb_width), 2),
            "squeeze_detected": squeeze,
            "atr": round(float(current_atr), 2),
            "atr_percent": round(float(atr_percent), 2)
        }


    # ============= 11. PRICE ACTION PATTERNS =============
    
    @staticmethod
    def detect_price_patterns(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detecta padrões clássicos de price action
        """
        patterns_found = []
        
        if len(data) < 50:
            return {"patterns": [], "total": 0}
        
        close = data['Close'].values
        high = data['High'].values
        low = data['Low'].values
        
        # Double Top (últimos 60 dias)
        if len(data) >= 60:
            window = close[-60:]
            peaks = []
            for i in range(5, len(window)-5):
                if window[i] == max(window[i-5:i+6]):
                    peaks.append((i, window[i]))
            
            if len(peaks) >= 2:
                last_two = peaks[-2:]
                if abs(last_two[0][1] - last_two[1][1]) / last_two[0][1] < 0.02:  # 2% tolerance
                    patterns_found.append({
                        'pattern': 'Double Top',
                        'type': 'Bearish',
                        'confidence': 70,
                        'target': float(min(window)),
                        'description': 'Reversal pattern - Consider selling'
                    })
        
        # Double Bottom
        if len(data) >= 60:
            window = close[-60:]
            troughs = []
            for i in range(5, len(window)-5):
                if window[i] == min(window[i-5:i+6]):
                    troughs.append((i, window[i]))
            
            if len(troughs) >= 2:
                last_two = troughs[-2:]
                if abs(last_two[0][1] - last_two[1][1]) / last_two[0][1] < 0.02:
                    patterns_found.append({
                        'pattern': 'Double Bottom',
                        'type': 'Bullish',
                        'confidence': 70,
                        'target': float(max(window)),
                        'description': 'Reversal pattern - Consider buying'
                    })
        
        # Triângulo Ascendente
        if len(data) >= 30:
            recent_highs = high[-30:]
            recent_lows = low[-30:]
            
            # Resistência horizontal (highs)
            high_std = np.std(recent_highs[-5:])
            # Suporte ascendente (lows)
            low_trend = np.polyfit(range(30), recent_lows, 1)[0]
            
            if high_std < close[-1] * 0.01 and low_trend > 0:
                patterns_found.append({
                    'pattern': 'Ascending Triangle',
                    'type': 'Bullish',
                    'confidence': 65,
                    'target': float(close[-1] * 1.1),
                    'description': 'Continuation pattern - Breakout expected'
                })
        
        # Flag Pattern (alta rápida seguida de consolidação)
        if len(data) >= 20:
            pole_return = ((close[-11] / close[-20]) - 1) * 100
            flag_volatility = np.std(close[-10:]) / close[-10] * 100
            
            if pole_return > 10 and flag_volatility < 3:
                patterns_found.append({
                    'pattern': 'Bull Flag',
                    'type': 'Bullish',
                    'confidence': 75,
                    'target': float(close[-1] * (1 + pole_return/100)),
                    'description': 'Strong continuation pattern'
                })
        
        return {
            "patterns": patterns_found,
            "total": len(patterns_found),
            "has_bullish": any(p['type'] == 'Bullish' for p in patterns_found),
            "has_bearish": any(p['type'] == 'Bearish' for p in patterns_found)
        }
    
    # ============= 12. STATISTICAL DASHBOARD =============
    
    @staticmethod
    def statistical_analysis(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Análise estatística completa
        """
        returns = data['Close'].pct_change().dropna() * 100
        
        # Estatísticas básicas
        mean_return = returns.mean()
        median_return = returns.median()
        std_return = returns.std()
        
        # Skewness e Kurtosis
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        # Value at Risk (VaR)
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)
        
        # Máximo e mínimo
        max_return = returns.max()
        min_return = returns.min()
        
        # Distribuição de retornos
        positive_days = (returns > 0).sum()
        negative_days = (returns < 0).sum()
        win_rate = positive_days / len(returns) * 100
        
        # Histograma
        hist, bin_edges = np.histogram(returns, bins=20)
        histogram_data = [
            {"range": f"{bin_edges[i]:.1f} to {bin_edges[i+1]:.1f}", "count": int(hist[i])}
            for i in range(len(hist))
        ]
        
        return {
            "mean_return": round(float(mean_return), 3),
            "median_return": round(float(median_return), 3),
            "std_deviation": round(float(std_return), 3),
            "skewness": round(float(skewness), 3),
            "kurtosis": round(float(kurtosis), 3),
            "var_95": round(float(var_95), 3),
            "var_99": round(float(var_99), 3),
            "max_return": round(float(max_return), 2),
            "min_return": round(float(min_return), 2),
            "positive_days": int(positive_days),
            "negative_days": int(negative_days),
            "win_rate": round(float(win_rate), 1),
            "histogram": histogram_data,
            "interpretation": {
                "skewness": "Right-skewed (more gains)" if skewness > 0 else "Left-skewed (more losses)",
                "kurtosis": "Fat tails (extreme events)" if kurtosis > 3 else "Normal distribution"
            }
        }
    
    # ============= 13. ANOMALY DETECTION =============
    
    @staticmethod
    def detect_anomalies(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detecta anomalias de mercado
        """
        anomalies = []
        
        returns = data['Close'].pct_change() * 100
        volume = data['Volume']
        
        # Z-scores
        return_mean = returns.mean()
        return_std = returns.std()
        volume_mean = volume.mean()
        volume_std = volume.std()
        
        for i in range(len(data)):
            date = data.index[i]
            anomaly_score = 0
            reasons = []
            
            # Anomalia de retorno
            if abs(returns.iloc[i]) > return_mean + 3 * return_std:
                anomaly_score += 40
                reasons.append(f"Extreme price movement: {returns.iloc[i]:.1f}%")
            
            # Anomalia de volume
            if volume.iloc[i] > volume_mean + 3 * volume_std:
                anomaly_score += 30
                reasons.append(f"Abnormal volume: {volume.iloc[i]/volume_mean:.1f}x average")
            
            # Gap
            if i > 0:
                gap = ((data['Open'].iloc[i] - data['Close'].iloc[i-1]) / data['Close'].iloc[i-1]) * 100
                if abs(gap) > 3:
                    anomaly_score += 30
                    reasons.append(f"Significant gap: {gap:.1f}%")
            
            if anomaly_score >= 50:
                anomalies.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'score': anomaly_score,
                    'price': float(data['Close'].iloc[i]),
                    'change': round(float(returns.iloc[i]), 2),
                    'volume': int(volume.iloc[i]),
                    'reasons': reasons
                })
        
        # Últimas 20 anomalias
        anomalies = sorted(anomalies, key=lambda x: x['date'], reverse=True)[:20]
        
        return {
            "anomalies": anomalies,
            "total": len(anomalies),
            "recent_count": len([a for a in anomalies if pd.to_datetime(a['date']) > pd.Timestamp.now() - pd.Timedelta(days=30)])
        }
    
    # ============= 14. MULTI-INDICATOR CONSENSUS =============
    
    @staticmethod
    def multi_indicator_consensus(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Sistema de votação com múltiplos indicadores
        """
        votes = {'BUY': 0, 'SELL': 0, 'NEUTRAL': 0}
        signals = []
        
        current_price = data['Close'].iloc[-1]
        
        # RSI
        if 'RSI' in data.columns:
            rsi = data['RSI'].iloc[-1]
            if rsi < 30:
                votes['BUY'] += 1
                signals.append({'indicator': 'RSI', 'signal': 'BUY', 'value': round(float(rsi), 1)})
            elif rsi > 70:
                votes['SELL'] += 1
                signals.append({'indicator': 'RSI', 'signal': 'SELL', 'value': round(float(rsi), 1)})
            else:
                votes['NEUTRAL'] += 1
                signals.append({'indicator': 'RSI', 'signal': 'NEUTRAL', 'value': round(float(rsi), 1)})
        
        # MACD
        if 'MACD' in data.columns and 'Signal' in data.columns:
            macd = data['MACD'].iloc[-1]
            signal = data['Signal'].iloc[-1]
            if macd > signal and data['MACD'].iloc[-2] <= data['Signal'].iloc[-2]:
                votes['BUY'] += 1
                signals.append({'indicator': 'MACD', 'signal': 'BUY', 'value': 'Bullish Cross'})
            elif macd < signal and data['MACD'].iloc[-2] >= data['Signal'].iloc[-2]:
                votes['SELL'] += 1
                signals.append({'indicator': 'MACD', 'signal': 'SELL', 'value': 'Bearish Cross'})
            else:
                votes['NEUTRAL'] += 1
                signals.append({'indicator': 'MACD', 'signal': 'NEUTRAL', 'value': 'No Cross'})
        
        # SMAs
        if 'SMA_20' in data.columns and 'SMA_50' in data.columns:
            sma20 = data['SMA_20'].iloc[-1]
            sma50 = data['SMA_50'].iloc[-1]
            
            if current_price > sma20 > sma50:
                votes['BUY'] += 2  # Peso maior
                signals.append({'indicator': 'SMA', 'signal': 'BUY', 'value': 'Price > SMA20 > SMA50'})
            elif current_price < sma20 < sma50:
                votes['SELL'] += 2
                signals.append({'indicator': 'SMA', 'signal': 'SELL', 'value': 'Price < SMA20 < SMA50'})
            else:
                votes['NEUTRAL'] += 1
                signals.append({'indicator': 'SMA', 'signal': 'NEUTRAL', 'value': 'Mixed signals'})
        
        # Bollinger Bands
        if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
            bb_upper = data['BB_Upper'].iloc[-1]
            bb_lower = data['BB_Lower'].iloc[-1]
            
            if current_price <= bb_lower:
                votes['BUY'] += 1
                signals.append({'indicator': 'Bollinger', 'signal': 'BUY', 'value': 'At lower band'})
            elif current_price >= bb_upper:
                votes['SELL'] += 1
                signals.append({'indicator': 'Bollinger', 'signal': 'SELL', 'value': 'At upper band'})
            else:
                votes['NEUTRAL'] += 1
                signals.append({'indicator': 'Bollinger', 'signal': 'NEUTRAL', 'value': 'Within bands'})
        
        # Volume
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
        current_volume = data['Volume'].iloc[-1]
        if current_volume > avg_volume * 1.5:
            # Volume confirma a direção do preço
            if data['Close'].iloc[-1] > data['Close'].iloc[-2]:
                votes['BUY'] += 1
                signals.append({'indicator': 'Volume', 'signal': 'BUY', 'value': 'High volume + up'})
            else:
                votes['SELL'] += 1
                signals.append({'indicator': 'Volume', 'signal': 'SELL', 'value': 'High volume + down'})
        
        # Calcula score
        total_votes = sum(votes.values())
        if total_votes > 0:
            buy_percent = (votes['BUY'] / total_votes) * 100
            sell_percent = (votes['SELL'] / total_votes) * 100
            score = buy_percent - sell_percent  # -100 a +100
        else:
            score = 0
        
        # Recomendação
        if score > 40:
            recommendation = "STRONG BUY"
        elif score > 15:
            recommendation = "BUY"
        elif score > -15:
            recommendation = "HOLD"
        elif score > -40:
            recommendation = "SELL"
        else:
            recommendation = "STRONG SELL"
        
        return {
            "votes": votes,
            "score": round(score, 1),
            "recommendation": recommendation,
            "signals": signals,
            "total_indicators": len(signals),
            "strength": "STRONG" if abs(score) > 40 else "MODERATE" if abs(score) > 15 else "WEAK"
        }
    
    # ============= 15. WATCHLIST COMPARISON =============
    
    @staticmethod
    def compare_watchlist(stocks_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """
        Compara múltiplas cryptos
        """
        comparison = []
        
        for ticker, data in stocks_data.items():
            if len(data) < 20:
                continue
            
            current_price = data['Close'].iloc[-1]
            rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns else 50
            
            # MACD
            if 'MACD' in data.columns and 'Signal' in data.columns:
                macd_signal = '↑' if data['MACD'].iloc[-1] > data['Signal'].iloc[-1] else '↓'
            else:
                macd_signal = '-'
            
            # Momentum
            if len(data) >= 20:
                momentum = ((current_price / data['Close'].iloc[-20]) - 1) * 100
            else:
                momentum = 0
            
            # Volume
            avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
            current_volume = data['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            volume_class = 'High' if volume_ratio > 1.5 else 'Med' if volume_ratio > 0.8 else 'Low'
            
            # Score técnico (simplificado)
            score = 50
            if rsi < 30:
                score += 20
            elif rsi > 70:
                score -= 20
            if macd_signal == '↑':
                score += 15
            elif macd_signal == '↓':
                score -= 15
            if momentum > 0:
                score += 15
            else:
                score -= 15
            
            comparison.append({
                'ticker': ticker,
                'price': round(float(current_price), 2),
                'rsi': round(float(rsi), 1),
                'macd_signal': macd_signal,
                'momentum': round(float(momentum), 2),
                'volume': volume_class,
                'score': max(0, min(100, score))
            })
        
        # Ordena por score
        comparison = sorted(comparison, key=lambda x: x['score'], reverse=True)
        
        return comparison
    
    # ============= 16. VISUAL TRADE PLANNER =============
    
    @staticmethod
    def trade_planner(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Plano visual de trade
        """
        if len(data) < 20:
            return {"error": "Insufficient data"}
        
        current_price = data['Close'].iloc[-1]
        
        # Encontra suporte e resistência recentes
        recent_low = data['Low'].iloc[-20:].min()
        recent_high = data['High'].iloc[-20:].max()
        
        # Calcula ATR para stop loss
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        atr = true_range.rolling(14).mean().iloc[-1]
        
        # Determina direção baseado em tendência
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(50).mean().iloc[-1] if len(data) >= 50 else sma_20
        
        if sma_20 > sma_50:
            # Bullish setup
            entry_zone_low = recent_low * 1.01
            entry_zone_high = current_price
            stop_loss = recent_low * 0.98
            target_1 = current_price + (current_price - stop_loss) * 1.5
            target_2 = current_price + (current_price - stop_loss) * 2.5
            direction = "LONG"
        else:
            # Bearish setup
            entry_zone_high = recent_high * 0.99
            entry_zone_low = current_price
            stop_loss = recent_high * 1.02
            target_1 = current_price - (stop_loss - current_price) * 1.5
            target_2 = current_price - (stop_loss - current_price) * 2.5
            direction = "SHORT"
        
        risk = abs(current_price - stop_loss)
        reward_1 = abs(target_1 - current_price)
        reward_2 = abs(target_2 - current_price)
        
        return {
            "direction": direction,
            "current_price": round(float(current_price), 2),
            "entry_zone": {
                "low": round(float(entry_zone_low), 2),
                "high": round(float(entry_zone_high), 2)
            },
            "stop_loss": round(float(stop_loss), 2),
            "targets": {
                "target_1": round(float(target_1), 2),
                "target_2": round(float(target_2), 2)
            },
            "risk": round(float(risk), 2),
            "reward_1": round(float(reward_1), 2),
            "reward_2": round(float(reward_2), 2),
            "risk_reward_1": round(reward_1 / risk, 2) if risk > 0 else 0,
            "risk_reward_2": round(reward_2 / risk, 2) if risk > 0 else 0,
            "atr": round(float(atr), 2)
        }
    
    # ============= 17. FAST MOVERS ALERT =============
    
    @staticmethod
    def fast_movers_scanner(stocks_data: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """
        Identifica cryptos com movimento rápido
        """
        movers = []
        
        for ticker, data in stocks_data.items():
            if len(data) < 20:
                continue
            
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2]
            
            # Mudança 24h
            change_24h = ((current_price - prev_price) / prev_price) * 100
            
            # Volume vs média
            avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
            current_volume = data['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Momentum
            if len(data) >= 5:
                momentum_5d = ((current_price / data['Close'].iloc[-5]) - 1) * 100
            else:
                momentum_5d = 0
            
            # Critérios para "fast mover"
            if abs(change_24h) >= 5 and volume_ratio >= 1.5:
                movers.append({
                    'ticker': ticker,
                    'price': round(float(current_price), 2),
                    'change_24h': round(float(change_24h), 2),
                    'volume_ratio': round(float(volume_ratio), 2),
                    'momentum_5d': round(float(momentum_5d), 2),
                    'alert_level': 'HIGH' if abs(change_24h) >= 10 else 'MEDIUM'
                })
        
        # Ordena por mudança absoluta
        movers = sorted(movers, key=lambda x: abs(x['change_24h']), reverse=True)
        
        return movers[:10]  # Top 10
    
    # ============= 18. DCA SIMULATOR =============
    
    @staticmethod
    def dca_simulator(data: pd.DataFrame, monthly_investment: float = 100, months: int = 12) -> Dict[str, Any]:
        """
        Simula estratégia de Dollar-Cost Averaging
        """
        if len(data) < months * 21:  # ~21 dias de trading por mês
            return {"error": "Insufficient data for simulation"}
        
        # Simula compras mensais
        investment_dates = []
        total_invested = 0
        total_units = 0
        
        for i in range(months):
            # Índice da compra (primeiro dia de cada mês)
            idx = -(months - i) * 21
            if idx >= -len(data):
                price = data['Close'].iloc[idx]
                units = monthly_investment / price
                total_units += units
                total_invested += monthly_investment
                
                investment_dates.append({
                    'date': data.index[idx].strftime('%Y-%m-%d'),
                    'price': round(float(price), 2),
                    'units_bought': round(float(units), 6),
                    'invested': monthly_investment
                })
        
        # Valor atual
        current_price = data['Close'].iloc[-1]
        current_value = total_units * current_price
        profit = current_value - total_invested
        return_pct = (profit / total_invested) * 100 if total_invested > 0 else 0
        
        # Compara com lump sum
        first_price = data['Close'].iloc[-months * 21]
        lump_sum_units = total_invested / first_price
        lump_sum_value = lump_sum_units * current_price
        lump_sum_return = ((lump_sum_value - total_invested) / total_invested) * 100
        
        return {
            "total_invested": round(total_invested, 2),
            "current_value": round(float(current_value), 2),
            "profit": round(float(profit), 2),
            "return_percent": round(return_pct, 2),
            "avg_price": round(total_invested / total_units, 2) if total_units > 0 else 0,
            "total_units": round(float(total_units), 6),
            "investments": investment_dates,
            "lump_sum_comparison": {
                "lump_sum_return": round(lump_sum_return, 2),
                "difference": round(return_pct - lump_sum_return, 2),
                "better_strategy": "DCA" if return_pct > lump_sum_return else "Lump Sum"
            }
        }
    
    # ============= 19. ENTRY CONFIRMATION CHECKLIST =============
    
    @staticmethod
    def entry_checklist(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Checklist antes de entrar em trade
        """
        checks = []
        score = 0
        total = 0
        
        current_price = data['Close'].iloc[-1]
        
        # 1. Tendência
        if len(data) >= 50:
            sma_20 = data['Close'].rolling(20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(50).mean().iloc[-1]
            
            if sma_20 > sma_50:
                checks.append({'check': 'Trend', 'status': 'PASS', 'detail': 'Bullish (SMA20 > SMA50)'})
                score += 1
            else:
                checks.append({'check': 'Trend', 'status': 'FAIL', 'detail': 'Bearish (SMA20 < SMA50)'})
            total += 1
        
        # 2. Momentum
        if len(data) >= 20:
            momentum = ((current_price / data['Close'].iloc[-20]) - 1) * 100
            if momentum > 0:
                checks.append({'check': 'Momentum', 'status': 'PASS', 'detail': f'Positive (+{momentum:.1f}%)'})
                score += 1
            else:
                checks.append({'check': 'Momentum', 'status': 'FAIL', 'detail': f'Negative ({momentum:.1f}%)'})
            total += 1
        
        # 3. Volume
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
        current_volume = data['Volume'].iloc[-1]
        if current_volume > avg_volume:
            checks.append({'check': 'Volume', 'status': 'PASS', 'detail': 'Above average'})
            score += 1
        else:
            checks.append({'check': 'Volume', 'status': 'WARNING', 'detail': 'Below average'})
        total += 1
        
        # 4. RSI
        if 'RSI' in data.columns:
            rsi = data['RSI'].iloc[-1]
            if 30 < rsi < 70:
                checks.append({'check': 'RSI', 'status': 'PASS', 'detail': f'Neutral ({rsi:.1f})'})
                score += 1
            elif rsi >= 70:
                checks.append({'check': 'RSI', 'status': 'WARNING', 'detail': f'Overbought ({rsi:.1f})'})
            else:
                checks.append({'check': 'RSI', 'status': 'WARNING', 'detail': f'Oversold ({rsi:.1f})'})
            total += 1
        
        # 5. Suporte próximo
        recent_low = data['Low'].iloc[-20:].min()
        distance_to_support = ((current_price - recent_low) / current_price) * 100
        if distance_to_support < 10:
            checks.append({'check': 'Support', 'status': 'PASS', 'detail': f'Nearby at ${recent_low:.2f} (-{distance_to_support:.1f}%)'})
            score += 1
        else:
            checks.append({'check': 'Support', 'status': 'WARNING', 'detail': f'Far at ${recent_low:.2f} (-{distance_to_support:.1f}%)'})
        total += 1
        
        # 6. Resistência
        recent_high = data['High'].iloc[-20:].max()
        distance_to_resistance = ((recent_high - current_price) / current_price) * 100
        if distance_to_resistance > 5:
            checks.append({'check': 'Resistance', 'status': 'PASS', 'detail': f'Clear room to ${recent_high:.2f} (+{distance_to_resistance:.1f}%)'})
            score += 1
        else:
            checks.append({'check': 'Resistance', 'status': 'FAIL', 'detail': f'Too close at ${recent_high:.2f} (+{distance_to_resistance:.1f}%)'})
        total += 1
        
        # Decisão final
        score_percent = (score / total) * 100 if total > 0 else 0
        
        if score_percent >= 70:
            decision = "GO"
            confidence = "HIGH"
        elif score_percent >= 50:
            decision = "GO WITH CAUTION"
            confidence = "MODERATE"
        else:
            decision = "NO GO"
            confidence = "LOW"
        
        return {
            "checks": checks,
            "score": f"{score}/{total}",
            "score_percent": round(score_percent, 1),
            "decision": decision,
            "confidence": confidence
        }
    
    # ============= 20. FIBONACCI TIME ZONES =============
    
    @staticmethod
    def fibonacci_time_zones(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Projeção temporal de Fibonacci
        """
        if len(data) < 60:
            return {"error": "Insufficient data"}
        
        # Encontra último swing low significativo
        lows = data['Low'].values
        swing_low_idx = None
        swing_low_price = float('inf')
        
        for i in range(len(data) - 40, len(data) - 10):
            if lows[i] == min(lows[max(0, i-10):min(len(lows), i+10)]):
                swing_low_idx = i
                swing_low_price = lows[i]
                break
        
        if swing_low_idx is None:
            return {"error": "No significant swing low found"}
        
        # Dias desde o swing low
        days_since = len(data) - swing_low_idx - 1
        
        # Níveis de Fibonacci (dias)
        fib_days = [8, 13, 21, 34, 55, 89, 144]
        
        time_zones = []
        for fib in fib_days:
            target_idx = swing_low_idx + fib
            
            if target_idx < len(data):
                # Evento já aconteceu
                actual_date = data.index[target_idx]
                actual_price = data['Close'].iloc[target_idx]
                status = "PAST"
                
                time_zones.append({
                    'fib_days': fib,
                    'target_date': actual_date.strftime('%Y-%m-%d'),
                    'actual_price': round(float(actual_price), 2),
                    'status': status,
                    'significant_move': bool(abs((actual_price - swing_low_price) / swing_low_price) > 0.05)
                })
            else:
                # Projeção futura
                days_ahead = target_idx - len(data) + 1
                projected_date = data.index[-1] + pd.Timedelta(days=days_ahead)
                status = "FUTURE"
                
                time_zones.append({
                    'fib_days': fib,
                    'target_date': projected_date.strftime('%Y-%m-%d'),
                    'days_ahead': days_ahead,
                    'status': status,
                    'note': 'Potential turning point'
                })
        
        return {
            "swing_low_date": data.index[swing_low_idx].strftime('%Y-%m-%d'),
            "swing_low_price": round(float(swing_low_price), 2),
            "days_since_low": days_since,
            "time_zones": time_zones,
            "next_important_date": next((tz['target_date'] for tz in time_zones if tz['status'] == 'FUTURE'), None)
        }


# Singleton instance
advanced_analysis_service = AdvancedAnalysisService()
