class RiskScorer:
    @staticmethod
    def calculate_risk(df):
        """
        Assigns a risk score based on various flags.
        Weights:
        - Brute Force: 40
        - Geo Shift: 30
        - ML Anomaly: 20
        - Odd Hour: 10
        """
        df['risk_score'] = (
            df['flag_brute_force'] * 40 +
            df['flag_geo_shift'] * 30 +
            df['flag_ml_anomaly'] * 20 +
            df['flag_odd_hour'] * 10
        )
        
        # Ensure max score is 100
        df['risk_score'] = df['risk_score'].clip(0, 100)
        
        def categorize(score):
            if score >= 70: return 'High'
            if score >= 30: return 'Medium'
            return 'Low'
            
        df['risk_level'] = df['risk_score'].apply(categorize)
        
        # Generate a reason string
        def get_reason(row):
            reasons = []
            if row['flag_brute_force']: reasons.append("Multiple failed attempts")
            if row['flag_geo_shift']: reasons.append("Impossible travel detected")
            if row['flag_ml_anomaly']: reasons.append("Anomalous pattern (ML)")
            if row['flag_odd_hour']: reasons.append("Login at unusual hour")
            return ", ".join(reasons) if reasons else "Normal activity"
            
        df['reason'] = df.apply(get_reason, axis=1)
        return df
