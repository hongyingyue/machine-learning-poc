
setwd('./00-Code/Visualization')
library("ggplot2")
library("ggthemes")
library("reshape2")
library("plyr")

Da<-read.csv("./data/binary_com.csv",sep=',',header=T)
Da<-data.frame(Da)

p<-ggplot(Da)+coord_flip()
p<-p+geom_segment(aes(Items,Label1,xend=Items,yend=Label2),linetype='solid',size=5,lineend='round',color='light blue')
p<-p+geom_point(aes(x=Items,y=Label1),color='blue',size=5,shape=16)
p<-p+geom_point(aes(x=Items,y=Label2),color='blue',size=5,shape=21,fill='white')
p<-p+geom_text(aes(x=Items,y=Label1,label=Label1),hjust=2)
p<-p+geom_text(aes(x=Items,y=Label2,label=Label2),hjust=-2)
p<-p+theme_wsj(color="brown")
ggsave("./outputs/Binary comparison.png", p, height=4.8, width=9.5,bg= "transparent")
