CK 的查询和SQL的兼容性还是蛮高的，先使用SQL，遇到问题或者特殊的需求再去对照文档就好了。


基础结构
```
select *from logs limit 1;

┌─cip───────────┬───────────────dtime─┬─method─┬─status─┬─cost─┬─bytes─┬─hit─┬──────ddate─┬─domain───────────┬─offload─┐
│ 58.215.118.62 │ 2018-08-27 01:00:02 │ POST   │    200 │  186 │   667 │   0 │ 2018-08-27 │ vcloud.000607.cn │ baidu   │
└───────────────┴─────────────────────┴────────┴────────┴──────┴───────┴─────┴────────────┴──────────────────┴─────────┘

```

## 时序数据

某段时间内，每个小时数据聚合, [文档](https://clickhouse.yandex/docs/en/query_language/functions/date_time_functions/)

```
select count(*), toHour(dtime) as date from logs where ddate = '2018-08-28' group by date;
```

每五分聚合
```
select count(*), toStartOfFiveMinute(dtime) as date from logs where ddate = '2018-08-28' group by date order by date;
```
