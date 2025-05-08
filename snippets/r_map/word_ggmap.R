library(maps)
library(ggplot2)

map = map_data("world")
ggplot(map, aes(long, lat, group=group)) +
  geom_polygon(fill="white", colour="gray") +
  ggtitle("Map of World")