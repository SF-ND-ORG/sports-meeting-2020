# 体育节2020成绩查询系统后端文档

**表结构**
```sql
CREATE TABLE IF NOT EXISTS `sports`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `grades` VARCHAR(20),
   `class` VARCHAR(20),
   `name` VARCHAR(20),
   `sid` VARCHAR(20),
   `achievements` VARCHAR(100),
   `projects` VARCHAR(100),
   `rank` INT,
   `time` INT,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```sql
CREATE TABLE IF NOT EXISTS `students`(
   `sid` VARCHAR(10),
   `class` VARCHAR(20),
   `name` VARCHAR(20),
   PRIMARY KEY ( `sid` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```sql
CREATE TABLE IF NOT EXISTS `follow`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `sid` VARCHAR(10),
   `name` VARCHAR(20),
   `class` VARCHAR(20),
   `qq` VARCHAR(20),
   `time` INT,
   `status` INT,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

**班级**
* 地址：`/getgrades/byclass/`
* 参数：
```json
{
    "grades":"22",
    "class":"L9"
}
```
`http://114.55.93.225:5706/getgrades/byclass/?grades=22&class=L9`

**姓名**
* 地址：`/getgrades/byname/`
* 参数：
```json
{
    "grades":"22",
    "class":"L9",
    "name":"南鸣"
}
```
`http://114.55.93.225:5706/getgrades/byclass/?grades=22&class=L9&name=南鸣`

**项目**
* 地址：`/getgrades/bypro/`
* 参数：
```json
{
    "projects":"打篮球"
}
```
`http://114.55.93.225:5706/getgrades/bypro/?projects=打篮球`

**上传成绩**
* 地址：`/getgrades/byclass/`
* 参数：
```json
{
    "data":[
        {
            "grades":"22",
            "class":"L9",
            "name":"南鸣",
            "achievements":"233个",
            "projects":"打篮球",
            "rank":"2"
        },
        {
            "grades":"23",
            "class":"15",
            "name":"蔡徐坤",
            "achievements":"666个",
            "projects":"打篮球",
            "rank":"1"
        }
    ]
}
```
`http://114.55.93.225:5706/upgrades/?data=[{"grades":"22","class":"L9","name":"南鸣","achievements":"233个","projects":"打篮球","rank":"2"},{"grades":"23","class":"15","name":"蔡徐坤","achievements":"666个","projects":"打篮球","rank":"1"}]`

订阅
[订阅选手] 21L12 金坷垃
[取消订阅] 1
[订阅列表] 