"""Pydantic response schemas for the Stock Market Intelligence API."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float


class DetailedHealthResponse(HealthResponse):
    request_count: int
    error_count: int
    error_rate: float
    components: dict[str, str]


class VersionResponse(BaseModel):
    version: str
    api_name: str


class MetricsResponse(BaseModel):
    request_count: int
    error_count: int
    error_rate: float
    uptime_seconds: float


class SignalResponse(BaseModel):
    ticker: str
    signal: str
    confidence: float
    price: float
    timestamp: str


class PortfolioRiskResponse(BaseModel):
    ticker: str
    var_95: float = Field(description="Value-at-Risk at 95% confidence (fraction)")
    sharpe_ratio: float = Field(description="Annualised Sharpe ratio")
    max_drawdown: float = Field(description="Maximum drawdown fraction")
    annualised_vol: float = Field(description="Annualised volatility fraction")
    timestamp: str


class ArticleSummary(BaseModel):
    title: str
    source: str
    url: str
    published_date: str
    ticker: Optional[str] = None


class AnalyzeResponse(BaseModel):
    ticker: str
    recommendation: str
    articles_analysed: int
    sentiment_score: Optional[float] = None
    timestamp: str
