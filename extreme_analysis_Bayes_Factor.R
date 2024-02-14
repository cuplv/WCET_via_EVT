library(extRemes)
library(evd)
library("Cairo")
library(ggplot2)
library(MASS)

args = commandArgs(trailingOnly=TRUE)
# args[1] --> path and name of input file (e.g., Dataset/Snapbuddy_timing.txt)
# args[2] --> threshold value (e.g., 15.6 for SnapBuddy) // by default 0.95 quantile of data


# Linear SVM
# args[1] <- "Dataset/Linear_SVM_Bank_9042.txt"
# args[1] <- "Dataset/Linear_SVM_Bank_18084.txt"
# args[1] <- "Dataset/Linear_SVM_Bank_27126.txt"
# args[1] <- "Dataset/Linear_SVM_Bank_36168.txt"
# args[1] <- "Dataset/Linear_SVM_Bank_44758.txt"
# Bayes_Test <- TRUE
# ind_max = 500
# pos_shape <- FALSE

# args[1] <- "Dataset/Linear_SVM_Census_6512.txt"
# args[1] <- "Dataset/Linear_SVM_Census_13024.txt"
# args[1] <-"Dataset/Linear_SVM_Census_19536.txt"
# args[1] <- "Dataset/Linear_SVM_Census_26048.txt"
# args[1] <- "Dataset/Linear_SVM_Census_32235.txt"
# Bayes_Test <- TRUE
# ind_max = 500
# pos_shape <- FALSE

namefile <- strsplit(args[1],"./")[[1]][2]
print(namefile)

a <- read.csv(paste("./",args[1],sep = ''), sep = "\n", header=F)

count = -1
ind = 2
max_observed = a$V1[1]
max_index = 1
if(Bayes_Test)
{
  while(count <= 90)
  {
    if(ind > 500)
    {
      count = -1
      print("failed to find any value.")
      break
    }
    else if(a$V1[ind] > max_observed)
    {
      count = 0
      max_observed = a$V1[ind]
      max_index = ind
    }
    else
    {
      count = count + 1
    }
    ind = ind + 1
  }
}else{
  max_observed = max(a$V1[1:ind_max], na.rm = TRUE)
  max_index = ind_max
}

if(ind <= 500 && count != -1 && Bayes_Test)
{
  ind_max = ind
}

Not_Valid = TRUE

start_time <- as.numeric(Sys.time())*1000

