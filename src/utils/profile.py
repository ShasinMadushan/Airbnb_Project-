import pandas as pd


FILES = {
    "listings": "data/raw/london_listings.csv.gz",
    "calendar": "data/raw/london_calendar.csv.gz",
    "reviews": "data/raw/london_reviews.csv.gz"
}

def peek_data(name, path):
    print(f"\n--- Profiling {name.upper()} ---")
    try:
        
        df = pd.read_csv(path, nrows=5, compression='gzip')
        print(f"Columns: {len(df.columns)}")
        print(f"Sample Columns: {list(df.columns)[:5]}...")
        
        
        chunk_iter = pd.read_csv(path, chunksize=100000, compression='gzip', usecols=[0])
        total_rows = sum(len(chunk) for chunk in chunk_iter)
        print(f"Total Rows: {total_rows:,}")
        
    except Exception as e:
        print(f"Error reading {name}: {e}")

def main():
    for name, path in FILES.items():
        peek_data(name, path)

if __name__ == "__main__":
    main()