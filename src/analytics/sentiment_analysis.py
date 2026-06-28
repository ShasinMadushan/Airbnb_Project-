import pandas as pd
import duckdb
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment():
    print("Booting up Analysis")

   
    print("Reading reviews...")
    try:
        df = pd.read_csv("data/raw/london_reviews.csv.gz", nrows=10000, low_memory=False)
    except FileNotFoundError:
        print("Error: london_reviews.csv.gz not found.")
        return

    df = df.dropna(subset=['comments'])
    
  
    sia = SentimentIntensityAnalyzer()
    
    print(f"Scoring {len(df)} guest reviews...")
    df['sentiment_score'] = df['comments'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])

    print("Aggregating emotional data...")
    listing_sentiment = df.groupby('listing_id').agg(
        avg_sentiment=('sentiment_score', 'mean'),
        total_reviews=('id', 'count')
    ).reset_index()

    print("Saving AI insights to DuckDB...")
    con = duckdb.connect('data/processed/airbnb.duckdb')
    con.execute("CREATE OR REPLACE TABLE london_sentiment AS SELECT * FROM listing_sentiment")
    con.close()

    print("Analysis complete!")

if __name__ == "__main__":
    analyze_sentiment()