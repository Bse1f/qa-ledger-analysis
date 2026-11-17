# 不良台账分析（qa-ledger-analysis）

把一份不良台账 CSV 读进来，按不良现象、产线、交叉三个维度出统计表和三张图。

## 这是做什么的

制造业现场的不良记录通常靠手工 Excel 台账维护。按现象统计一遍、再按产线统计一遍，一次要花小半天，换个人算出来的口径还不一定一样。

一条命令做完三件事：清洗数量列（`4件`、`1,200` 这类写法统一成整数）、按维度汇总并计算占比、输出三张横向条形图。统计口径固定写在代码里，同输入必得同输出。

## 怎么装

需要 Python 3.12。

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```


## 怎么跑

```bash
.\.venv\Scripts\python.exe src\analyze.py --input data\sample.csv --outdir output
```

`--input` 指定台账路径，`--outdir` 指定图片输出目录，目录不存在会自动创建。

## 跑完长什么样

```text
2026-11-17 11:08:48,702 INFO 读到 5 条记录
不良现象  数量   占比
外观划伤   5 41.7
尺寸超差   2 16.7
  虚焊   5 41.7
产线  数量   占比
 A   9 75.0
 B   1  8.3
 C   2 16.7
```

同时生成 `output/图1-不良分布.png`、`output/图2-产线分布.png`、`output/图3-交叉前五.png`。

## 数据从哪来

`data/sample.csv` 是五行样例，表头为 `日期,产线,不良现象,数量`。真实台账按同样表头替换即可，不用改代码。

样例里特意保留了 `4件` 这种带单位的脏数据，用来验证清洗逻辑确实在跑。

运行环境是 Windows + Python 3.12，中文图表依赖系统自带的微软雅黑字体。
