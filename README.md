# Suspicious Login Detection System

## Overview
This project is a comprehensive security tool designed to detect anomalous login activities using a combination of **Rule-Based Heuristics** and **Machine Learning**. It processes login logs, identifies threats like brute-force attacks and impossible travel, and assigns a risk score to every event.

## Features
- **Data Generation**: Creates synthetic login data with injected attack patterns.
- **Rule-Based Detection**:
    - Brute Force: Detects multiple failed attempts.
    - Odd-Hour Logins: Flags logins between 12 AM and 5 AM.
    - Geo-Shift: Identifies "impossible travel" (multiple locations in < 1 hour).
- **Machine Learning**: Uses **Isolation Forest** (Anomaly Detection) to find patterns that deviate from normal behavior.
- **Risk Scoring**: Categorizes events into Low, Medium, and High risk.
- **Alert System**: Simulates SMTP email notifications for high-risk threats.
- **Visualizations**: Generates distribution charts and threat analysis reports.

## Project Structure
```text
suspicious_login_system/
├── data/               # Raw login data (CSV)
├── output/             # Processed reports and PNG charts
├── src/
│   ├── data_gen.py     # Synthetic data generator
│   ├── detector.py     # Detection logic (Rules + ML)
│   ├── risk_engine.py  # Scoring logic
│   └── utils.py        # Visualization & Alerts
├── main.py             # Execution pipeline & Simulation
└── README.md           # Project documentation
```

## How to Run
1. Ensure you have the required libraries:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

## Output
- `output/suspicious_users.csv`: A filtered list of users requiring investigation.
- `output/risk_distribution.png`: Visualization of overall system health.
- `output/failed_logins.png`: Bar chart showing top targets/attackers.

## Real-World Relevance
This system mimics modern SIEM (Security Information and Event Management) tools. Detecting brute force and impossible travel is a standard requirement for PCI-DSS and SOC2 compliance.
