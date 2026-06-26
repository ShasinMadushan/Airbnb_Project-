# Load libraries
library(DBI)
library(duckdb)
library(randomForest)
library(Metrics)

cat("Initializing ML Pipeline in R...\n\n")

# 1. Extract Data from DuckDB
con <- dbConnect(duckdb::duckdb(), dbdir = "Desktop/Airbnb_Project/data/processed/airbnb.duckdb", read_only = TRUE)
query <- "
    SELECT 
        price, 
        room_type, 
        host_is_superhost, 
        accommodates, 
        bedrooms, 
        beds, 
        number_of_reviews, 
        review_scores_rating
    FROM listings
    WHERE price IS NOT NULL 
      AND price < 1000
"
df <- dbGetQuery(con, query)
dbDisconnect(con)

cat(sprintf("Data extracted: %d records.\n", nrow(df)))

# 2. Feature Engineering & Preprocessing
# Handle known missing values
df$bedrooms[is.na(df$bedrooms)] <- median(df$bedrooms, na.rm = TRUE)
df$beds[is.na(df$beds)] <- median(df$beds, na.rm = TRUE)
df$review_scores_rating[is.na(df$review_scores_rating)] <- mean(df$review_scores_rating, na.rm = TRUE)

# Handle potential NAs in Superhost before converting
df$host_is_superhost[is.na(df$host_is_superhost)] <- 'f' 
df$host_is_superhost <- as.factor(ifelse(df$host_is_superhost == 't', 1, 0))
df$room_type <- as.factor(df$room_type)

# THE FIX: Drop any remaining rows with NAs
df <- na.omit(df)

cat(sprintf("Clean data ready for ML: %d records.\n", nrow(df)))

# Train/Test Split (80/20)
set.seed(42)
sample_index <- sample(seq_len(nrow(df)), size = 0.8 * nrow(df))
train_data <- df[sample_index, ]
test_data <- df[-sample_index, ]

# 3. Model Training
cat("Training Random Forest Model...\n")
rf_model <- randomForest(
  price ~ ., 
  data = train_data, 
  ntree = 50, 
  maxnodes = 50, 
  importance = TRUE
)

# 4. Evaluation
predictions <- predict(rf_model, test_data)
rmse_val <- rmse(test_data$price, predictions)
mae_val <- mae(test_data$price, predictions)

cat("\nModel Performance:\n")
cat(sprintf("Root Mean Squared Error (RMSE): $%.2f\n", rmse_val))
cat(sprintf("Mean Absolute Error (MAE): $%.2f\n", mae_val))

# 5. Model Explainability
cat("\n Generating Feature Importance Plot...\n")

if (!dir.exists("dashboard")) {
  dir.create("dashboard")
}

png("dashboard/feature_importance_R.png", width = 800, height = 600)
varImpPlot(rf_model, main = "Feature Importance for Airbnb Pricing (London)")
invisible(dev.off())

cat("Plot saved to 'dashboard/feature_importance_R.png'\n")

