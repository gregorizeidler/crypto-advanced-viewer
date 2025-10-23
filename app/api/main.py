"""
Main API - Crypto Viewer
Advanced Cryptocurrency Visualization System
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from app.services.paper_trading_service import paper_trading_service

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crypto Viewer API",
    description="Advanced Cryptocurrency Visualization System",
    version="2.0.0",
)

# CORS - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Start application."""
    logger.info("🚀 Crypto Viewer API started")
    logger.info("📊 Server ready to receive requests")


@app.get("/")
def root():
    return {
        "message": "Crypto Viewer - Cryptocurrency Market API",
        "status": "active",
        "version": "2.0.0",
        "market": "Cryptocurrency Market - 100+ Cryptos"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Crypto Viewer API"
    }


# ============= Cryptocurrency Specific Endpoints =============

@app.get("/api/crypto/assets/main")
@app.get("/api/sp500/stocks/main")  # Keep for backwards compatibility
def get_main_cryptos():
    """Returns main cryptocurrencies with real-time data."""
    from ..services.crypto_data_service import crypto_service
    from ..services.cache_service import cache_service
    
    # Cache for 3 minutes
    cache_key = "main_cryptos"
    cached = cache_service.get(cache_key)
    if cached:
        return cached
    
    cryptos = crypto_service.get_main_cryptos()
    result = {
        "stocks": cryptos,  # Keep "stocks" key for compatibility
        "total": len(cryptos),
        "market": "Cryptocurrency",
        "timestamp": datetime.now().isoformat(),
    }
    
    cache_service.set(cache_key, result, ttl_seconds=180)
    return result


