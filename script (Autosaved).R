function sumMatrixRows (m) {sapply(1:28, function (row) {  sum(sapply(1:28, function (col) { m[[row,col]] } )) })}

function sumMatrixColumns(m) {
	sapply(1:28, function (col) {  sum(sapply(1:28, function (row) { m[[row,col]] } )) })
}