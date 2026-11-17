import argparse
import logging
import os

import matplotlib.pyplot as plt

from util import load, summarize

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def parse_args():
    """输入: 命令行参数; 输出: input 路径、outdir 目录。"""
    parser = argparse.ArgumentParser(description="不良台账分析")
    parser.add_argument("--input", required=True,help="台账 CSV路径")
    parser.add_argument("--outdir",default="output", help="输出目录")
    return parser.parse_args()


def plot_bar(by_group, label_col, value_col, titel, outfile, xlabel="数量(件)"):
    """输入：分组统计表；输出：一张横向条形图存到 outfile。"""
    s = by_group.set_index(label_col)[value_col].sort_values()
    s.index.name = None
    plt.figure(figsize=(6,3.2))
    s.plot(kind = "barh")
    plt.title(titel)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(outfile,dpi=150, bbox_inches="tight")
    plt.close()

def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    ledger = load(args.input)
    logging.info("读到 %d 条记录",len(ledger))

    by_kind = summarize(ledger, "不良现象")
    print(by_kind.to_string(index=False))
    plot_bar(by_kind, "不良现象", "数量", "各不良现象数量合计",
             os.path.join(args.outdir, "图1-不良分布.png"))
    by_line = summarize(ledger, "产线")
    print(by_line.to_string(index=False))
    plot_bar(by_line, "产线", "数量", "各产线不良数量合计",
             os.path.join(args.outdir, "图2-产线分布.png"))

    cross = ledger.groupby(["产线", "不良现象"], as_index=False)["数量"].sum()
    cross = cross.sort_values("数量", ascending=False).head(5)
    labels = cross["产线"] + "-" + cross["不良现象"]

    plt.figure(figsize=(6, 3.2))
    plt.barh(labels, cross["数量"])
    plt.title("前 5 个「产线 × 不良」组合")
    plt.xlabel("数量（件）")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "图3-交叉前五.png"), dpi=150, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    main()