import time
import pandas as pd
import os
from src.data_gen import generate_dataset
from src.detector import LoginDetector
from src.risk_engine import RiskScorer
from src.utils import Visualizer, AlertSystem

def run_pipeline():
    print("--- Phase 1: Data Generation ---")
    generate_dataset()
    
    print("\n--- Phase 2: Processing and Detection ---")
    detector = LoginDetector()
    df = detector.rule_based_detection()
    df = detector.ml_anomaly_detection()
    
    print("\n--- Phase 3: Risk Scoring ---")
    scorer = RiskScorer()
    df = scorer.calculate_risk(df)
    
    # Save the full report
    os.makedirs('output', exist_ok=True)
    df.to_csv('output/processed_logins.csv', index=False)
    
    # Filter only suspicious users for final output
    suspicious_users = df[df['risk_score'] > 0][['user_id', 'timestamp', 'ip', 'risk_score', 'risk_level', 'reason']]
    suspicious_users.to_csv('output/suspicious_users.csv', index=False)
    print(f"Summary of suspicious activity saved to output/suspicious_users.csv")

    print("\n--- Phase 4: Real-Time Simulation ---")
    # We simulate a stream by iterating through the most recent records
    recent_records = df.tail(10) # Simulating the last 10 'new' logs
    for _, record in recent_records.iterrows():
        print(f"Scanning login: {record['user_id']} from {record['location']} ({record['status']})...")
        time.sleep(0.5) # Simulate processing time
        
        if record['risk_level'] == 'High':
            AlertSystem.send_alert(record['user_id'], record['risk_score'], record['reason'])
            
    print("\n--- Phase 5: Visualization ---")
    Visualizer.plot_risk_distribution(df)
    Visualizer.plot_failed_logins(df)
    
    print("\n" + "="*30)
    print("SYSTEM TASK COMPLETE")
    print("Check 'output/' folder for reports and charts.")
    print("="*30)

if __name__ == "__main__":
    run_pipeline()
