"""
NVDB Traffic Insights - Data Processing Pipeline  
Norwegian Road Database Traffic Analysis

This module processes Norwegian NVDB traffic data to generate
actionable insights about traffic patterns, regional variations, and infrastructure usage.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def load_raw(filename):
    """Load raw NVDB traffic data"""
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / filename
    print(f"Processing NVDB traffic data from {raw_path}")
    return pd.read_csv(raw_path)


def build_traffic_metrics(df):
    """
    Build comprehensive traffic metrics with regional and temporal analysis
    
    Transforms raw NVDB traffic data into analytical metrics including:
    - Regional traffic volume comparisons
    - Monthly traffic patterns and seasonality  
    - Road category performance analysis
    - COVID-19 impact assessment
    - Infrastructure utilization trends
    
    Args:
        df (pd.DataFrame): Raw NVDB traffic data
        
    Returns:
        pd.DataFrame: Processed monthly metrics with regional analysis
    """
    # Data preparation
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    # Group by date, region, and road category for comprehensive analysis
    monthly = df.groupby(["date", "region", "road_category"]).agg({
        "value": ["sum", "mean", "max", "count"]
    }).round(1)
    monthly.columns = ["traffic_sum", "traffic_mean", "traffic_max", "traffic_count"]
    monthly = monthly.reset_index()
    
    # Calculate monthly changes (period-over-period growth)
    monthly["monthly_change_mean"] = monthly.groupby(["region", "road_category"])["traffic_mean"].pct_change() * 100
    monthly["monthly_change_mean"] = monthly["monthly_change_mean"].fillna(0).round(1)
    
    # Add date components first
    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month
    
    # Calculate rolling averages for trend smoothing
    monthly["rolling_3m_avg"] = monthly.groupby(["region", "road_category"])["traffic_mean"].transform(lambda x: x.rolling(window=3, center=True).mean()).round(1)
    
    # Year-over-year comparison for same month in previous year
    monthly["yoy_change"] = monthly.groupby(["region", "road_category", "month"])["traffic_mean"].pct_change(periods=1) * 100
    monthly["yoy_change"] = monthly["yoy_change"].fillna(0).round(1)
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    # Traffic volume classification
    monthly["volume_classification"] = monthly["traffic_mean"].apply(lambda x:
        "Very High" if x > 50000 else
        "High" if x > 40000 else
        "Moderate" if x > 30000 else
        "Low" if x > 20000 else
        "Very Low"
    )
    
    # COVID-19 impact period identification (2020 Q2-Q3)
    monthly["covid_period"] = ((monthly["year"] == 2020) & 
                              (monthly["month"].isin([3, 4, 5, 6, 7, 8, 9]))).astype(int)
    
    # Recovery trend classification
    monthly["recovery_trend"] = monthly["monthly_change_mean"].apply(lambda x:
        "Strong Recovery" if x > 10 else
        "Moderate Recovery" if x > 5 else
        "Stable" if x > -5 else
        "Declining" if x > -15 else
        "Sharp Decline"
    )
    
    return monthly


def calculate_regional_comparisons(df):
    """Calculate comprehensive regional traffic comparisons"""
    regional_stats = df.groupby(["region", "road_category"]).agg({
        "traffic_mean": ["mean", "std", "min", "max"],
        "monthly_change_mean": ["mean", "std"],
        "traffic_sum": ["sum", "count"]
    }).round(1)
    
    # Flatten column names
    regional_stats.columns = [
        "avg_traffic", "std_traffic", "min_traffic", "max_traffic",
        "avg_growth", "std_growth", "total_traffic", "months_tracked"
    ]
    regional_stats = regional_stats.reset_index()
    
    # Calculate efficiency metrics
    regional_stats["traffic_consistency"] = (1 - regional_stats["std_traffic"] / regional_stats["avg_traffic"]) * 100
    regional_stats["growth_stability"] = (1 - regional_stats["std_growth"] / (regional_stats["avg_growth"].abs() + 0.1)) * 100
    
    return regional_stats


def covid_impact_analysis(df):
    """Analyze COVID-19 impact on traffic patterns"""
    pre_covid = df[df["date"] < "2020-03-01"]["traffic_mean"].mean()
    covid_period = df[(df["date"] >= "2020-03-01") & (df["date"] < "2020-10-01")]["traffic_mean"].mean()
    post_covid = df[df["date"] >= "2021-01-01"]["traffic_mean"].mean()
    
    covid_impact = {
        "pre_covid_avg": pre_covid,
        "covid_period_avg": covid_period, 
        "post_covid_avg": post_covid,
        "covid_decline_pct": ((covid_period - pre_covid) / pre_covid * 100) if pre_covid > 0 else 0,
        "recovery_rate_pct": ((post_covid - covid_period) / covid_period * 100) if covid_period > 0 else 0,
        "full_recovery": post_covid >= pre_covid * 0.95  # 95% of pre-COVID levels
    }
    
    return covid_impact


def save_processed(df, filename):
    """Save processed data and regional analysis"""
    processed_path = Path(__file__).resolve().parents[2] / "data" / "processed" / filename
    df.to_csv(processed_path, index=False)
    print(f"Processed traffic data saved to {processed_path}")
    print(f"Dataset contains {len(df)} monthly records across {df['region'].nunique()} regions")
    return processed_path


def main():
    """Main processing pipeline for NVDB traffic insights"""
    parser = argparse.ArgumentParser(description="Process Norwegian NVDB traffic data")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--analysis", "-a", action="store_true", help="Include detailed analysis")
    args = parser.parse_args()
    
    if args.verbose:
        print("NVDB Traffic Insights - Data Processing Pipeline")
        print("Loading and processing Norwegian road traffic data...")
    
    try:
        # Load raw data
        df_raw = load_raw("norwegian_traffic_nvdb.csv")
        
        if args.verbose:
            print(f"Raw data loaded: {len(df_raw)} records")
            print(f"Date range: {df_raw['date'].min()} to {df_raw['date'].max()}")
            print(f"Regions: {df_raw['region'].unique()}")
            print(f"Road categories: {df_raw['road_category'].unique()}")
            if 'road_number' in df_raw.columns:
                print(f"Roads tracked: {df_raw['road_number'].unique()}")
        
        # Process data
        df_processed = build_traffic_metrics(df_raw)
        
        # Save results
        output_path = save_processed(df_processed, "traffic_insights_processed.csv")
        
        if args.verbose:
            print("\nProcessing Summary:")
            print(f"   • Total traffic volume tracked: {df_processed['traffic_sum'].sum():,.0f}")
            print(f"   • Average daily traffic: {df_processed['traffic_mean'].mean():,.0f}")
            print(f"   • Peak traffic month: {df_processed.loc[df_processed['traffic_mean'].idxmax(), 'date'].strftime('%B %Y')}")
            print(f"   • Lowest traffic month: {df_processed.loc[df_processed['traffic_mean'].idxmin(), 'date'].strftime('%B %Y')}")
            print(f"   • Average monthly change: {df_processed['monthly_change_mean'].mean():.1f}%")
        
        # Additional analysis if requested
        if args.analysis:
            print("\nDetailed Analysis:")
            
            # Regional comparison
            regional_stats = calculate_regional_comparisons(df_processed)
            print(f"\nRegional Performance:")
            for _, row in regional_stats.iterrows():
                print(f"   • {row['region']} ({row['road_category']}): {row['avg_traffic']:,.0f} avg traffic, {row['avg_growth']:.1f}% avg growth")
            
            # COVID impact analysis
            covid_analysis = covid_impact_analysis(df_processed)
            print(f"\nCOVID-19 Impact Analysis:")
            print(f"   • Pre-COVID average: {covid_analysis['pre_covid_avg']:,.0f}")
            print(f"   • COVID period decline: {covid_analysis['covid_decline_pct']:.1f}%")
            print(f"   • Recovery rate: {covid_analysis['recovery_rate_pct']:.1f}%")
            print(f"   • Full recovery achieved: {'Yes' if covid_analysis['full_recovery'] else 'No'}")
            
        print(f"\nReady for dashboard analysis!")
        print(f"   Run: streamlit run src/app/streamlit_app.py")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find data file - {e}")
        print("Ensure 'norwegian_traffic_nvdb.csv' exists in data/raw/")
    except Exception as e:
        print(f"Processing error: {e}")


if __name__ == "__main__":
    main()