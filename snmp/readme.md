

### 流量带宽统计

获取信息汇总
```
$ snmpwalk -v 2c -c xxxxx 10.0.20.14 IF-MIB::ifTable
```

区分出网卡，然后获取网卡的信息
```
$ snmpwalk -v 2c -c xxxxx 10.0.20.14 IF-MIB::ifDescr
IF-MIB::ifDescr.1 = STRING: lo
IF-MIB::ifDescr.2 = STRING: eth0

$ snmpwalk -v 2c -c xxxxx 10.0.20.14 IF-MIB::ifInOctets.2
IF-MIB::ifInOctets.2 = Counter32: 3777493685

$ snmpwalk -v 2c -c xxxxx 10.0.20.14 IF-MIB::ifOutOctets.2
IF-MIB::ifOutOctets.2 = Counter32: 2551297306
```


