import duckdb

def run_export():
    print("Exporting data to Parquet...")
    con = duckdb.connect('data/processed/airbnb.duckdb')
    # This command creates the file Power BI can read easily
    con.execute("COPY (SELECT * FROM listings) TO 'data/processed/london_listings.parquet' (FORMAT PARQUET)")
    print("Export complete! File is at: data/processed/london_listings.parquet")

if __name__ == "__main__":
    run_export()