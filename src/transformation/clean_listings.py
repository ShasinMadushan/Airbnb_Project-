import pandas as pd
import duckdb

def process_multiple_cities():
    cities = {
        'london': {'file': 'london_listings.csv.gz', 'currency_rate': 1.0},    # Base GBP
        'tokyo': {'file': 'tokyo_listings.csv.gz', 'currency_rate': 190.0},  # ~190 JPY to 1 GBP
        'nyc': {'file': 'nyc_listings.csv.gz', 'currency_rate': 1.25}        # ~1.25 USD to 1 GBP
    }
    
    all_cleaned_data = []
    print("Starting Global ELT Pipeline...")

    for city, config in cities.items():
        file_path = f"data/raw/{config['file']}"
        print(f"Processing {city.upper()}...")
        
        df = pd.read_csv(file_path, low_memory=False)
        
        df['city_name'] = city.upper()
        
        df = df.dropna(subset=['price']) 
        
        if df['price'].dtype == 'O':
            df['price'] = df['price'].replace({r'\$': '', r'£': '', r'¥': '', r',': ''}, regex=True).astype(float)
            
        if config['currency_rate'] != 1.0:
            print(f"   Converting currency to Base (£)...")
            df['price'] = df['price'] / config['currency_rate']
        
        all_cleaned_data.append(df)

    master_df = pd.concat(all_cleaned_data, ignore_index=True)
    print(f"Global Dataset Ready: {len(master_df)} total rows.")

    con = duckdb.connect('data/processed/airbnb.duckdb')
    con.execute("CREATE OR REPLACE TABLE listings AS SELECT * FROM master_df")
    con.close()
    
    print("Multi-City Data successfully saved to DuckDB")

if __name__ == "__main__":
    process_multiple_cities()