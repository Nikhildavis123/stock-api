from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import yfinance as yf
from app.logger import logger
import time  

app = FastAPI()

cache = {}
CACHE_EXPIRY_SECONDS = 600  # 10 minutes
def get_cache_key(ticker: str, start: Optional[str], end: Optional[str]) -> str:
    return f"{ticker}_{start}_{end}"

@app.get("/api/stats")
def get_stock_stats(ticker: str, start: Optional[str] = None, end: Optional[str] = None):
    logger.info(f"Request received: ticker={ticker}, start={start}, end={end}")

    key = get_cache_key(ticker, start, end)
    now = time.time()

    # Checking cache
    if key in cache:
        data, timestamp = cache[key]
        if now - timestamp < CACHE_EXPIRY_SECONDS:
            logger.info(f"Serving cached data for {key}")
            return data
        else:
            logger.info(f"Cache expired for {key}")
            del cache[key]  # Remove expired

    # Fetch fresh data from yfinance
    try:
        df = yf.download(ticker, start=start, end=end)
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stock data")

    if df.empty:
        logger.warning(f"No data found for {ticker}")
        raise HTTPException(status_code=404, detail="No data found")

    logger.info(df)
    stats = {
        "ticker": ticker,
        "start": start,
        "end": end,
        "high": df["High"].max(),
        "low": df["Low"].min(),
        "average_close": round(df["Close"].mean(), 2),
        "last_close": round(df["Close"].iloc[-1], 2)
    }

    #saving to cache
    cache[key] = (stats, now)
    logger.info(f"Cached data for {key}")

    return stats