while (Not_Valid) {
  aa <- a$V1
  # for the Linear SVM experiemtns, choose the first 1000 data samples.
  for(i in seq(ind_max, 10, -1.0))
  {
    aa <- aa[1:i]
    if(max(a$V1, na.rm = TRUE) != max(aa, na.rm = TRUE))
      break
  }
  ind_max = ind_max + 100
  aa <- sample(aa,length(aa))
  t_seq <- seq(quantile(aa, c(.95, .997))[2], quantile(aa, c(0.5,.95))[1], by=-1.0)

  # mean residual plot
  # mrlplot(aa, nint = 10)
  
  # Range between shape and scale!
  for (t in t_seq){
    start_time <- as.numeric(Sys.time())*1000
    # Bayesian approach
    # fit <- fevd(aa, type = "PP", method = "Bayesian", threshold = t, time.units = "days", units = "Time", period.basis = "1 unit = 365 sample")
    
    # GP or PP
    type_name = "GP"
    fit <- try(fevd(aa, type = type_name, threshold = t, time.units = "days", units = "Time", period.basis = "1 unit = 365 sample"), silent = TRUE)
    
    try(distill(fit), silent = TRUE)
    
    end_time <- as.numeric(Sys.time())*1000
    time2 <- end_time - start_time
    
    fit$period.basis <- "1 unit = 365 sample" 
    
    gauss <- fitdistr(aa, "normal")
    
    # next 1,000; 2,000, 5,000, 10,000, 20,000, and 50,000 samples!
    summary(fit)
    
    print(paste("the length of array 0 is", length(aa)))
    print(paste("threshold_0 is : ", t))
    print(paste("num. items over threshold t : ", length(aa[aa > t])))
    print(paste("computation time", time2))
    print(paste("The mean and std=:", gauss$estimate))
    print(paste("The error for mean and std:", gauss$sd))
    
    try(return.level(fit), silent = TRUE)
    try(return.level(fit, do.ci=FALSE), silent = TRUE)
    returns <- try(ci(fit, return.period=c(0.5 * 2.73972602739726, 2.73972602739726, 2*2.73972602739726, 5* 2.73972602739726, 10 * 2.73972602739726, 20 * 2.73972602739726, 50*2.73972602739726)), silent = TRUE)
    print(returns)
    if(length(returns) < 18 || is.nan(returns[18]) || returns[1] < 0 || returns[2] < 0 || returns[3] < 0 
       || returns[4] < 0 || returns[5] < 0 || returns[6] < 0 || returns[13] < 0 || returns[14] < 0 
       || returns[15] < 0 || returns[16] < 0 || returns[17] < 0 || returns[18] < 0
       || (returns[1] >  returns[2] && returns[2] >  returns[3]) 
       || (returns[3] >  returns[4] && returns[4] >  returns[5])
       || (returns[13] > returns[14] && returns[14] > returns[15])
       || (returns[14] > returns[15] && returns[15] > returns[16])
       || (returns[16] > returns[17] && returns[17] > returns[18])
    )
    {
      print("Not Valid---here1")
      print("--------------------------")
      next
    }
    else
    {
      if(pos_shape)
      {
        if(fit$results$par[2] <= -0.05 || fit$results$par[2] >= 0.05)
        {
          print("Not Valid---here2")
          print("--------------------------")
          next
        }
      }
      else
      {
        # this should be chosen judiciously: some possible values are 0.01, 0.05, 0.08, 0.1, 0.2
        if(fit$results$par[2] > 0.1 || fit$results$par[2] < 0.00001)
        {
          print("Not Valid---here3")
          print("--------------------------")
          next
        }
      }
      print(returns)
      
      P = ecdf(fit$x)
      apply(returns, 2, function(x) P(x))
      print("--------------------------")
      Not_Valid = FALSE
      final = paste("./Figures/threshold_",namefile, ".png",sep = '')
      Cairo(file=final,
            bg="white",
            type="png",
            units="in",
            width=12,
            height=9,
            pointsize=14,
            dpi=100)
      par(mar=c(7, 6, 2,2) + 0.2)
      
      plot(aa, type = "p", col = "blue", lwd = 1, cex.lab = 2, cex.axis = 2, font = 2, xlab = "Samples", ylab = "Cost")
      abline(h = t, col = "red", lty=c(2), lwd=c(2))
      points(which(aa > t, arr.ind = TRUE), aa[aa > t], col="red")
      dev.off()

      final = paste("./Figures/rl_",namefile, "_", ".png",sep = '')
      Cairo(file=final,
            bg="white",
            type="png",
            units="in",
            width=12,
            height=9,
            pointsize=14,
            dpi=100)
      par(mar=c(7, 6, 2,2) + 0.2)
      
      plot(fit, "rl", rperiods = c(3, 6, 9, 15, 30, 45, 60), col = "blue",
           main = paste("Return Values"), lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)
      dev.off()
      
      
      final = paste("./Figures/qq_",namefile, ".png",sep = '')
      Cairo(file=final,
            bg="white",
            type="png",
            units="in",
            width=12,
            height=9,
            pointsize=14,
            dpi=100)
      par(mar=c(7, 6, 2,2) + 0.2)
      
      plot(fit, "qq",main = paste("Empirical quantiles against model quantiles"), col = "blue", lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)
      
      dev.off()
      
      fit$period.basis <- ""
      
      final = paste("./Figures/density_",namefile, ".png",sep = '')
      Cairo(file=final,
            bg="white",
            type="png",
            units="in",
            width=12,
            height=9,
            pointsize=14,
            dpi=100)
      par(mar=c(7, 6, 2,2) + 0.2)
      
      plot(fit, "density", sub = "", main = "", xlab = "Execution Times", col=c("black","blue"), lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)
      dev.off()
      
      break
    }
  }  
}


print("Bayesian Factor Method:")
print(ind)
print(max_index)
print(max_observed)
print("--------------------------")
print("Actual observed Time:")
# what are actual timing after these steps:
for(i in c(500, 1000, 2000, 3000, 4000, 5000, 10000))
{
  print(i)
  j <- i + ind_max
  print(max(a$V1[1:j], na.rm = TRUE))
}