@app.get("/api/crypto/asset/{ticker}")
@app.get("/api/sp500/stock/{ticker}")  # Keep for backwards compatibility
def get_crypto_data(
    ticker: str,
    period: str = Query(default="1y", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$")
):
    """Returns complete historical data for a cryptocurrency."""
    from ..services.crypto_data_service import crypto_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    info = crypto_service.fetch_crypto_info(ticker)
    
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    # Convert to JSON format
    data_json = []
    for idx, row in data.iterrows():
        data_json.append({
            "date": idx.strftime("%Y-%m-%d"),
            "open": float(row['Open']) if pd.notna(row['Open']) else None,
            "high": float(row['High']) if pd.notna(row['High']) else None,
            "low": float(row['Low']) if pd.notna(row['Low']) else None,
            "close": float(row['Close']) if pd.notna(row['Close']) else None,
            "volume": int(row['Volume']) if pd.notna(row['Volume']) else None,
            "rsi": float(row['RSI']) if 'RSI' in row and pd.notna(row['RSI']) else None,
            "sma_20": float(row['SMA_20']) if 'SMA_20' in row and pd.notna(row['SMA_20']) else None,
            "sma_50": float(row['SMA_50']) if 'SMA_50' in row and pd.notna(row['SMA_50']) else None,
            "sma_200": float(row['SMA_200']) if 'SMA_200' in row and pd.notna(row['SMA_200']) else None,
            "macd": float(row['MACD']) if 'MACD' in row and pd.notna(row['MACD']) else None,
            "macd_signal": float(row['Signal']) if 'Signal' in row and pd.notna(row['Signal']) else None,
            "bb_upper": float(row['BB_Upper']) if 'BB_Upper' in row and pd.notna(row['BB_Upper']) else None,
            "bb_middle": float(row['BB_Middle']) if 'BB_Middle' in row and pd.notna(row['BB_Middle']) else None,
            "bb_lower": float(row['BB_Lower']) if 'BB_Lower' in row and pd.notna(row['BB_Lower']) else None,
            "volatility": float(row['Volatility']) if 'Volatility' in row and pd.notna(row['Volatility']) else None,
        })
    
    return {
        "ticker": ticker,
        "info": info,
        "data": data_json,
        "period": period,
        "total_records": len(data_json),
    }


@app.get("/api/crypto/bitcoin")
@app.get("/api/sp500/index")  # Keep for backwards compatibility
def get_bitcoin_index(period: str = Query(default="1y")):
    """Returns historical data for Bitcoin (main crypto index)."""
    from ..services.crypto_data_service import crypto_service
    from ..services.cache_service import cache_service
    
    # Cache for 5 minutes by period
    cache_key = f"bitcoin_index_{period}"
    cached = cache_service.get(cache_key)
    if cached:
        return cached
    
    data = crypto_service.fetch_bitcoin_index(period)
    
    if data.empty:
        raise HTTPException(status_code=404, detail="Bitcoin data not available")
    
    data_json = []
    for idx, row in data.iterrows():
        data_json.append({
            "date": idx.strftime("%Y-%m-%d"),
            "close": float(row['Close']),
            "volume": int(row['Volume']) if pd.notna(row['Volume']) else 0,
        })
    
    # Calculate variation
    day_change = 0
    period_change = 0
    if len(data_json) >= 2:
        day_change = ((data_json[-1]['close'] / data_json[-2]['close']) - 1) * 100
        period_change = ((data_json[-1]['close'] / data_json[0]['close']) - 1) * 100
    
    result = {
        "index": "Bitcoin (BTC)",
        "data": data_json,
        "day_change": round(day_change, 2),
        "period_change": round(period_change, 2),
        "period": period,
    }
    
    cache_service.set(cache_key, result, ttl_seconds=300)
    return result


@app.get("/api/crypto/categories")
@app.get("/api/sp500/sectors")  # Keep for backwards compatibility
def get_category_performance():
    """Returns performance of crypto categories."""
    from ..services.crypto_data_service import crypto_service
    from ..services.cache_service import cache_service
    
    # Cache for 5 minutes
    cache_key = "categories"
    cached = cache_service.get(cache_key)
    if cached:
        return cached
    
    categories = crypto_service.fetch_category_performance()
    
    sectors_list = [
        {"sector": category, "change": round(change, 2)}
        for category, change in categories.items()
    ]
    
    # Sort by change
    sectors_list = sorted(sectors_list, key=lambda x: x['change'], reverse=True)
    
    result = {
        "sectors": sectors_list,
        "total": len(sectors_list),
        "timestamp": datetime.now().isoformat(),
    }
    
    cache_service.set(cache_key, result, ttl_seconds=300)
    return result


@app.get("/api/crypto/ranking")
@app.get("/api/sp500/ranking")  # Keep for backwards compatibility
def get_crypto_ranking(type: str = Query(default="change", regex="^(change|volume)$")):
    """Returns cryptocurrency ranking by change or volume."""
    from ..services.crypto_data_service import crypto_service
    from ..services.cache_service import cache_service
    
    # Try cache first (2 minutes)
    cache_key = f"ranking_{type}"
    cached = cache_service.get(cache_key)
    if cached:
        return cached
    
    if type == "change":
        ranking = crypto_service.fetch_change_ranking(limit=20)
    else:
        ranking = crypto_service.get_main_cryptos()
        ranking = sorted(ranking, key=lambda x: x.get('volume', 0), reverse=True)[:20]
    
    result = {
        "ranking": ranking,
        "type": type,
        "total": len(ranking),
        "timestamp": datetime.now().isoformat(),
    }
    
    # Cache for 2 minutes
    cache_service.set(cache_key, result, ttl_seconds=120)
    
    return result


@app.get("/api/crypto/correlations")
@app.get("/api/sp500/correlations")  # Keep for backwards compatibility
def get_correlations(
    tickers: str = Query(..., description="Comma-separated tickers (e.g., BTC-USD,ETH-USD,SOL-USD)"),
    period: str = Query(default="6mo")
):
    """Returns correlation matrix between cryptocurrencies with advanced data."""
    from ..services.crypto_data_service import crypto_service
    
    ticker_list = [t.strip() for t in tickers.split(',')]
    
    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 tickers")
    
    correlations = crypto_service.calculate_correlations(ticker_list, period)
    
    if correlations.empty:
        raise HTTPException(status_code=404, detail="Could not calculate correlations")
    
    # Convert to JSON format
    correlations_json = {}
    for ticker1 in correlations.columns:
        correlations_json[ticker1] = {}
        for ticker2 in correlations.columns:
            value = correlations.loc[ticker1, ticker2]
            correlations_json[ticker1][ticker2] = round(float(value), 3) if pd.notna(value) else None
    
    # Create correlation pairs for network graph
    pairs = []
    for i, ticker1 in enumerate(ticker_list):
        for ticker2 in ticker_list[i+1:]:
            if ticker1 in correlations.columns and ticker2 in correlations.columns:
                corr = correlations.loc[ticker1, ticker2]
                if pd.notna(corr):
                    pairs.append({
                        'source': ticker1,
                        'target': ticker2,
                        'correlation': round(float(corr), 3),
                        'strength': abs(float(corr))  # For line thickness
                    })
    
    return {
        "correlations": correlations_json,
        "pairs": pairs,
        "tickers": ticker_list,
        "period": period,
    }


@app.get("/api/crypto/comparison")
@app.get("/api/sp500/comparison")  # Keep for backwards compatibility
def get_crypto_comparison(
    tickers: str = Query(..., description="Comma-separated tickers"),
    period: str = Query(default="1y")
):
    """Compares performance of multiple cryptocurrencies."""
    from ..services.crypto_data_service import crypto_service
    
    ticker_list = [t.strip() for t in tickers.split(',')]
    
    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 tickers for comparison")
    
    comparison = {}
    
    for ticker in ticker_list:
        data = crypto_service.fetch_crypto_data(ticker, period)
        if not data.empty:
            # Normalize prices (base 100)
            normalized_prices = (data['Close'] / data['Close'].iloc[0]) * 100
            
            comparison[ticker] = {
                "data": [
                    {
                        "date": idx.strftime("%Y-%m-%d"),
                        "normalized_value": round(float(val), 2)
                    }
                    for idx, val in normalized_prices.items()
                ],
                "period_change": round(((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100, 2),
            }
    
    return {
        "comparison": comparison,
        "tickers": ticker_list,
        "period": period,
        "base": 100,
    }


# ============= Advanced Analysis Endpoints =============

@app.get("/api/crypto/analysis/score/{ticker}")
@app.get("/api/sp500/analysis/score/{ticker}")  # Keep for backwards compatibility
def get_technical_score(ticker: str, period: str = Query(default="3mo")):
    """Returns Technical Score and Automatic Recommendation"""
    from ..services.crypto_data_service import crypto_service
    from ..services.technical_analysis_advanced import TechnicalAnalysisAdvanced
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    score = TechnicalAnalysisAdvanced.calculate_technical_score(data)
    pivot = TechnicalAnalysisAdvanced.calculate_pivot_points(data)
    anomalies = TechnicalAnalysisAdvanced.detect_anomalies(data)
    support_resistance = TechnicalAnalysisAdvanced.detect_support_resistance(data)
    
    return {
        "ticker": ticker,
        "score": score['score'],
        "recommendation": score['recommendation'],
        "signals": score['signals'],
        "pivot_points": pivot,
        "support": support_resistance['support'],
        "resistance": support_resistance['resistance'],
        "anomalies": anomalies,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/crypto/analysis/patterns/{ticker}")
@app.get("/api/sp500/analysis/patterns/{ticker}")  # Keep for backwards compatibility
def get_candle_patterns(ticker: str, period: str = Query(default="1mo")):
    """Detects candlestick patterns"""
    from ..services.crypto_data_service import crypto_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    # Last 10 days with patterns
    patterns_found = []
    for i in range(max(0, len(data) - 10), len(data)):
        row = data.iloc[i]
        day_patterns = []
    
        if row.get('Doji', False):
            day_patterns.append('Doji')
        if row.get('Hammer', False):
            day_patterns.append('Hammer (Bullish)')
        if row.get('Bullish_Engulfing', False):
            day_patterns.append('Bullish Engulfing')
        if row.get('Bearish_Engulfing', False):
            day_patterns.append('Bearish Engulfing')
    
        if day_patterns:
            patterns_found.append({
                'date': row.name.strftime("%Y-%m-%d"),
                'patterns': day_patterns,
                'price': float(row['Close'])
            })
    
    return {
        "ticker": ticker,
        "patterns": patterns_found,
        "total": len(patterns_found)
    }


@app.get("/api/crypto/analysis/volume-profile/{ticker}")
@app.get("/api/sp500/analysis/volume-profile/{ticker}")  # Keep for backwards compatibility
def get_volume_profile(ticker: str, period: str = Query(default="3mo")):
    """Returns Volume Profile for the cryptocurrency"""
    from ..services.crypto_data_service import crypto_service
    from ..services.technical_analysis_advanced import TechnicalAnalysisAdvanced
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    volume_profile = TechnicalAnalysisAdvanced.calculate_volume_profile(data)
    
    return {
        "ticker": ticker,
        "profile": volume_profile['profile'],
        "poc": volume_profile['poc'],
        "total_volume": volume_profile['total_volume'],
        "period": period
    }


@app.get("/api/crypto/analysis/advanced-indicators/{ticker}")
@app.get("/api/sp500/analysis/advanced-indicators/{ticker}")  # Keep for backwards compatibility
def get_advanced_indicators(ticker: str, period: str = Query(default="6mo")):
    """Returns all advanced indicators"""
    from ..services.crypto_data_service import crypto_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    last = data.iloc[-1]
    
    indicators = {
        "ticker": ticker,
        "current_price": float(last['Close']),
        "vwap": float(last.get('VWAP', 0)) if pd.notna(last.get('VWAP')) else None,
        "obv": float(last.get('OBV', 0)) if pd.notna(last.get('OBV')) else None,
        "mfi": float(last.get('MFI', 0)) if pd.notna(last.get('MFI')) else None,
        "force_index": float(last.get('Force_Index', 0)) if pd.notna(last.get('Force_Index')) else None,
        "accumulation_distribution": float(last.get('AD', 0)) if pd.notna(last.get('AD')) else None,
        "roc": float(last.get('ROC', 0)) if pd.notna(last.get('ROC')) else None,
        "momentum": float(last.get('Momentum', 0)) if pd.notna(last.get('Momentum')) else None,
        "adx": float(last.get('ADX', 0)) if pd.notna(last.get('ADX')) else None,
    
        # Time series of last 30 days
        "history": [
            {
                "date": idx.strftime("%Y-%m-%d"),
                "vwap": float(row.get('VWAP', 0)) if pd.notna(row.get('VWAP')) else None,
                "obv": float(row.get('OBV', 0)) if pd.notna(row.get('OBV')) else None,
                "mfi": float(row.get('MFI', 0)) if pd.notna(row.get('MFI')) else None,
                "adx": float(row.get('ADX', 0)) if pd.notna(row.get('ADX')) else None,
            }
            for idx, row in data.tail(30).iterrows()
        ]
    }
    
    return indicators


@app.post("/api/crypto/analysis/comparator")
@app.post("/api/sp500/analysis/comparator")  # Keep for backwards compatibility
def compare_cryptos_advanced(
    tickers: str = Query(..., description="Comma-separated tickers"),
    period: str = Query(default="1y")
):
    """Compares multiple cryptocurrencies with advanced metrics"""
    from ..services.crypto_data_service import crypto_service
    from ..services.technical_analysis_advanced import StockComparator
    
    ticker_list = [t.strip() for t in tickers.split(',')]
    
    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 tickers")
    
    stocks_data = {}
    for ticker in ticker_list:
        data = crypto_service.fetch_crypto_data(ticker, period)
        if not data.empty:
            stocks_data[ticker] = data
    
    comparison = StockComparator.compare_metrics(stocks_data)
    
    return {
        "comparison": comparison.to_dict(orient='records'),
        "tickers": ticker_list,
        "period": period
    }


@app.get("/api/crypto/analysis/fibonacci/{ticker}")
@app.get("/api/sp500/analysis/fibonacci/{ticker}")  # Keep for backwards compatibility
def get_fibonacci(ticker: str, period: str = Query(default="3mo")):
    """Returns Fibonacci levels, Camarilla and extensions"""
    from ..services.crypto_data_service import crypto_service
    from ..services.technical_analysis_advanced import TechnicalAnalysisAdvanced

    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")

    fibonacci = TechnicalAnalysisAdvanced.calculate_fibonacci(data)
    
    return {
        "ticker": ticker,
        **fibonacci,
        "period": period,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/crypto/screener")
@app.get("/api/sp500/screener")  # Keep for backwards compatibility
def crypto_screener(
    rsi_max: float = Query(default=None),
    rsi_min: float = Query(default=None),
    score_min: float = Query(default=None),
    volume_min: float = Query(default=None),
    price_max: float = Query(default=None),
    price_min: float = Query(default=None)
):
    """
    Cryptocurrency screener with custom filters (with 5-minute cache)
    """
    from ..services.crypto_data_service import crypto_service
    from ..services.technical_analysis_advanced import TechnicalAnalysisAdvanced
    from ..services.cache_service import cache_service
    
    # Create unique key for this filter
    cache_key = f"crypto_screener_{rsi_max}_{rsi_min}_{score_min}_{volume_min}_{price_max}_{price_min}"
    
    # Check cache (5 minutes)
    cached = cache_service.get(cache_key)
    if cached is not None:
        logger.info(f"📦 Crypto Screener returned from cache")
        return cached
    
    logger.info(f"🔍 Processing Crypto Screener (no cache)...")
    results = []
    
    # Fetch only 20 cryptos to avoid taking too long
    cryptos_to_analyze = crypto_service.MAIN_CRYPTOS[:20]
    
    for ticker in cryptos_to_analyze:
        try:
            data = crypto_service.fetch_crypto_data(ticker, '3mo')
            
            if data.empty or len(data) < 20:
                continue
            
            info = crypto_service.fetch_crypto_info(ticker)
            last = data.iloc[-1]
            
            # Extract values with protection against None/NaN
            price_value = float(info.get('current_price', 0)) if info.get('current_price') else 0.0
            rsi_value = float(last.get('RSI', 50)) if pd.notna(last.get('RSI')) else 50
            volume_value = float(last.get('Volume', 0)) if pd.notna(last.get('Volume')) else 0
            
            # Apply filters
            if price_max and price_value > price_max:
                continue
            if price_min and price_value < price_min:
                continue
            if rsi_max and rsi_value > rsi_max:
                continue
            if rsi_min and rsi_value < rsi_min:
                continue
            if volume_min and volume_value < volume_min:
                continue
            
            # Calculate score
            score_data = TechnicalAnalysisAdvanced.calculate_technical_score(data)
            
            if score_min and score_data['score'] < score_min:
                continue
            
            results.append({
                'ticker': str(ticker),
                'name': str(info.get('name', ticker)),
                'price': float(price_value),
                'market_cap': float(info.get('market_cap', 0)),
                'rsi': float(rsi_value),
                'score': float(score_data['score']),
                'recommendation': str(score_data['recommendation']),
                'volume': float(volume_value)
            })
            
        except Exception as e:
            logger.error(f"❌ Error analyzing {ticker} in crypto screener: {e}")
            continue
    
    # Sort by score
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    response = {
        "results": results,
        "total": len(results),
        "filters_applied": {
            "price_max": price_max,
            "price_min": price_min,
            "rsi_max": rsi_max,
            "rsi_min": rsi_min,
            "score_min": score_min,
            "volume_min": volume_min
        }
    }
    
    # Cache result for 5 minutes (300 seconds)
    cache_service.set(cache_key, response, ttl=300)
    logger.info(f"✅ Crypto Screener processed and cached: {len(results)} results")
    
    return response


@app.get("/api/crypto/heatmap/market-cap")
@app.get("/api/sp500/heatmap/market-cap")  # Keep for backwards compatibility
def get_heatmap_market_cap():
    """Returns data for Market Cap Treemap"""
    from ..services.crypto_data_service import crypto_service

    cryptos = crypto_service.get_main_cryptos()

    # Group by category
    sectors_data = {}
    for crypto in cryptos:
        sector = crypto.get('sector', 'Others')
        if sector not in sectors_data:
            sectors_data[sector] = []

        sectors_data[sector].append({
            'ticker': crypto['ticker'],
            'name': crypto['name'],
            'market_cap': crypto.get('market_cap', 0),
            'change': crypto.get('day_change', 0),
            'price': crypto.get('current_price', 0)
        })
    
    return {
        "sectors": sectors_data,
        "total_stocks": len(cryptos)
    }


# ============= Paper Trading Endpoints =============

@app.get("/api/paper-trading/portfolio/{user_id}")
def get_paper_trading_portfolio(user_id: str):
    """Returns user's paper trading portfolio"""
    portfolio = paper_trading_service.get_portfolio(user_id)
    return portfolio


@app.post("/api/paper-trading/buy")
def buy_stock_paper_trading(
    user_id: str = Query(...),
    ticker: str = Query(...),
    quantity: int = Query(...),
    price: float = Query(...)
):
    """Simulates stock purchase"""
    result = paper_trading_service.buy_stock(user_id, ticker, quantity, price)
    return result


@app.post("/api/paper-trading/sell")
def sell_stock_paper_trading(
    user_id: str = Query(...),
    ticker: str = Query(...),
    quantity: int = Query(...),
    price: float = Query(...)
):
    """Simulates stock sale"""
    result = paper_trading_service.sell_stock(user_id, ticker, quantity, price)
    return result


@app.get("/api/paper-trading/equity/{user_id}")
def get_paper_trading_equity(user_id: str, tickers: str = Query(default="")):
    """Calculates total portfolio equity"""
    from ..services.paper_trading_service import paper_trading_service
    from ..services.crypto_data_service import crypto_service
    
    portfolio = paper_trading_service.get_portfolio(user_id)
    
    # Fetch current prices
    current_prices = {}
    for ticker in portfolio['positions'].keys():
        try:
            info = crypto_service.fetch_crypto_info(ticker)
            current_prices[ticker] = info.get('current_price', 0)
        except:
            current_prices[ticker] = portfolio['positions'][ticker]['avg_price']
    
    equity = paper_trading_service.calculate_equity(user_id, current_prices)
    return equity


@app.post("/api/paper-trading/reset/{user_id}")
def reset_paper_trading_portfolio(user_id: str):
    """Resets portfolio to initial state"""
    result = paper_trading_service.reset_portfolio(user_id)
    return result


# ============= WebSocket - Live Market Feed =============

@app.websocket("/ws/market-feed")
async def websocket_market_feed(websocket: WebSocket):
    """
    WebSocket for real-time market feed
    Continuously sends buy/sell/price change events
    """
    await websocket.accept()
    logger.info("🔌 Client connected to Market Feed")
    
    try:
        from ..services.market_feed_service import market_feed_service
        await market_feed_service.stream_events(websocket)
    
    except WebSocketDisconnect:
        logger.info("🔌 Client disconnected from Market Feed")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")


# ============= ADVANCED ANALYSIS ENDPOINTS (20 NEW FEATURES) =============

@app.get("/api/crypto/advanced/divergences/{ticker}")
def get_divergences(ticker: str, period: str = Query(default="3mo")):
    """Detecta divergências entre preço e RSI"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.detect_divergences(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/gaps/{ticker}")
def get_gaps(ticker: str, period: str = Query(default="6mo")):
    """Analisa gaps de preço"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.analyze_gaps(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/breakout/{ticker}")
def get_breakout_analysis(ticker: str, period: str = Query(default="1y")):
    """Detecta breakouts"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.detect_breakouts(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/support-resistance/{ticker}")
def get_advanced_support_resistance(ticker: str, period: str = Query(default="6mo")):
    """Suporte e resistência avançados com cluster analysis"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.advanced_support_resistance(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/momentum-multi/{ticker}")
def get_momentum_multi_timeframe(ticker: str):
    """Momentum em múltiplos timeframes"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, "1y")
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.momentum_multi_timeframe(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/relative-strength/{ticker}")
def get_relative_strength(ticker: str, period: str = Query(default="6mo")):
    """Força relativa vs Bitcoin"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    crypto_data = crypto_service.fetch_crypto_data(ticker, period)
    btc_data = crypto_service.fetch_crypto_data("BTC-USD", period)
    
    if crypto_data.empty or btc_data.empty:
        raise HTTPException(status_code=404, detail="Data not available")
    
    result = advanced_analysis_service.calculate_relative_strength(crypto_data, btc_data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/mean-reversion/{ticker}")
def get_mean_reversion(ticker: str, period: str = Query(default="3mo")):
    """Análise de mean reversion com Z-Score"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.mean_reversion_zscore(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/swing-signals/{ticker}")
def get_swing_signals(ticker: str, period: str = Query(default="3mo")):
    """Sinais de swing trading"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.swing_trading_signals(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/seasonality/{ticker}")
def get_seasonality(ticker: str):
    """Análise de sazonalidade"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, "2y")
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.seasonality_analysis(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/volatility-expanded/{ticker}")
def get_volatility_expanded(ticker: str, period: str = Query(default="6mo")):
    """Análise expandida de volatilidade"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.volatility_analysis_expanded(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/price-patterns/{ticker}")
def get_price_patterns(ticker: str, period: str = Query(default="6mo")):
    """Detecta padrões clássicos de price action"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.detect_price_patterns(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/statistical/{ticker}")
def get_statistical_analysis(ticker: str, period: str = Query(default="1y")):
    """Dashboard estatístico completo"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.statistical_analysis(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/anomalies/{ticker}")
def get_anomalies(ticker: str, period: str = Query(default="1y")):
    """Detecção de anomalias de mercado"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.detect_anomalies(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/consensus/{ticker}")
def get_multi_indicator_consensus(ticker: str, period: str = Query(default="3mo")):
    """Sistema de votação multi-indicadores"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.multi_indicator_consensus(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/watchlist-compare")
