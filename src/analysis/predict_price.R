
library(DBI)
library(duckdb)
library(randomForest)
library(Metrics)

run_ml_pipeline <- function(target_city) {
  cat(sprintf("\n=============================================\n"))
  cat(sprintf("ML Pipeline for %s...\n", target_city))
  cat(sprintf("=============================================\n\n"))
  

  con <- dbConnect(duckdb::duckdb(), dbdir = "Desktop/Airbnb_Project/data/processed/airbnb.duckdb", read_only = TRUE)
  query <- sprintf("
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
        AND city_name = '%s'
  ", target_city)
  
  df <- dbGetQuery(con, query)
  dbDisconnect(con)
  
  cat(sprintf("Data extracted: %d records.\n", nrow(df)))
  

  df$bedrooms[is.na(df$bedrooms)] <- median(df$bedrooms, na.rm = TRUE)
  df$beds[is.na(df$beds)] <- median(df$beds, na.rm = TRUE)
  df$review_scores_rating[is.na(df$review_scores_rating)] <- mean(df$review_scores_rating, na.rm = TRUE)
  
  df$host_is_superhost[is.na(df$host_is_superhost)] <- 'f' 
  df$host_is_superhost <- as.factor(ifelse(df$host_is_superhost == 't', 1, 0))
  df$room_type <- as.factor(df$room_type)
  
  df <- na.omit(df)
  
  cat(sprintf("Clean data ready for ML: %d records.\n", nrow(df)))
  

  set.seed(42)
  sample_index <- sample(seq_len(nrow(df)), size = 0.8 * nrow(df))
  train_data <- df[sample_index, ]
  test_data <- df[-sample_index, ]
  

  cat("Training Random Forest Model...\n")
  rf_model <- randomForest(
    price ~ ., 
    data = train_data, 
    ntree = 50, 
    maxnodes = 50, 
    importance = TRUE
  )

  predictions <- predict(rf_model, test_data)
  rmse_val <- rmse(test_data$price, predictions)
  mae_val <- mae(test_data$price, predictions)
  

  cat(sprintf("Root Mean Squared Error (RMSE): GBP%.2f\n", rmse_val))
  cat(sprintf("Mean Absolute Error (MAE): GBP%.2f\n", mae_val))
  

  cat("Generating Feature\n")
  if (!dir.exists("dashboard")) {
    dir.create("dashboard")
  }
  
  plot_filename <- sprintf("dashboard/feature_importance_%s.png", tolower(target_city))
  png(plot_filename, width = 800, height = 600)
  varImpPlot(rf_model, main = sprintf("Feature Importance for Airbnb Pricing (%s)", target_city))
  invisible(dev.off())
  
  cat(sprintf("Plot saved to '%s'\n", plot_filename))
}


run_ml_pipeline("LONDON")
run_ml_pipeline("TOKYO")

