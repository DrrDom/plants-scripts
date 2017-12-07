# analysis of collected bestranking data by collect_grid_dock_data.py

library(dplyr)

get_clusters <- function(coords_df, threshold = 2) {
  i <- 1
  clusters <- rep(0, nrow(coords_df))
  m <- as.matrix(dist(coords_df))
  while(any(clusters == 0)) {
    j <- which.min(clusters)
    clusters[(m[j,] < threshold) & (clusters == 0)] <- i
    i <- i + 1
  }
  return(clusters)
}

d <- data.table::fread("~/IMTM/eEF2/5xjc/all_scores_py.txt", sep="\t", data.table = F)
colnames(d)[(ncol(d) - 3):ncol(d)] <- c("score", "x", "y", "z")

d <- d %>% arrange(V2, score)

s <- lapply(split(d, d$V2), function(s) {
  cbind(s, cluster = get_clusters(s[, c("x", "y", "z")]))
})


ss <- lapply(s, function(x) {
  x %>% filter(score - min(score) < 5) %>% group_by(cluster) %>% slice(1)
})

ss <- lapply(ss, function(x) {
  if (x[1, "score"] < -78) {
    return(x)
  } else {
    return(NULL)
  }
})

ss <- ss[!sapply(ss, is.null)]


for (df in ss) {
  for (i in 1:nrow(df)) {
    dname <- paste0("~/IMTM/eEF2/5xjc/best_dock/", sub(".*_([a-zA-Z])$", "\\1", df[i, "V2"]), "_", df[i, "V4"], "_", df[i, "score"])
    dir.create(dname, recursive = T)
    from_dir <- paste("~/IMTM/eEF2/5xjc/", df[i, 2], df[i, 3], df[i, 4], sep = "/")
    flist <- list.files(from_dir, "*", full.names = T)
    file.copy(flist, dname)
  }
}