def get_watchlist_comparison(
    tickers: str = Query(..., description="Comma-separated tickers"),
    period: str = Query(default="3mo")
):
    """Compara múltiplas cryptos lado a lado"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    ticker_list = [t.strip() for t in tickers.split(',')]
    stocks_data = {}
    
    for ticker in ticker_list:
        data = crypto_service.fetch_crypto_data(ticker, period)
        if not data.empty:
            stocks_data[ticker] = data
    
    if not stocks_data:
        raise HTTPException(status_code=404, detail="No valid tickers found")
    
    result = advanced_analysis_service.compare_watchlist(stocks_data)
    return {"comparison": result, "total": len(result)}


@app.get("/api/crypto/advanced/trade-planner/{ticker}")
def get_trade_planner(ticker: str, period: str = Query(default="3mo")):
    """Plano visual de trade com entry, stop e targets"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.trade_planner(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/fast-movers")
def get_fast_movers(period: str = Query(default="1mo")):
    """Cryptos com movimento rápido (alerta)"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    from ..services.cache_service import cache_service
    
    # Cache por 5 minutos
    cache_key = "fast_movers"
    cached = cache_service.get(cache_key)
    if cached:
        return cached
    
    # Analisa top 30 cryptos
    main_cryptos = crypto_service.MAIN_CRYPTOS[:30]
    stocks_data = {}
    
    for ticker in main_cryptos:
        try:
            data = crypto_service.fetch_crypto_data(ticker, period)
            if not data.empty:
                stocks_data[ticker] = data
        except:
            continue
    
    result = advanced_analysis_service.fast_movers_scanner(stocks_data)
    response = {"movers": result, "total": len(result)}
    
    cache_service.set(cache_key, response, ttl_seconds=300)
    return response


@app.get("/api/crypto/advanced/dca-simulator/{ticker}")
def get_dca_simulator(
    ticker: str,
    monthly_investment: float = Query(default=100),
    months: int = Query(default=12)
):
    """Simula estratégia DCA (Dollar-Cost Averaging)"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    # Precisa de dados suficientes
    data = crypto_service.fetch_crypto_data(ticker, "2y")
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.dca_simulator(data, monthly_investment, months)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/entry-checklist/{ticker}")
def get_entry_checklist(ticker: str, period: str = Query(default="3mo")):
    """Checklist antes de entrar em trade"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.entry_checklist(data)
    return {"ticker": ticker, **result}


@app.get("/api/crypto/advanced/fibonacci-time/{ticker}")
def get_fibonacci_time_zones(ticker: str, period: str = Query(default="6mo")):
    """Projeção temporal de Fibonacci"""
    from ..services.crypto_data_service import crypto_service
    from ..services.advanced_analysis_service import advanced_analysis_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = advanced_analysis_service.fibonacci_time_zones(data)
    return {"ticker": ticker, **result}


# ============================================================
# PROFESSIONAL TOOLS API - 28 Advanced Features
# ============================================================

@app.get("/api/professional/ichimoku/{ticker}")
def get_ichimoku_cloud(ticker: str, period: str = Query(default="6mo")):
    """Complete Ichimoku Cloud System"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.ichimoku_cloud(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/elliott-wave/{ticker}")
