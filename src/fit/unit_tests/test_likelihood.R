# For commparing to values calculated by R
# 
# Author: floha
###############################################################################


library(mvtnorm)
sigma = matrix(c(1,0.5,0.5,1),2)
-dmvnorm(c(0,0), sigma=sigma, log=T)
-dmvnorm(c(1,1), sigma=sigma, log=T)
-dmvnorm(c(3,3), sigma=sigma, log=T)

sigma = matrix(c(1,0.1,0.1,3),2)
-dmvnorm(c(1,1), sigma=sigma, log=T)
