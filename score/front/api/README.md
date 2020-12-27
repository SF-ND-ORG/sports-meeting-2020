# 接口文档

API端口开在5705上，实现成绩获取以及查询功能

## getgrades

获取成绩。

### 请求格式

| 项目 | 属性 | 备注 |
|  ----  | ----  | ---- |
| 请求方法 | GET ||
| 请求URL | `/getgrades/[methodname]` |methodname为查询方式，下有说明|

### methodname

有三种，分别为byclass，byname和bypro，分别表示按班级，按名字和按项目三种查询方式。

### 请求参数

参数只有一个，为查询的参数
对于byclass，参数为请求的班级，格式如下

```text
年级+文/理+班级
```

年级的格式为21，22或23，表示高一高二和高三

01代表文，02代表理，特别的，高一均为00。

班级有两位。

## 返回格式

返回格式为一段json，包含查询结果。

```json
{
    {
        "id":"<id>",
        "class":"<class>",
        "grade":"<grade>",
        "project":"<project>",
        "rank":"<rank>",
    }
    {
        "id":"<id>",
        "class":"<class>",
        "grade":"<grade>",
        "project":"<project>",
        "rank":"<rank>",
    }
    ......
}
```
