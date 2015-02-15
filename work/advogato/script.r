path <- ""
adv_data <- read.csv(path, TRUE, " ")
adv_data$Range[adv_data$Range > 2243] <- 2243