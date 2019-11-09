tst2 <- read.csv("D:\\Progetti_python\\Verona\\Sentinel1\\Databases_tutti\\SpeckleMultiTimeSeriesVV_originali.csv",row.name = 1, header = 1, check.names=FALSE, sep = ";",  dec = ",")
sc <- tst2[2:length(tst2)]
Prova<- as.data.frame(t(sc))

vars <- colnames(Prova)
## covariate
id <- 1:nrow(Prova)
## define a loess filter function (fitting loess regression line)
loess.filter <- function (x, span)  predict(loess(formula = paste(x, "id", sep = "~"),
                                         data = Prova,
                                         span = span))

## apply filter column-by-column
new.dat2 <- as.data.frame(lapply(vars, loess.filter, span = 0.30),
                         col.names = vars)

data=t(new.dat2)
colnames(data) <- colnames(sc)
tst3 <- tst2[1]
data2 <- cbind(tst3,data)


write.table(data2,"D:\\Progetti_python\\Verona\\Sentinel1\\Databases_tutti\\TutteDate\\BackscatterVVcomplete30_2.csv", sep = ";",dec = ",")


rownames(new.dat) <- rownames(Prova)

new.dat2 <- as.data.frame(lapply(vars, loess.filter, span = 0.30),
                          col.names = colnames())

new.dat3 <- new.dat[,1:10]
rownames(new.dat) <- rownames(Prova)


plot( new.dat$S1, x=date_serie, type="l", main="Loess Smoothing and Prediction", xlab="Date", ylab="S1 ")
lines(new.dat$S2, x=date_serie, col="red")
lines(new.dat$S3, x=date_serie, col="green")
lines(new.dat$S4, x=date_serie, col="blue")
legend(x= "topright",y=0.92,legend=c("2", "3" , "4"),
       col=c("red","green", "blue"),lty=1:2, cex=0.8)

plot.ts(new.dat3, plot.type = "single",  auto.legend = TRUE)


plot(new.dat3, plot.type="single", col = 1:ncol(new.dat3))

a <- ts(new.dat3, start = 05/01/2018, frequency = 1)

plot(a, plot.type="single", col = 1:ncol(a))
legend("bottomleft", colnames(a), col=1:ncol(a), lty=1, cex=.65)