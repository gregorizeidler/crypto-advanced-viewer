"""
Data Service for Cryptocurrency Market
Fetches and processes crypto data from various sources
"""

from __future__ import annotations

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from .technical_analysis_advanced import TechnicalAnalysisAdvanced, StockComparator

logger = logging.getLogger(__name__)


class CryptoDataService:
    """Service to fetch cryptocurrency data"""
    
    # Major cryptocurrencies available on Yahoo Finance (100+ cryptos)
    MAIN_CRYPTOS = [
        # Top 10 by Market Cap
        'BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'SOL-USD',
        'XRP-USD', 'USDC-USD', 'ADA-USD', 'DOGE-USD', 'TRX-USD',
        
        # Top 11-30
        'AVAX-USD', 'LINK-USD', 'DOT-USD', 'MATIC-USD', 'SHIB-USD',
        'LTC-USD', 'BCH-USD', 'UNI-USD', 'ATOM-USD', 'XLM-USD',
        'ETC-USD', 'FIL-USD', 'APT-USD', 'HBAR-USD', 'NEAR-USD',
        'VET-USD', 'ICP-USD', 'ARB-USD', 'MKR-USD', 'GRT-USD',
        
        # Top 31-60
        'ALGO-USD', 'AAVE-USD', 'FTM-USD', 'SAND-USD', 'MANA-USD',
        'XTZ-USD', 'THETA-USD', 'AXS-USD', 'EOS-USD', 'ZEC-USD',
        'XMR-USD', 'EGLD-USD', 'FLOW-USD', 'CHZ-USD', 'ENJ-USD',
        'COMP-USD', 'SNX-USD', 'BAT-USD', 'ZIL-USD', 'DASH-USD',
        'YFI-USD', 'SUSHI-USD', 'CRV-USD', 'ONE-USD', 'KAVA-USD',
        'RVN-USD', 'QTUM-USD', 'ZRX-USD', 'OMG-USD', 'ICX-USD',
        
        # Top 61-100
        'BNT-USD', 'WAVES-USD', 'SC-USD', 'IOST-USD', 'LSK-USD',
        'ONT-USD', 'IOTA-USD', 'BTG-USD', 'DGB-USD', 'DCR-USD',
        'REP-USD', 'STEEM-USD', 'STORJ-USD', 'KNC-USD', 'REN-USD',
        'BAND-USD', 'BLZ-USD', 'ANT-USD', 'KSM-USD', 'CELO-USD',
        
        # Popular Memecoins & Others
        'PEPE-USD', 'FLOKI-USD', 'BONK-USD', 'WIF-USD',
        
        # Layer 2 & Scaling Solutions
        'OP-USD', 'IMX-USD', 'LRC-USD',
        
        # DeFi Tokens
        'INJ-USD', 'RUNE-USD', 'BAL-USD', '1INCH-USD',
        
        # Stablecoins (for comparison)
        'DAI-USD', 'TUSD-USD', 'BUSD-USD',
        
        # Gaming & Metaverse
        'GALA-USD', 'IMX-USD',
        
        # Infrastructure & Oracles
        'FET-USD', 'OCEAN-USD', 'ROSE-USD',
    ]
    
    CATEGORIES = {
        'Layer 1 Blockchains': ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'DOT-USD', 'AVAX-USD', 'NEAR-USD', 'ATOM-USD'],
        'DeFi': ['UNI-USD', 'AAVE-USD', 'LINK-USD', 'MKR-USD', 'SNX-USD', 'COMP-USD', 'SUSHI-USD', 'CRV-USD'],
        'Memecoins': ['DOGE-USD', 'SHIB-USD', 'PEPE-USD', 'FLOKI-USD', 'BONK-USD', 'WIF-USD'],
        'Layer 2 & Scaling': ['MATIC-USD', 'OP-USD', 'ARB-USD', 'IMX-USD', 'LRC-USD'],
        'Exchange Tokens': ['BNB-USD', 'UNI-USD', 'FTT-USD'],
        'Stablecoins': ['USDT-USD', 'USDC-USD', 'DAI-USD', 'BUSD-USD', 'TUSD-USD'],
        'Gaming & Metaverse': ['SAND-USD', 'MANA-USD', 'AXS-USD', 'GALA-USD', 'ENJ-USD', 'CHZ-USD'],
        'Storage & Infrastructure': ['FIL-USD', 'STORJ-USD', 'AR-USD', 'THETA-USD'],
        'Privacy Coins': ['XMR-USD', 'ZEC-USD', 'DASH-USD'],
        'Smart Contract Platforms': ['ETH-USD', 'ADA-USD', 'SOL-USD', 'AVAX-USD', 'NEAR-USD', 'ATOM-USD', 'FTM-USD'],
        'Enterprise Blockchain': ['VET-USD', 'HBAR-USD', 'ALGO-USD', 'XLM-USD'],
    }
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
        
    def fetch_crypto_data(self, ticker: str, period: str = '1y') -> pd.DataFrame:
        """
        Fetch historical cryptocurrency data
        
        Args:
            ticker: Crypto ticker (e.g., 'BTC-USD')
            period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        """
        try:
            crypto = yf.Ticker(ticker)
            data = crypto.history(period=period)
            
            if data.empty:
                logger.warning(f"No data for {ticker}")
                return pd.DataFrame()
            
            # Add technical indicators
            data = self._calculate_indicators(data)
            
            return data
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            return pd.DataFrame()
    
    def fetch_crypto_info(self, ticker: str) -> Dict[str, Any]:
        """Fetch detailed cryptocurrency information"""
        try:
            crypto = yf.Ticker(ticker)
            info = crypto.info
            
            # Get crypto name without -USD suffix
            crypto_name = ticker.replace('-USD', '')
            name_map = {
                'BTC': 'Bitcoin',
                'ETH': 'Ethereum',
                'USDT': 'Tether',
                'BNB': 'Binance Coin',
                'SOL': 'Solana',
                'XRP': 'Ripple',
                'USDC': 'USD Coin',
                'ADA': 'Cardano',
                'DOGE': 'Dogecoin',
                'TRX': 'TRON',
                'AVAX': 'Avalanche',
                'LINK': 'Chainlink',
                'DOT': 'Polkadot',
                'MATIC': 'Polygon',
                'SHIB': 'Shiba Inu',
                'LTC': 'Litecoin',
                'BCH': 'Bitcoin Cash',
                'UNI': 'Uniswap',
                'ATOM': 'Cosmos',
                'XLM': 'Stellar',
            }
            
            return {
                'ticker': ticker,
                'name': name_map.get(crypto_name, info.get('longName', crypto_name)),
                'sector': self._get_crypto_category(ticker),
                'current_price': info.get('regularMarketPrice', info.get('currentPrice', 0)),
                'day_change': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', info.get('regularMarketVolume', 0)),
                'market_cap': info.get('marketCap', 0),
                'circulating_supply': info.get('circulatingSupply', 0),
                'total_supply': info.get('totalSupply', 0),
                'week_52_low': info.get('fiftyTwoWeekLow', 0),
                'week_52_high': info.get('fiftyTwoWeekHigh', 0),
                'avg_volume': info.get('averageVolume', info.get('averageVolume10days', 0)),
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return {'ticker': ticker, 'name': ticker, 'error': str(e)}
    
    def _get_crypto_category(self, ticker: str) -> str:
        """Get category for a cryptocurrency"""
        for category, tickers in self.CATEGORIES.items():
            if ticker in tickers:
                return category
        return 'Other'
    
    def fetch_realtime_quotes(self, tickers: List[str]) -> pd.DataFrame:
        """Fetch real-time quotes for multiple cryptocurrencies"""
        try:
            data = yf.download(tickers, period='1d', interval='1m', progress=False)
            return data
        except Exception as e:
            logger.error(f"Error fetching quotes: {e}")
            return pd.DataFrame()
    
    def fetch_bitcoin_index(self, period: str = '1y') -> pd.DataFrame:
        """Fetch Bitcoin (BTC) index data as main reference"""
        try:
            btc = yf.Ticker('BTC-USD')
            data = btc.history(period=period)
            return data
        except Exception as e:
            logger.error(f"Error fetching Bitcoin: {e}")
            return pd.DataFrame()
    
    def fetch_category_performance(self) -> Dict[str, float]:
        """Fetch category performance"""
        category_performance = {}
        
        for category, tickers in self.CATEGORIES.items():
            try:
                changes = []
                for ticker in tickers[:3]:  # Top 3 from each category
                    info = self.fetch_crypto_info(ticker)
                    if 'day_change' in info and info['day_change'] is not None:
                        changes.append(info['day_change'])
                
                if changes:
                    category_performance[category] = np.mean(changes)
            except Exception as e:
                logger.error(f"Error processing category {category}: {e}")
        
        return category_performance
    
    def _calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        try:
            # RSI (Relative Strength Index)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # Moving Averages
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['SMA_200'] = data['Close'].rolling(window=200).mean()
            
            # MACD
            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
            data['MACD_Histogram'] = data['MACD'] - data['Signal']
            
            # Bollinger Bands
            data['BB_Middle'] = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            data['BB_Upper'] = data['BB_Middle'] + (std * 2)
            data['BB_Lower'] = data['BB_Middle'] - (std * 2)
            
            # Volatility (crypto markets are 24/7, so adjusted calculation)
            data['Volatility'] = data['Close'].pct_change().rolling(window=20).std() * np.sqrt(365) * 100
            
            # Average Volume
            data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
            
            # Advanced Indicators
            data['VWAP'] = TechnicalAnalysisAdvanced.calculate_vwap(data)
            data['OBV'] = TechnicalAnalysisAdvanced.calculate_obv(data)
            data['MFI'] = TechnicalAnalysisAdvanced.calculate_mfi(data)
            data['Force_Index'] = TechnicalAnalysisAdvanced.calculate_force_index(data)
            data['AD'] = TechnicalAnalysisAdvanced.calculate_accumulation_distribution(data)
            data['ROC'] = TechnicalAnalysisAdvanced.calculate_roc(data)
            data['Momentum'] = TechnicalAnalysisAdvanced.calculate_momentum(data)
            data['ADX'] = TechnicalAnalysisAdvanced.calculate_adx(data)
            
            # Detect Patterns
            data['Doji'] = TechnicalAnalysisAdvanced.detect_doji(data)
            data['Hammer'] = TechnicalAnalysisAdvanced.detect_hammer(data)
            data['Bullish_Engulfing'] = TechnicalAnalysisAdvanced.detect_bullish_engulfing(data)
            data['Bearish_Engulfing'] = TechnicalAnalysisAdvanced.detect_bearish_engulfing(data)
            
            return data
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return data
    
    def get_main_cryptos(self) -> List[Dict[str, Any]]:
        """Return list of main cryptocurrencies with basic information"""
        cryptos = []
        for ticker in self.MAIN_CRYPTOS[:20]:  # Top 20
            try:
                info = self.fetch_crypto_info(ticker)
                cryptos.append(info)
            except Exception as e:
                logger.error(f"Error fetching {ticker}: {e}")
        
        return cryptos
    
    def fetch_change_ranking(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return cryptocurrency ranking by daily change (half gainers, half losers)"""
        from .cache_service import cache_service
        
        # CACHE: avoid fetching 100+ cryptos every time (2 minutes)
        cache_key = f"crypto_ranking_raw_{limit}"
        cached = cache_service.get(cache_key)
        if cached:
            logger.info("🚀 Crypto Ranking returned from CACHE!")
            return cached
        
        logger.info(f"⏳ Fetching {len(self.MAIN_CRYPTOS)} cryptocurrencies (will take ~60s)...")
        cryptos = []
        for ticker in self.MAIN_CRYPTOS:
            try:
                info = self.fetch_crypto_info(ticker)
                if 'day_change' in info and info['day_change'] is not None:
                    cryptos.append(info)
            except Exception as e:
                logger.error(f"Error fetching {ticker}: {e}")
        
        # Sort by change (highest to lowest)
        sorted_cryptos = sorted(cryptos, key=lambda x: x.get('day_change', 0), reverse=True)
        
        # Get half top gainers and half top losers
        half = limit // 2
        top_gainers = sorted_cryptos[:half]
        top_losers = sorted_cryptos[-half:]
        top_losers.reverse()  # Reverse to show from highest loss to lowest
        
        # Combine: gainers first, then losers
        result = top_gainers + top_losers
        
        # Cache for 2 minutes
        cache_service.set(cache_key, result, ttl_seconds=120)
        logger.info(f"✅ Crypto Ranking of {len(result)} cryptos cached!")
        
        return result
    
    def calculate_correlations(self, tickers: List[str], period: str = '6mo') -> pd.DataFrame:
        """Calculate correlation matrix between cryptocurrencies"""
        try:
            data = yf.download(tickers, period=period, progress=False)['Close']
            
            if isinstance(data, pd.Series):
                return pd.DataFrame()
            
            returns = data.pct_change().dropna()
            correlations = returns.corr()
            
            return correlations
        except Exception as e:
            logger.error(f"Error calculating correlations: {e}")
            return pd.DataFrame()


# Global instance
crypto_service = CryptoDataService()

