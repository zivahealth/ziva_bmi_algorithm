# Import libraries
library(ggplot2)

# Read data, convert categorical variables to factor type
scoring_data <- read.csv("./../../data/processed/scoring_data.csv")
scoring_data$age <- as.factor(scoring_data$age)
scoring_data$sex <- as.factor(scoring_data$sex)


for (sex_group in unique(scoring_data$sex)) {
  # Define values for visualization subtitle
  if (sex_group == 1) {
    sex_val <- "Female"
  }
  else {
    sex_val <- "Male"
  }
  
  # Subset dataframe by sex
  sub_df <- scoring_data[scoring_data$sex == sex_group,]
  
  # Create visualization
  comp_plot <- ggplot(data = sub_df, mapping = aes(x = bfp)) +
    geom_line(aes(y = score, color = age)) + 
    scale_color_discrete(labels = c("20-29", "30-39", "40-49", "50-59", "60-69")) +
    labs(
      title = "Body Fat Pct vs Health Score",
      subtitle = paste(sex_val, "at birth"),
      x = "Body Fat Percentage",
      y = "Health Score (scaled 0 to 1)",
      color = "Age Range"
    ) +
    scale_x_continuous(breaks = c(0, 20, 40, 60), labels = c("0%", "20%", "40%", "60%"))

  # Print plot
  print(comp_plot)
  }




