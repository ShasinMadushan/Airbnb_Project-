import duckdb

def run_export():
    print("Exporting unified global data to Parquet...")
    con = duckdb.connect('data/processed/airbnb.duckdb')
    
    # Updated filename to accurately reflect our 3-city global dataset
    con.execute("COPY (SELECT * FROM listings) TO 'data/processed/global_listings.parquet' (FORMAT PARQUET)")
    
    con.close()
    print("Export complete! Unified file is at: data/processed/global_listings.parquet")

if __name__ == "__main__":
    run_export()