import pandas as pd
import duckdb
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def run_chunked_sentiment():
    print("Batching Pipeline")
    sia = SentimentIntensityAnalyzer()
    
   
    con = duckdb.connect('data/processed/airbnb.duckdb')
    con.execute("DROP TABLE IF EXISTS raw_sentiment_stage")
    con.execute("CREATE TABLE raw_sentiment_stage (listing_id BIGINT, sentiment_score DOUBLE)")
    
    chunk_size = 10000
    total_processed = 0
    
    print("Reading ALL reviews in the dataset ")
    
 
    try:
        chunks = pd.read_csv("data/raw/london_reviews.csv.gz", chunksize=chunk_size, low_memory=False)
    except FileNotFoundError:
        print("❌ Error: london_reviews.csv.gz not found.")
        return

    for i, chunk in enumerate(chunks):
   
        chunk = chunk.dropna(subset=['comments']).copy()
        
        chunk['sentiment_score'] = chunk['comments'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])
        
       
        batch_df = chunk[['listing_id', 'sentiment_score']]
        
     
        con.execute("INSERT INTO raw_sentiment_stage SELECT * FROM batch_df")
        
        total_processed += len(chunk)
        print(f"   -> Processed batch {i+1} ({total_processed} rows).")
        
        time.sleep(3)

    print("\nEnd of file")
    
    con.execute("""
        CREATE OR REPLACE TABLE london_sentiment AS 
        SELECT 
            listing_id, 
            AVG(sentiment_score) as avg_sentiment, 
            COUNT(*) as total_reviews
        FROM raw_sentiment_stage 
        GROUP BY listing_id
    """)
    
    
    con.execute("DROP TABLE raw_sentiment_stage")
    con.close()
    
    print(f"Pipeline complete! {total_processed} total reviews ")

if __name__ == "__main__":
    run_chunked_sentiment()