"""
Data Engineering Utilities for UIDAI Pulse
Optional data preparation and transformation functions
"""

import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from pathlib import Path

class UidaiDataPipeline:
    """Data engineering pipeline for UIDAI datasets"""
    
    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        self.df = None
        
    def load_raw_data(self):
        """Load raw data from CSV"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.input_path}")
        
        self.df = pd.read_csv(self.input_path)
        print(f"✓ Loaded {len(self.df)} records from {self.input_path.name}")
        return self
    
    def normalize_names(self):
        """Normalize state and district names"""
        if 'State' in self.df.columns:
            self.df['State'] = self.df['State'].astype(str).str.strip().str.upper()
        
        if 'District' in self.df.columns:
            self.df['District'] = self.df['District'].astype(str).str.strip().str.title()
        
        print("✓ Normalized state and district names")
        return self
    
    def remove_ghost_districts(self, threshold=100):
        """Remove districts with very low enrolment"""
        if 'Total_Enrolment' not in self.df.columns:
            print("⚠ Total_Enrolment column not found, skipping ghost district removal")
            return self
        
        initial_count = len(self.df)
        self.df = self.df[self.df['Total_Enrolment'] > threshold].copy()
        removed = initial_count - len(self.df)
        
        print(f"✓ Removed {removed} ghost districts (enrolment ≤ {threshold})")
        return self
    
    def winsorize_metrics(self, columns=None, limits=(0, 1)):
        """Apply winsorization to cap outliers"""
        if columns is None:
            columns = ['Migration_Intensity', 'Biometric_Lag', 'Digital_Penetration']
        
        for col in columns:
            if col in self.df.columns:
                # Clip to 0-100 range for percentage metrics
                self.df[col] = self.df[col].clip(0, 100)
        
        print(f"✓ Winsorized {len(columns)} metric columns")
        return self
    
    def calculate_risk_scores(self):
        """Calculate derived risk metrics"""
        if 'Migration_Intensity' in self.df.columns and 'Biometric_Lag' in self.df.columns:
            self.df['Risk_Score'] = (self.df['Migration_Intensity'] * self.df['Biometric_Lag']) / 100
            print("✓ Calculated risk scores")
        
        # Add risk categories
        if 'Risk_Score' in self.df.columns:
            self.df['Risk_Category'] = pd.cut(
                self.df['Risk_Score'],
                bins=[0, 30, 50, 70, 100],
                labels=['Low', 'Medium', 'High', 'Critical']
            )
            print("✓ Added risk categories")
        
        return self
    
    def add_geospatial_features(self):
        """Add geospatial aggregations and features"""
        # State-level statistics
        if 'State' in self.df.columns:
            state_stats = self.df.groupby('State').agg({
                'Total_Enrolment': 'sum',
                'Migration_Intensity': 'mean',
                'Biometric_Lag': 'mean',
                'Risk_Score': 'mean'
            }).reset_index()
            
            state_stats.columns = ['State', 'State_Total_Enrolment', 
                                   'State_Avg_Migration', 'State_Avg_Biometric_Lag',
                                   'State_Avg_Risk']
            
            self.df = self.df.merge(state_stats, on='State', how='left')
            print("✓ Added state-level aggregations")
        
        return self
    
    def handle_missing_values(self, strategy='median'):
        """Handle missing values"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if strategy == 'median':
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
        elif strategy == 'mean':
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        elif strategy == 'zero':
            self.df[numeric_cols] = self.df[numeric_cols].fillna(0)
        
        print(f"✓ Filled missing values using {strategy} strategy")
        return self
    
    def detect_anomalies(self):
        """Detect statistical anomalies using IQR method"""
        anomalies = pd.DataFrame()
        
        for col in ['Migration_Intensity', 'Biometric_Lag', 'Risk_Score']:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                
                col_anomalies = self.df[
                    (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                ].copy()
                col_anomalies['Anomaly_Metric'] = col
                
                anomalies = pd.concat([anomalies, col_anomalies])
        
        if len(anomalies) > 0:
            print(f"⚠ Detected {len(anomalies)} potential anomalies")
        else:
            print("✓ No anomalies detected")
        
        return anomalies
    
    def generate_summary_report(self):
        """Generate a summary statistics report"""
        print("\n" + "="*60)
        print("DATA SUMMARY REPORT")
        print("="*60)
        
        print(f"\n📊 Dataset Overview:")
        print(f"   • Total Records: {len(self.df):,}")
        print(f"   • States: {self.df['State'].nunique()}")
        print(f"   • Districts: {self.df['District'].nunique()}")
        
        if 'Total_Enrolment' in self.df.columns:
            print(f"   • Total Enrolments: {self.df['Total_Enrolment'].sum():,.0f}")
        
        print(f"\n📈 Key Metrics Summary:")
        metrics = ['Migration_Intensity', 'Biometric_Lag', 'Digital_Penetration', 'Risk_Score']
        
        for metric in metrics:
            if metric in self.df.columns:
                print(f"\n   {metric}:")
                print(f"      Mean:   {self.df[metric].mean():.2f}")
                print(f"      Median: {self.df[metric].median():.2f}")
                print(f"      Std:    {self.df[metric].std():.2f}")
                print(f"      Min:    {self.df[metric].min():.2f}")
                print(f"      Max:    {self.df[metric].max():.2f}")
        
        if 'Risk_Category' in self.df.columns:
            print(f"\n⚠️  Risk Distribution:")
            risk_dist = self.df['Risk_Category'].value_counts()
            for category, count in risk_dist.items():
                pct = (count / len(self.df)) * 100
                print(f"      {category}: {count} ({pct:.1f}%)")
        
        print("\n" + "="*60 + "\n")
        
        return self
    
    def save_processed_data(self, output_path: str):
        """Save processed data to CSV"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        print(f"✓ Saved processed data to {output_path}")
        
        return self
    
    def run_full_pipeline(self, output_path: str = None):
        """Execute complete data engineering pipeline"""
        print("\n🚀 Starting UIDAI Data Engineering Pipeline...")
        print("="*60 + "\n")
        
        self.load_raw_data()
        self.normalize_names()
        self.remove_ghost_districts()
        self.winsorize_metrics()
        self.handle_missing_values()
        self.calculate_risk_scores()
        self.add_geospatial_features()
        
        # Detect anomalies (but don't remove them)
        anomalies = self.detect_anomalies()
        
        self.generate_summary_report()
        
        if output_path:
            self.save_processed_data(output_path)
        
        print("✅ Pipeline execution complete!\n")
        
        return self.df, anomalies


# Example usage
if __name__ == "__main__":
    # Example: Process the UIDAI dataset
    pipeline = UidaiDataPipeline("artifacts/final_master_data.csv")
    
    try:
        processed_df, anomalies = pipeline.run_full_pipeline(
            output_path="artifacts/processed_master_data.csv"
        )
        
        print("✅ Data engineering complete!")
        print(f"📊 Processed {len(processed_df)} records")
        
        if len(anomalies) > 0:
            print(f"⚠️  Found {len(anomalies)} anomalies (saved for review)")
            anomalies.to_csv("artifacts/detected_anomalies.csv", index=False)
            
    except FileNotFoundError:
        print("⚠️  Sample data file not found.")
        print("💡 Create 'artifacts/final_master_data.csv' first or run the dashboard app.")
