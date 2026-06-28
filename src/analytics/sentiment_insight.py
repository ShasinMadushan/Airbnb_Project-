import duckdb

def get_sentiment_insight():
   
    con = duckdb.connect('data/processed/airbnb.duckdb', read_only=True)
    
    
    query = """
    SELECT 
        l.host_is_superhost as is_superhost, 
        COUNT(s.listing_id) as total_listings_scored,
        ROUND(AVG(s.avg_sentiment), 4) as average_emotional_score
    FROM listings l
    JOIN london_sentiment s ON l.id = s.listing_id
    WHERE l.city_name = 'LONDON'
      AND l.host_is_superhost IN ('t', 'f')
    GROUP BY l.host_is_superhost
    """
    
    print("\nAI Sentiment Analysis: Superhost vs. Standard Host")
    print("-" * 60)
    result = con.execute(query).fetchdf()
    
 
    result['is_superhost'] = result['is_superhost'].map({'t': 'Yes', 'f': 'No'})
    print(result.to_string(index=False))
    print("-" * 60)
    
    con.close()

if __name__ == "__main__":
    get_sentiment_insight()