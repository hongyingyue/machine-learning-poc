setwd('./Visualization')
library(rworldmap)
Market<-read.table("./data/map_R_world.csv",header=T,sep=',',skip=2)
Market<-data.frame(Market)
names(Market)<-c("Country_code","Market","Metrics","Claims","Production_number","Complaint_rate")
Market$Production_number<-as.numeric(Market$Production_number)
Market<-Market[order(-Market$Production_number),]
#Market<-Market[1:20,]
Market$Market<-gsub("Korea (South)","South Korea",Market$Market)  #Not working!!!!

SPDF<-joinCountryData2Map(Market,joinCode='NAME',nameJoinColumn='Market')
mapBubbles(SPDF, nameZSize="Complaint_rate",nameZColour="red",oceanCol="lightblue",landCol="beige")

identifyCountries(getMap(), nameColumnToPlot="category")   #click the country to add the lable

#change the columns name of 'Salesmarket' and 'Complaint_rate', change the percentage to number, change to 'South Korea'