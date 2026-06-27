import pandas as pd
import duckdb
# We swapped NLTK for the standalone package to bypass the network error
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment():
    print("Booting up Analysis")

    # Limiting to 10,000 rows to prevent CPU thermal throttling
    print("Reading reviews...")
    try:
        df = pd.read_csv("data/raw/london_reviews.csv.gz", nrows=10000, low_memory=False)
    except FileNotFoundError:
        print("Error: london_reviews.csv.gz not found.")
        return

    df = df.dropna(subset=['comments'])
    
    # Initialize the standalone AI
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