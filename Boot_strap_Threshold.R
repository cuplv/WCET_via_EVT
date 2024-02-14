library(extRemes)
library(evd)
library("Cairo")
library(ggplot2)
library(MASS)

# True: IID; False: GB
# namefile <- "diff_costs_modExp_True_32.csv"
# namefile <- "diff_costs_modExp_False_32.csv"
# namefile <- "diff_costs_modExp_True_64.csv"
# namefile <- "diff_costs_modExp_False_64.csv"
# namefile <- "diff_costs_modExp_True_128.csv"
# namefile <- "diff_costs_modExp_False_128.csv"
# namefile <- "diff_costs_modExp_True_256.csv"
# namefile <- "diff_costs_modExp_False_256.csv"

# namefile <- "diff_costs_mod_pow_True_32.csv"
# namefile <- "diff_costs_mod_pow_False_32.csv"
# namefile <- "diff_costs_mod_pow_True_64.csv"
# namefile <- "diff_costs_mod_pow_False_64.csv"
# namefile <- "diff_costs_mod_pow_True_128.csv"
# namefile <- "diff_costs_mod_pow_False_128.csv"
# namefile <- "diff_costs_mod_pow_True_256.csv"
# namefile <- "diff_costs_mod_pow_False_256.csv"

# namefile <- "diff_costs_password_True_32.csv"
# namefile <- "diff_costs_password_False_32.csv"
# namefile <- "diff_costs_password_True_64.csv"
# namefile <- "diff_costs_password_False_64.csv"
# namefile <- "diff_costs_password_True_128.csv"
namefile <- "diff_costs_password_False_128.csv"
# namefile <- "diff_costs_password_True_256.csv"
# namefile <- "diff_costs_password_False_256.csv"

a <- read.csv(namefile)

aa <- sample(a$X0, length(a$X0))
# mean residual plot

# mrlplot(a)

# if the main analysis failed, reduce by 0.5 (quantile(aa, seq(0.75, 0.997, by=0.01)))
t_approx <- quantile(aa, seq(0.999, 0.75, by=-0.001))
# if the main analysis failed, reduce this by 50 (seq(950, 750, by=-50)). 
thresholds <- seq(950, 750, by=-50)
best_shape <- 10.0
best_scale <- 1000000.0
best_shape_threshold <- 0.0
best_scale_threshold <- 0.0

for(tr in thresholds)
{
  prev_observed = 0.0
  for(x in t_approx) {
    print("----------------------------------------")
    if(prev_observed == x)
    {
      next
    }
    else
    {
      prev_observed <- x
    }
    print(x)
    exceedances <- aa[aa > x] - x
    
    n_bootstrap <- 1000
    shape_estimates <- numeric(n_bootstrap)
    scale_estimates <- numeric(n_bootstrap)
    
    for(i in 1:n_bootstrap) {
      # Sample exceedances with replacement
      bootstrap_sample <- sample(exceedances, length(exceedances), replace = TRUE)
      
      # Fit GPD to bootstrap sample
      fit <- try(fpot(bootstrap_sample, model = "gpd", threshold = 0), silent = TRUE)  # Note: threshold is 0 because we've already subtracted it
      
      scale_estimates[i] <- try(fit$estimate[1], silent = TRUE)
      shape_estimates[i] <- try(fit$estimate[2], silent = TRUE)
    }
    
    # Analyze the results
    scale_estimates <- as.double(scale_estimates[scale_estimates!="Error in fit$estimate : $ operator is invalid for atomic vectors\n"])
    shape_estimates <- as.double(shape_estimates[shape_estimates!="Error in fit$estimate : $ operator is invalid for atomic vectors\n"])
    
    if(length(scale_estimates) < tr)
    {
      next
    }
    mean_shape <- mean(shape_estimates)
    sd_shape <- sd(shape_estimates)
    conf_interval_shape <- quantile(shape_estimates, c(0.025, 0.975))
    
    mean_scale <- mean(scale_estimates)
    sd_scale <- sd(scale_estimates)
    conf_interval_scale <- quantile(scale_estimates, c(0.025, 0.975))
    
    cat("Shape Parameter Estimates:\n")
    cat("Mean:", mean_shape, "\n")
    cat("SD:", sd_shape, "\n")
    cat("95% CI:", conf_interval_shape, "\n")
    cat("CI Diff:", conf_interval_shape[2] - conf_interval_shape[1], "\n\n")
    CI_shape_diff <- conf_interval_shape[2] - conf_interval_shape[1]
    
    cat("Scale Parameter Estimates:\n")
    cat("Mean:", mean_scale, "\n")
    cat("SD:", sd_scale, "\n")
    cat("95% CI:", conf_interval_scale, "\n")
    cat("CI diff:", conf_interval_scale[2] - conf_interval_scale[1], "\n")
    CI_interval_diff <- conf_interval_scale[2] - conf_interval_scale[1]
    
    if(CI_shape_diff < best_shape){
      best_shape <- CI_shape_diff
      best_shape_threshold <- c(x, conf_interval_shape[1], conf_interval_shape[2])
    }
    if(CI_interval_diff < best_scale)
    {
      best_scale <- CI_interval_diff
      best_scale_threshold <- c(x, conf_interval_scale[1], conf_interval_scale[2])
    }
    print("----------------------------------------")
  }
  cat("Threshold of selecting:", tr,"\n")
  cat("Best Parameter and Values:\n")
  cat("best_shape:", best_shape, "\n")
  cat("best_shape_threshold:", best_shape_threshold, "\n")
  cat("best_scale:", best_scale, "\n")
  cat("best_scale_threshold:", best_scale_threshold, "\n")
  if(best_scale < 1000000.0)
  {
    break
  }
}