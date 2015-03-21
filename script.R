#data <- read.csv("train.csv")

ari = matrix(data[972,2:785],nrow=28, ncol=28, byrow=TRUE)

sumMatrixRows <- function (m)   {
	sapply(1:28, function (row) {  
		sum(sapply(1:28, function (col) { 
			m[[row,col]] 
			} )) 
		})
}

sumMatrixColumns <- function (m)  {
	sapply(1:28, function (col) {
	  sum(sapply(1:28, function (row) {
	   m[[row,col]] 
	   } )) 
	  })
}

markChopPoints <- function (lst) {

	result = c()

	for (i in 1:length(lst)) {
		if (lst[[i]] != 0 ) {
			break

		}
		else {
			result <- c(result,-1*i)
		}
		
	}

	for(i in rev(1:length(lst))) {
		if (lst[[i]] != 0) {
			break
		}
		else {
			result <- c(result,-1*i)
		}
	}

	result
}

rowsToChop <- markChopPoints(sumMatrixRows(ari))
columnsToChop <- markChopPoints(sumMatrixColumns(ari))

print(ari[rowsToChop,columnsToChop])


