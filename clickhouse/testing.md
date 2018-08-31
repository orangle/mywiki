test case  https://clickhouse.yandex/docs/en/getting_started/example_datasets/ontime/ 下载了一部分数据做测试

看看原始数据大小
```
$ for i in *.zip; do echo $i; unzip -cq $i '*.csv' | sed 's/\.00//g' >> merge.csv ; done
$ ls -lsh merge.csv
6.0G -rw-rw-r-- 1 liuzz liuzz 6.0G Aug 27 23:34 merge.csv

$ head -n 2 merge.csv
"Year","Quarter","Month","DayofMonth","DayOfWeek","FlightDate","UniqueCarrier","AirlineID","Carrier","TailNum","FlightNum","OriginAirportID","OriginAirportSeqID","OriginCityMarketID","Origin","OriginCityName","OriginState","OriginStateFips","OriginStateName","OriginWac","DestAirportID","DestAirportSeqID","DestCityMarketID","Dest","DestCityName","DestState","DestStateFips","DestStateName","DestWac","CRSDepTime","DepTime","DepDelay","DepDelayMinutes","DepDel15","DepartureDelayGroups","DepTimeBlk","TaxiOut","WheelsOff","WheelsOn","TaxiIn","CRSArrTime","ArrTime","ArrDelay","ArrDelayMinutes","ArrDel15","ArrivalDelayGroups","ArrTimeBlk","Cancelled","CancellationCode","Diverted","CRSElapsedTime","ActualElapsedTime","AirTime","Flights","Distance","DistanceGroup","CarrierDelay","WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay","FirstDepTime","TotalAddGTime","LongestAddGTime","DivAirportLandings","DivReachedDest","DivActualElapsedTime","DivArrDelay","DivDistance","Div1Airport","Div1AirportID","Div1AirportSeqID","Div1WheelsOn","Div1TotalGTime","Div1LongestGTime","Div1WheelsOff","Div1TailNum","Div2Airport","Div2AirportID","Div2AirportSeqID","Div2WheelsOn","Div2TotalGTime","Div2LongestGTime","Div2WheelsOff","Div2TailNum","Div3Airport","Div3AirportID","Div3AirportSeqID","Div3WheelsOn","Div3TotalGTime","Div3LongestGTime","Div3WheelsOff","Div3TailNum","Div4Airport","Div4AirportID","Div4AirportSeqID","Div4WheelsOn","Div4TotalGTime","Div4LongestGTime","Div4WheelsOff","Div4TailNum","Div5Airport","Div5AirportID","Div5AirportSeqID","Div5WheelsOn","Div5TotalGTime","Div5LongestGTime","Div5WheelsOff","Div5TailNum",
2015,4,10,1,4,2015-10-01,"AA",19805,"AA","N797AA","1",12478,1247803,31703,"JFK","New York, NY","NY","36","New York",22,12892,1289203,32575,"LAX","Los Angeles, CA","CA","06","California",91,"0900","1001",61,61,1,4,"0900-0959",32,"1033","1257",4,"1210","1301",51,51,1,3,"1200-1259",0,"",0,370,360,324,1,2475,10,51,0,0,0,0,"0901",41,41,0,,,,,"",,,"",,,"","","",,,"",,,"","","",,,"",,,"","","",,,"",,,"","","",,,"",,,"","",
```

字段可真不少 109个字段


