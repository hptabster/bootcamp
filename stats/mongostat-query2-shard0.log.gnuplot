set title "MongoDB 2.4.6 YCSB Performance Graph"
set xlabel "Time (seconds)"
set ylabel "Hits per sec"
set y2label "Lock %"

set y2range [0:100]
set y2tics border

set terminal png large
set style data linespoints
set output 'mongostat-query2-shard0.log.png'

set datafile separator ','

DATA_FILE = 'mongostat-query2-shard0.log.csv'

# plot '<csv_filename>' using '<column_name_in_first_line_of_csv>' title '<line_name>', ...
plot DATA_FILE using 'insert' title 'Insert', DATA_FILE using 'update' title 'Update', DATA_FILE using 'query' title 'Query', DATA_FILE using 'locked db' axes x1y2 title 'Locked DB %'
