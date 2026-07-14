import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_dataset(n_records=500, output_path='data/login_data.csv'):
    """Generates a synthetic login dataset with suspicious patterns."""
    users = [f'user_{i}' for i in range(1, 21)]
    locations = ['New York', 'London', 'Tokyo', 'Mumbai', 'Berlin', 'Paris', 'Sydney']
    ips = [f'192.168.1.{i}' for i in range(1, 50)]
    
    data = []
    base_time = datetime.now() - timedelta(days=2)

    for i in range(n_records):
        user = random.choice(users)
        # Normal login behavior
        timestamp = base_time + timedelta(minutes=i*5 + random.randint(0, 10))
        status = 'Success' if random.random() > 0.15 else 'Failed'
        location = random.choice(locations)
        ip = random.choice(ips)
        
        data.append([user, timestamp, ip, location, status])

    # Inject Suspicious Patterns
    # 1. Brute Force (User 5 has 5 failed attempts in 10 mins)
    for i in range(5):
        data.append(['user_5', base_time + timedelta(hours=5, minutes=i*2), '10.0.0.1', 'Moscow', 'Failed'])
    
    # 2. Impossible Travel (User 10 logs in from NY and Tokyo in 5 mins)
    data.append(['user_10', base_time + timedelta(hours=10), '1.1.1.1', 'New York', 'Success'])
    data.append(['user_10', base_time + timedelta(hours=10, minutes=5), '2.2.2.2', 'Tokyo', 'Success'])
    
    # 3. Odd Hour Login (User 3 at 3 AM)
    odd_time = base_time.replace(hour=3, minute=15)
    data.append(['user_3', odd_time, '192.168.1.100', 'Berlin', 'Success'])

    df = pd.DataFrame(data, columns=['user_id', 'timestamp', 'ip', 'location', 'status'])
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path}")
    return df

if __name__ == "__main__":
    generate_dataset()
