import React from 'react';

function SignalCard({ signal }) {
  const getSignalColor = (sig) => {
    if (sig.includes('BUY')) return '#00ff00';
    if (sig.includes('SELL')) return '#ff0000';
    return '#ffaa00';
  };

  return (
    <div className="card signal-card">
      <div className="signal-header">
        <h2>{signal.ticker}</h2>
        <div
          className="signal-badge"
          style={{ color: getSignalColor(signal.signal?.final_signal) }}
        >
          {signal.signal?.final_signal}
        </div>
      </div>

      <div className="signal-grid">
        <div className="signal-item">
          <span className="label">Price</span>
          <span className="value">
            ${signal.signal?.technical?.latest_price}
          </span>
        </div>
        <div className="signal-item">
          <span className="label">Change</span>
          <span className="value">
            {signal.signal?.technical?.price_change_percent}%
          </span>
        </div>
        <div className="signal-item">
          <span className="label">Score</span>
          <span className="value">
            {(signal.signal?.combined_score * 100).toFixed(0)}%
          </span>
        </div>
        <div className="signal-item">
          <span className="label">Confidence</span>
          <span className="value">
            {(signal.signal?.confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      <style>{`
        .signal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .signal-header h2 {
          font-size: 28px;
        }

        .signal-badge {
          font-size: 18px;
          font-weight: 700;
          padding: 8px 16px;
          border-radius: 6px;
          background: rgba(0, 212, 255, 0.1);
          border: 1px solid currentColor;
        }

        .signal-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 15px;
        }

        .signal-item {
          display: flex;
          flex-direction: column;
          gap: 8px;
          padding: 15px;
          background: rgba(0, 212, 255, 0.05);
          border-radius: 8px;
          border: 1px solid rgba(0, 212, 255, 0.1);
        }

        .label {
          font-size: 12px;
          color: #888;
          text-transform: uppercase;
        }

        .value {
          font-size: 20px;
          font-weight: 600;
          color: #00d4ff;
        }
      `}</style>
    </div>
  );
}

export default SignalCard;
