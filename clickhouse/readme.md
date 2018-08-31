CH
===

分析型数据库

* docker https://hub.docker.com/r/yandex/clickhouse-server/
* docs https://clickhouse.yandex/docs/en/

环境
* Centos7
* clickhouse 18.10.3

[单机版, 安装参考](https://github.com/Altinity/clickhouse-rpm-install)

```
$ curl -s https://packagecloud.io/install/repositories/altinity/clickhouse/script.rpm.sh | sudo bash
$ sudo yum list 'clickhouse*'
$ sudo yum install -y clickhouse-server clickhouse-client
$ sudo /etc/init.d/clickhouse-server restart
```

主要有两个命令

* clickhouse-server
* clickhouse-client


配置文件有2个

```
/etc/clickhouse-server/config.xml
/etc/clickhouse-server/users.xml
```

默认只能本地访问，可以在 `config.xml` 中配置监听的端口.




### 简单集群安装

如果需要复制还需要安装 zookeeper，这里就是3个节点，所以没有配置zk

* [doc](https://clickhouse.yandex/docs/en/operations/table_engines/distributed/)
* [ClickHouse之集群搭建以及数据复制](http://www.cnblogs.com/gomysql/p/6708650.html)
* [配置文件也可以直接写到主配置中](https://stackoverflow.com/questions/39095443/where-should-the-remote-server-element-located-when-configurating-clickhouse-clu)
* [配置文件位置自定义](https://github.com/yandex/ClickHouse/issues/666)

#### 安装配置

首先每个集群安装好单机版本的clickhouse，然后就是配置文件修改了，加入3个节点叫做 A,B,C

* A : 10.0.12.13
* B : 10.0.12.10
* C : 10.0.12.8

集群方式使用 Distributed 这个引擎，需要在配置文件中配置表名等信息

这里为了方面把 `config.xml` 中的 listen_host 改成 `0.0.0.0`了，节点之间还是要保证互通的。

创建配置 `sudo vim /etc/metrika.xml`, 写入配置（这个配置的请看 `config.xml`中的 `remote_servers` 下的说明)

```xml
<yandex>
<clickhouse_remote_servers>
    <logs>
        <shard>
             <internal_replication>true</internal_replication>
            <replica>
                <host>10.0.12.13</host>
                <port>9000</port>
            </replica>
        </shard>
        <shard>
            <replica>
                <internal_replication>true</internal_replication>
                <host>10.0.12.10</host>
                <port>9000</port>
            </replica>
        </shard>
        <shard>
            <internal_replication>true</internal_replication>
            <replica>
                <host>10.0.12.8</host>
                <port>9000</port>
            </replica>
        </shard>
    </logs>
</clickhouse_remote_servers>

<networks>
   <ip>::/0</ip>
</networks>

<clickhouse_compression>
<case>
  <min_part_size>10000000000</min_part_size>             
  <min_part_size_ratio>0.01</min_part_size_ratio>
  <method>lz4</method>
</case>
</clickhouse_compression>

</yandex>
```

配置好了依次启动这三个节点
```
sudo /etc/init.d/clickhouse-server start 
```

发现 `/etc/clickhouse-server/` 多了一个 `config-preprocessed.xml` 文件，这个是自动生成的文件，查看下就会发现，clickhouse启动的之后把配置合并了


#### 建表

创建表需要建立本地表，还有分布式表两种表,

```bash
$ clickhouse-client --host=127.0.0.1
```

本地表，所有节点统一建立
```sql
CREATE TABLE ontime_local (FlightDate Date,Year UInt16) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192);
```


分布式表, 写入数据用这个表，所以要在写入数据的节点建表，如果所有节点都可写，那么所有节点都建表
```sql
CREATE TABLE ontime_all AS ontime_local ENGINE = Distributed(logs, default, ontime_local, rand())
```

注意下 `Distributed()`的几个参数 ， `logs`是集群名称，和配置中对应的，`ontime_local` 是本地表名，`default` 是库名，`rand()` 是key的分布方式


#### 测试

在其中一台server写入数据
```sql
node1 :) insert into ontime_all (FlightDate,Year)values('2001-10-12',2001);

INSERT INTO ontime_all (FlightDate, Year) VALUES

Ok.

1 rows in set. Elapsed: 0.005 sec.
```

另外一台查询
```
node1 :) select * from  ontime_all;

SELECT *
FROM ontime_all

┌─FlightDate─┬─Year─┐
│ 2002-10-12 │ 2002 │
└────────────┴──────┘
┌─FlightDate─┬─Year─┐
│ 2001-10-12 │ 2001 │
└────────────┴──────┘
```

交叉测试没问题


