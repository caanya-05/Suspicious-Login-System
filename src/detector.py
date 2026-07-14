import pandas as pd
import numpy as np

class LoginDetector:
    def __init__(self, data_path='data/login_data.csv'):
        self.df = pd.read_csv(data_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])

    def rule_based_detection(self):
        """Applies simple heuristics to flag suspicious activity."""
        # 1. Failed Attempts Threshold (>3 in a row or short period)
        self.df['is_failed'] = self.df['status'].apply(lambda x: 1 if x == 'Failed' else 0)
        failed_counts = self.df.groupby('user_id')['is_failed'].rolling(window=5, min_periods=1).sum().reset_index(0, drop=True)
        self.df['flag_brute_force'] = (failed_counts >= 3).astype(int)

        # 2. Odd Hour Logins (12 AM - 5 AM)
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['flag_odd_hour'] = self.df['hour'].apply(lambda x: 1 if 0 <= x <= 5 else 0)

        # 3. Multiple Location Detection (Impossible Travel)
        # Check if a user has logged in from different locations in < 1 hour
        self.df = self.df.sort_values(['user_id', 'timestamp'])
        self.df['prev_location'] = self.df.groupby('user_id')['location'].shift(1)
        self.df['prev_time'] = self.df.groupby('user_id')['timestamp'].shift(1)
        
        def check_travel(row):
            if pd.isna(row['prev_location']) or row['location'] == row['prev_location']:
                return 0
            time_diff = (row['timestamp'] - row['prev_time']).total_seconds() / 60
            return 1 if time_diff < 60 else 0 # Flag if < 1 hour

        self.df['flag_geo_shift'] = self.df.apply(check_travel, axis=1)
        return self.df

    def ml_anomaly_detection(self):
        """
        Uses a statistical density approach to detect unusual login patterns.
        Flags logins that are statistically rare for the given user/location/hour.
        """
        # Create a combined feature key for frequency analysis
        self.df['pattern_key'] = self.df['user_id'] + "_" + self.df['location'] + "_" + self.df['hour'].astype(str)
        
        # Calculate frequency of each pattern
        pattern_counts = self.df['pattern_key'].value_counts()
        total_records = len(self.df)
        
        # Calculate a density score (normalized)
        pattern_density = self.df['pattern_key'].map(pattern_counts) / total_records
        
        # Flag as anomaly if the pattern is in the bottom 5% of density
        # This mimics the behavior of Isolation Forest's contamination parameter
        threshold = pattern_density.quantile(0.05)
        self.df['flag_ml_anomaly'] = (pattern_density <= threshold).astype(int)
        
        # Cleanup
        self.df = self.df.drop(columns=['pattern_key'])
        return self.df

if __name__ == "__main__":
    detector = LoginDetector()
    df = detector.rule_based_detection()
    df = detector.ml_anomaly_detection()
    print(df[df['flag_ml_anomaly'] == 1].head())
