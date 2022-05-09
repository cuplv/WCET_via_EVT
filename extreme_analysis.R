library(extRemes)
library(evd)
library("Cairo")

args = commandArgs(trailingOnly=TRUE)
# args[1] --> path and name of input file (e.g., Dataset/Snapbuddy_timing.txt)
# args[2] --> threshold value (e.g., 15.6 for SnapBuddy)

namefile <- strsplit(args[1],"./")[[1]][2]
print(namefile)

if(namefile == "gabfeed_time.csv") {
   a <- read.csv(namefile, sep = ",")
   a <- as.matrix(a)
   aa <- as.vector(a)
   aa <- aa/1000000
} else {
   a <- read.csv(paste("./",args[1],sep = ''), sep = "\n", header=F)
   aa <- a$V1
   aa <- sample(aa,length(aa))
}

if(namefile == "Snapbuddy_timing.txt")
{
   aa <- a$V1/1000
} else if(namefile == "LogisticRegression_timing.txt") {
   aa <- a$V1/1000000
   aa <- unique(aa)   
} else if(namefile == "TreeRegressor_timing.txt") {
   # only consider execution times up to 100 seconds
   aa <- a$V1/1000000
   aa1 <- Filter(function(x){if(x >= 25) return(TRUE) else return(FALSE)}, aa)
   aa2 <- Filter(function(x){if(x < 25) return(TRUE) else return(FALSE)}, aa)
   aa1 <- unique(aa1)
   aa <- c(aa1,aa2)
   aa <- sample(aa,length(aa))
   aa <- aa[aa < 100]
}

start_time <- as.numeric(Sys.time())*1000

# mean residual plot
mrlplot(aa, nint = 10)

t_approx <- quantile(aa, c(.95, .997))
print("these are threshold for 95% and 99.7%")
print(t_approx)

t <- as.numeric(args[2])

end_time <- as.numeric(Sys.time())*1000
time1 <- end_time - start_time

final = paste("Figures/threshold_",namefile, ".png",sep = '')
Cairo(file=final,
      bg="white",
      type="png",
      units="in",
      width=12,
      height=9,
      pointsize=14,
      dpi=200)
par(mar=c(7, 6, 2,2) + 0.2)

plot(aa, type = "p", col = "darkblue", lwd = 1, cex.lab = 2, cex.axis = 2, font = 2, xlab = "Samples", ylab = "Execution Time")
abline(h = t, col = "red", lty=c(2), lwd=c(2))
points(which(aa > t, arr.ind = TRUE), aa[aa > t], col="red")
dev.off()

start_time <- as.numeric(Sys.time())*1000

if(namefile == "TreeRegressor_timing.txt") {
   fit1 <- fevd(aa, type = "PP", method = "Bayesian", threshold = t, time.units = "days", units = "Time", period.basis = "1 unit = 365 sample")
} else {
   fit1 <- fevd(aa, type = "PP", threshold = t, time.units = "days", units = "Time", period.basis = "1 unit = 365 sample")
}
distill(fit1)

end_time <- as.numeric(Sys.time())*1000
time2 <- end_time - start_time

final = paste("Figures/rl_",namefile, ".png",sep = '')
Cairo(file=final,
      bg="white",
      type="png",
      units="in",
      width=12,
      height=9,
      pointsize=14,
      dpi=200)
par(mar=c(7, 6, 2,2) + 0.2)

plot(fit1, "rl", rperiods = c(3, 6, 9, 15, 30, 45, 60), 
     main = "Return Values", lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)
dev.off()
#plot(fit1, "probprob")

final = paste("Figures/qq_",namefile, ".png",sep = '')
Cairo(file=final,
      bg="white",
      type="png",
      units="in",
      width=12,
      height=9,
      pointsize=14,
      dpi=200)
par(mar=c(7, 6, 2,2) + 0.2)

plot(fit1, "qq",main = "Empirical quantiles against model quantiles", lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)

dev.off()

final = paste("Figures/density_",namefile, ".png",sep = '')
Cairo(file=final,
      bg="white",
      type="png",
      units="in",
      width=12,
      height=9,
      pointsize=14,
      dpi=200)
par(mar=c(7, 6, 2,2) + 0.2)


plot(fit1, "density" , main = "Empirical density against model density", lwd = 2, cex.axis = 1, cex.lab = 2, font = 2)

dev.off()

print(paste("the length of array is", length(aa)))
print(paste("threshold is: ", t))
print(paste("computation time", time1 + time2))


# next 1,000; 2,000, 5,000, 10,000, 20,000, and 50,000 samples!
summary(fit1)

return.level(fit1)
return.level(fit1, do.ci=FALSE)
returns <- ci(fit1, return.period=c(2.73972602739726, 2*2.73972602739726, 5* 2.73972602739726, 10 * 2.73972602739726, 20 * 2.73972602739726, 50*2.73972602739726))
print(returns)

P = ecdf(fit1$x)
apply(returns, 2, function(x) P(x))