def get_elliott_wave(ticker: str, period: str = Query(default="6mo")):
    """Elliott Wave Counter"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.elliott_wave_counter(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/wyckoff/{ticker}")
def get_wyckoff_analysis(ticker: str, period: str = Query(default="3mo")):
    """Wyckoff Method Analysis"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.wyckoff_analysis(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/trend-alignment/{ticker}")
def get_trend_alignment(ticker: str, period: str = Query(default="6mo")):
    """Trend Alignment Scanner"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.trend_alignment_scanner(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/candlestick-patterns/{ticker}")
def get_candlestick_patterns(ticker: str, period: str = Query(default="3mo")):
    """Candlestick Pattern Library"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.candlestick_pattern_library(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/support-resistance/{ticker}")
def get_support_resistance_zones(ticker: str, period: str = Query(default="6mo")):
    """Support/Resistance Zones"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.support_resistance_zones(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/monte-carlo/{ticker}")
def get_monte_carlo_simulation(
    ticker: str, 
    period: str = Query(default="6mo"),
    days: int = Query(default=30),
    simulations: int = Query(default=1000)
):
    """Monte Carlo Simulation"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.monte_carlo_simulation(data, days, simulations)
    return {"ticker": ticker, **result}


@app.get("/api/professional/calendar/{ticker}")
def get_historical_calendar(ticker: str, period: str = Query(default="2y")):
    """Historical Performance Calendar"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.historical_performance_calendar(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/drawdown/{ticker}")
def get_drawdown_analysis(ticker: str, period: str = Query(default="1y")):
    """Drawdown Analysis"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.drawdown_analysis(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/win-rate/{ticker}")
