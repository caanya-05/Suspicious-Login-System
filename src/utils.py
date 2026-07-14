import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    @staticmethod
    def plot_risk_distribution(df, output_dir='output/'):
        os.makedirs(output_dir, exist_ok=True)
        
        plt.figure(figsize=(10, 6))
        sns.countplot(x='risk_level', data=df, palette='viridis', order=['Low', 'Medium', 'High'])
        plt.title('Distribution of Login Risk Levels')
        plt.xlabel('Risk Level')
        plt.ylabel('Count')
        plt.savefig(os.path.join(output_dir, 'risk_distribution.png'))
        plt.close()
        print(f"Risk distribution chart saved to {output_dir}")

    @staticmethod
    def plot_failed_logins(df, output_dir='output/'):
        plt.figure(figsize=(10, 6))
        failed_df = df[df['status'] == 'Failed'].groupby('user_id').size().sort_values(ascending=False).head(10)
        failed_df.plot(kind='bar', color='salmon')
        plt.title('Top 10 Users with Failed Logins')
        plt.xlabel('User ID')
        plt.ylabel('Failed Attempts')
        plt.savefig(os.path.join(output_dir, 'failed_logins.png'))
        plt.close()
        print(f"Failed logins chart saved to {output_dir}")

class AlertSystem:
    @staticmethod
    def send_alert(user_id, risk_score, reason):
        """Simulates an email alert for high-risk activity."""
        print("\n" + "!" * 50)
        print(f"SECURITY ALERT: High Risk Detected!")
        print(f"User: {user_id}")
        print(f"Risk Score: {risk_score}")
        print(f"Reason: {reason}")
        print("Action: Email notification sent to Administrator via SMTP (Simulated)")
        print("!" * 50 + "\n")
