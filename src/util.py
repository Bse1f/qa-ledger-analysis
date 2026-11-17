import logging
import os
import re

import pandas as pd

log = logging.getLogger(__name__)


def parse_qty(text):
    """把 "3 件" / "4pcs" / " 2 " / "1,200" 变成整数；取不到就抛 ValueError。"""
    if text is None:
        raise ValueError("数量为空")
    s = str(text).replace(",", "").replace("，", "")
    m = re.search(r"\d+", s)
    if m is None:
        raise ValueError(f"取不到数字：{text!r}")
    return int(m.group())


def load(path):
    if not os.path.exists(path):
        raise SystemExit(f"找不到文件：{path}\n请确认路径，或把文件放到当前目录。")

    df = pd.read_csv(path, encoding="utf-8-sig")

    def to_int_or_na(value):
        try:
            return parse_qty(value)
        except ValueError:
            return pd.NA

    df["数量"] = df["数量"].map(to_int_or_na)      # 整列一次性转换，不写逐行循环

    bad = int(df["数量"].isna().sum())
    if bad:
        log.warning("跳过 %d 条无法解析的数量", bad)
        df = df.dropna(subset=["数量"])

    df["数量"] = df["数量"].astype(int)
    return df


def summarize(df, column, threshold=80):
    if column not in df.columns:
        raise ValueError(f"列名 {column} 不存在，实际有：{list(df.columns)}")
    g = df.groupby(column, as_index=False)["数量"].sum()
    if g["数量"].sum() == 0:
        raise ValueError("总数量为零，无法计算占比")
    g["占比"] = (g["数量"] / g["数量"].sum() * 100).round(1)

    for name, qty, rate in zip(g[column], g["数量"], g["占比"]):
        if rate > threshold:
            log.warning("%s 维度：「%s」占 %.1f%%（%d 件），某类不良高度集中",
                        column, name, rate, qty)

    return g


if __name__ == "__main__":
    print("执行通用函数")