def get_win_rate_by_time(ticker: str, period: str = Query(default="1y")):
    """Win Rate by Day/Hour"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.win_rate_by_time(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/confluence/{ticker}")
def get_confluence_detector(ticker: str, period: str = Query(default="6mo")):
    """Confluence Detector"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.confluence_detector(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/reversal-probability/{ticker}")
def get_reversal_probability(ticker: str, period: str = Query(default="3mo")):
    """Reversal Probability"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.reversal_probability(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/acceleration/{ticker}")
def get_acceleration_indicator(ticker: str, period: str = Query(default="3mo")):
    """Acceleration Indicator"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.acceleration_indicator(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/volume-momentum/{ticker}")
def get_volume_momentum(ticker: str, period: str = Query(default="3mo")):
    """Volume Momentum"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.volume_momentum(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/velocity/{ticker}")
def get_price_velocity_gauge(ticker: str, period: str = Query(default="3mo")):
    """Price Velocity Gauge"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.price_velocity_gauge(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/position-sizing/{ticker}")
def get_position_sizing(
    ticker: str,
    period: str = Query(default="3mo"),
    account_size: float = Query(default=10000),
    risk_pct: float = Query(default=2),
    stop_loss_pct: float = Query(default=5)
):
    """Position Sizing Calculator"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.position_sizing_calculator(data, account_size, risk_pct, stop_loss_pct)
    return {"ticker": ticker, **result}


@app.get("/api/professional/risk-reward/{ticker}")
def get_risk_reward_heatmap(ticker: str, period: str = Query(default="3mo")):
    """Risk/Reward Heatmap"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.risk_reward_heatmap(data)
    return {"ticker": ticker, **result}


@app.get("/api/professional/technical-setups/{ticker}")
def get_technical_setups(ticker: str, period: str = Query(default="6mo")):
    """Technical Setup Finder"""
    from ..services.crypto_data_service import crypto_service
    from ..services.professional_tools_service import professional_tools_service
    
    data = crypto_service.fetch_crypto_data(ticker, period)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"Crypto {ticker} not found")
    
    result = professional_tools_service.technical_setup_finder(data)
    return {"ticker": ticker, **result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