创建表
```
$ clickhouse-client --host=127.0.0.1

node2 :) CREATE TABLE `ontime` (`Year` UInt16,`Quarter` UInt8,`Month` UInt8,`DayofMonth` UInt8,`DayOfWeek` UInt8,`FlightDate` Date,`UniqueCarrier` FixedString(7),`AirlineID` Int32,`Carrier` FixedString(2),`TailNum` String,`FlightNum` String,`OriginAirportID` Int32,`OriginAirportSeqID` Int32,`OriginCityMarketID` Int32,`Origin` FixedString(5),`OriginCityName` String,`OriginState` FixedString(2),`OriginStateFips` String,`OriginStateName` String,`OriginWac` Int32,`DestAirportID` Int32,`DestAirportSeqID` Int32,`DestCityMarketID` Int32,`Dest` FixedString(5),`DestCityName` String,`DestState` FixedString(2),`DestStateFips` String,`DestStateName` String,`DestWac` Int32,`CRSDepTime` Int32,`DepTime` Int32,`DepDelay` Int32,`DepDelayMinutes` Int32,`DepDel15` Int32,`DepartureDelayGroups` String,`DepTimeBlk` String,`TaxiOut` Int32,`WheelsOff` Int32,`WheelsOn` Int32,`TaxiIn` Int32,`CRSArrTime` Int32,`ArrTime` Int32,`ArrDelay` Int32,`ArrDelayMinutes` Int32,`ArrDel15` Int32,`ArrivalDelayGroups` Int32,`ArrTimeBlk` String,`Cancelled` UInt8,`CancellationCode` FixedString(1),`Diverted` UInt8,`CRSElapsedTime` Int32,`ActualElapsedTime` Int32,`AirTime` Int32,`Flights` Int32,`Distance` Int32,`DistanceGroup` UInt8,`CarrierDelay` Int32,`WeatherDelay` Int32,`NASDelay` Int32,`SecurityDelay` Int32,`LateAircraftDelay` Int32,`FirstDepTime` String,`TotalAddGTime` String,`LongestAddGTime` String,`DivAirportLandings` String,`DivReachedDest` String,`DivActualElapsedTime` String,`DivArrDelay` String,`DivDistance` String,`Div1Airport` String,`Div1AirportID` Int32,`Div1AirportSeqID` Int32,`Div1WheelsOn` String,`Div1TotalGTime` String,`Div1LongestGTime` String,`Div1WheelsOff` String,`Div1TailNum` String,`Div2Airport` String,`Div2AirportID` Int32,`Div2AirportSeqID` Int32,`Div2WheelsOn` String,`Div2TotalGTime` String,`Div2LongestGTime` String,`Div2WheelsOff` String,`Div2TailNum` String,`Div3Airport` String,`Div3AirportID` Int32,`Div3AirportSeqID` Int32,`Div3WheelsOn` String,`Div3TotalGTime` String,`Div3LongestGTime` String,`Div3WheelsOff` String,`Div3TailNum` String,`Div4Airport` String,`Div4AirportID` Int32,`Div4AirportSeqID` Int32,`Div4WheelsOn` String,`Div4TotalGTime` String,`Div4LongestGTime` String,`Div4WheelsOff` String,`Div4TailNum` String,`Div5Airport` String,`Div5AirportID` Int32,`Div5AirportSeqID` Int32,`Div5WheelsOn` String,`Div5TotalGTime` String,`Div5LongestGTime` String,`Div5WheelsOff` String,`Div5TailNum` String) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192)

node2 :) show tables;

SHOW TABLES

┌─name───┐
│ ontime │
└────────┘
```

倒入数据报错
```
Code: 210. DB::NetException: Connection refused: (node2:9000, 10.0.12.8)
```

这个错误需要修改配置文件，让clickhouse绑定到ipv4, 配置文件`/etc/clickhouse-server/config.xml` 中查找 `listen_host`，改成ipv4再重启就好了


导入数据
```
time for i in *.zip; do echo $i; unzip -cq $i '*.csv' | sed 's/\.00//g' | clickhouse-client --host=127.0.0.1 --query="INSERT INTO ontime FORMAT CSVWithNames"; done

real	2m7.272s
user	3m5.545s
sys	0m18.028s
```

倒入时间，倒入后数据大小，查询速度，总记录大小

```
node2 :) SELECT table, formatReadableSize(sum(bytes)) as size,min(min_date) as min_date,max(max_date) as max_date FROM system.parts WHERE active GROUP BY table;


┌─table──┬─size─────┬───min_date─┬───max_date─┐
│ ontime │ 1.45 GiB │ 2015-01-01 │ 2017-09-30 │
└────────┴──────────┴────────────┴────────────┘

node2 :) select count(*) from ontime;
┌──count()─┐
│ 15713194 │
└──────────┘

1 rows in set. Elapsed: 0.018 sec. Processed 15.71 million rows, 15.71 MB (855.25 million rows/s., 855.25 MB/s.)
```

做了几个例子发现灰常的快啊。
