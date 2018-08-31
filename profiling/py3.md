性能分析
=====

尽可能简单，环境依赖少

## cProfile

最简单的是 cProfile

```
python -m cProfile -s cumtime handler.py

```
但是内容有点乱, 但是可以找出大概问题的位置


产生输出并做分析，分析的工具很多
```
python3.6 -m cProfile -o output.file run.py

python3.6 -m pstats output.file
# 这是一个交互式的引擎
output.file% help 
output.file% sort

# 然后可以先sort 然后 看排序
output.file% sort cumtime
output.file% stats 10

output.file% sort cumulative
output.file% stats 20
```

### qcachegrind

```
brew install qcachegrind --with-graphviz
sudo pip3.6 install pyprof2calltree

python -m cProfile -o <output_filename> <normal stuff here>
pyprof2calltree -i import.prof -o import.callgrind
pyprof2calltree -i import.prof -k
```




