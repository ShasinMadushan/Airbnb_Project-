# Install required packages if you don't have them
# install.packages(c("duckdb", "DBI", "effsize"))

library(DBI)
library(duckdb)
library(effsize)

cat("--- Running Statistical Analysis in R ---\n\n")

# Connect to your existing DuckDB database
con <- dbConnect(duckdb::duckdb(), dbdir = "Desktop/Airbnb_Project/data/processed/airbnb.duckdb", read_only = TRUE)


# ---------------------------------------------------------
# Hypothesis 1: Entire homes cost more than Private rooms
# ---------------------------------------------------------
cat("Hypothesis 1: Entire-home listings command higher prices than private rooms.\n")
df_h1 <- dbGetQuery(con, "
    SELECT room_type, price 
    FROM listings 
    WHERE room_type IN ('Entire home/apt', 'Private room')
    AND price IS NOT NULL
")

entire_homes <- df_h1$price[df_h1$room_type == 'Entire home/apt']
private_rooms <- df_h1$price[df_h1$room_type == 'Private room']

# Run Welch Two Sample t-test
t_test_1 <- t.test(entire_homes, private_rooms)
# Calculate Cohen's d (Effect Size)
effect_1 <- cohen.d(entire_homes, private_rooms)

print(t_test_1)
cat("Cohen's d:", effect_1$estimate, "\n\n")

# ---------------------------------------------------------
# Hypothesis 2: Superhosts get higher review scores
# ---------------------------------------------------------
cat("Hypothesis 2: Superhost listings achieve higher review scores than non-superhosts.\n")
df_h2 <- dbGetQuery(con, "
    SELECT host_is_superhost, review_scores_rating 
    FROM listings 
    WHERE host_is_superhost IN ('t', 'f')
    AND review_scores_rating IS NOT NULL
")

superhosts <- df_h2$review_scores_rating[df_h2$host_is_superhost == 't']
standard_hosts <- df_h2$review_scores_rating[df_h2$host_is_superhost == 'f']

t_test_2 <- t.test(superhosts, standard_hosts)
effect_2 <- cohen.d(superhosts, standard_hosts)

print(t_test_2)
cat("Cohen's d:", effect_2$estimate, "\n\n")

# Disconnect
dbDisconnect(con)
# 
