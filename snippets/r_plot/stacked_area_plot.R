#To be updated: use + theme_bw()

# setwd('./06-QFS_month')

library(reshape2)
library(ggplot2)
library(gridExtra)

Fre<-read.table("QFS_monthly_prognosis1.csv",sep=',',header=T)
Fre$Time<-format(as.Date(paste(Fre$Time,".01"),"%Y%m .%d"),format="%y-%m") 
DA1<-melt(Fre,id.vars="Time",variable.name="Frequency",value.name="Complaints_per_hundred")
DA1<-data.frame(DA1)
colors1<-c("grey","blue","light green","pink")
p1<-ggplot(DA1,aes(x=Time,y=Complaints_per_hundred,fill=Frequency,group=Frequency))+
geom_area(alpha=0.5,position='stack',color='black',size =0.1)+scale_fill_manual(values = colors1)
p1<-p1+xlab("Complaint Month")
p1<-p1+scale_y_continuous("Complaint Rate [%]",labels=scales::percent)
p1<-p1+theme(axis.text.y = element_text(size = 12),axis.text.x =  element_text(size = 12))
p1<-p1+theme(axis.title.y = element_text(size = 12),axis.title.x =  element_text(size = 12))
p1<-p1+theme(axis.line.x = element_line(color="black", size = 0.3),axis.line.y = element_line(color="black", size = 0.3))
p1<-p1+theme(legend.justification=c(0.04,0.95),legend.position=c(0.04,0.95),panel.grid.major=element_blank())
p1<-p1+theme(legend.background = element_rect(fill=alpha('white', 0.1)),legend.text=element_text(size=6),legend.key.size=unit(0.4,'cm'),legend.key.width=unit(0.4,'cm'))
p1<-p1+theme(legend.title=element_blank())+annotate("rect", xmin="18-12", xmax="19-06", ymin=0, ymax=Inf, alpha=0.22, fill="grey")
ggsave("plot.png", p1, height=4.2, width=8.5)





