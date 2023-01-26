# Import libraries
library(ggplot2)
library(caret)

# Read data, convert categorical variables to factor type
scoring_data <- read.csv("./../../data/processed/scoring_data.csv")
scoring_data$age <- as.factor(scoring_data$age)
scoring_data$sex <- as.factor(scoring_data$sex)

# Train polynomial regression model
lm_poly7 <- lm(score ~ poly(bfp, 7, raw=TRUE) + age + sex, data=scoring_data)

# Save coefficients
write.csv(lm_poly7$coefficients, file = "./../../models/lm_poly7_coeffs.csv")

# Generate and save predictions
scoring_data$preds <- predict(lm_poly7, scoring_data[c("bfp", "age", "sex")])

for (age_group in unique(scoring_data$age)) {
  for (sex_group in unique(scoring_data$sex)) {
    # Define subgroup dataframe
    sub_df <- scoring_data[scoring_data$age == age_group & 
                             scoring_data$sex == sex_group,]
    
    
    # Define values for visualization
    if (sex_group == 1) {
      sex_val <- "Female"
    }
    else {
      sex_val <- "Male"
    }
    
    if (age_group == 0) {
      age_val <- "Twenties"
    }
    else if (age_group == 1) {
      age_val <- "Thirties"
    }
    else if (age_group == 2) {
      age_val == "Forties"
    }
    else if (age_group == 3) {
      age_val == "Fifties"
    }
    else {
      age_val == "Sixties"
    }
    
    # Create visualizations
    comp_plot <- ggplot(data = sub_df, mapping = aes(x = bfp)) +
      geom_line(aes(y = score), color="darkblue") +
      geom_line(aes(y = preds), color = "red")
    
    print(comp_plot)
  }
}




