import pandas as pd
import duckdb
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def run_chunked_sentiment():
    print("Batching Pipeline")
    sia = SentimentIntensityAnalyzer()
    
    # 1. Connect to DuckDB and set up a temporary staging table
    con = duckdb.connect('data/processed/airbnb.duckdb')
    con.execute("DROP TABLE IF EXISTS raw_sentiment_stage")
    con.execute("CREATE TABLE raw_sentiment_stage (listing_id BIGINT, sentiment_score DOUBLE)")
    
    chunk_size = 10000
    total_processed = 0
    
    print("Reading ALL reviews in the dataset using hardware-safe micro-batches...")
    
    # 2. The Unconstrained Chunking Engine
    # We removed nrows, so it will read until the file is completely finished.
    try:
        chunks = pd.read_csv("data/raw/london_reviews.csv.gz", chunksize=chunk_size, low_memory=False)
    except FileNotFoundError:
        print("❌ Error: london_reviews.csv.gz not found.")
        return

    for i, chunk in enumerate(chunks):
        # Clean the chunk AND use .copy() to prevent the Pandas SettingWithCopy warning
        chunk = chunk.dropna(subset=['comments']).copy()
        
        # Score the AI sentiment
        chunk['sentiment_score'] = chunk['comments'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])
        
        # Isolate just the columns we need to save memory
        batch_df = chunk[['listing_id', 'sentiment_score']]
        
        # Append the batch to our DuckDB staging table
        con.execute("INSERT INTO raw_sentiment_stage SELECT * FROM batch_df")
        
        total_processed += len(chunk)
        print(f"   -> Processed batch {i+1} ({total_processed} rows).")
        
        # 3. The Hardware Safety Valve
        time.sleep(3)

    print("\nEnd of file")
    
    # 4. Final SQL Transformation 
    con.execute("""
        CREATE OR REPLACE TABLE london_sentiment AS 
        SELECT 
            listing_id, 
            AVG(sentiment_score) as avg_sentiment, 
            COUNT(*) as total_reviews
        FROM raw_sentiment_stage 
        GROUP BY listing_id
    """)
    
    # Clean up the staging table
    con.execute("DROP TABLE raw_sentiment_stage")
    con.close()
    
    print(f"Pipeline complete! {total_processed} total reviews ")

if __name__ == "__main__":
    run_chunked_sentiment()