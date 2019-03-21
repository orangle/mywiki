py3 asyncio
=========

> 执行原理，多进程和多线程怎么结合？

* 协程原理 http://www.dabeaz.com/coroutines/Coroutines.pdf



## 场景 一

cpu和io混合型，例如边计算，边入数据库，入库的IO操作，占了比较长的时间，怎么减少总时间？

用例设计：一个程序同时做2个事情，比如做累加计算一轮之后，请求一个http地址（http延迟返回)



