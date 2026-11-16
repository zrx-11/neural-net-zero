#!/usr/bin/env python3
"""从 manifest.json 生成人类可读的 quiz.md / flashcards.md / glossary.md，
保证与网页内嵌数据完全一致（单一数据源）。"""
import json

m = json.load(open("manifest.json", encoding="utf-8"))
chs = {c["id"]: c["title"] for c in m["chapters"]}
chs["__all__"] = "综合"

# ---------- quiz.md ----------
lines = ["# 测验", "", "题目与网页内测验一致，答案与解析在每题下方。", ""]
by_ch = {}
for q in m["quizzes"]:
    by_ch.setdefault(q["chapterId"], []).append(q)
for cid, qs in by_ch.items():
    lines.append(f"## {chs.get(cid, cid)}")
    lines.append("")
    for i, q in enumerate(qs, 1):
        typ = {"single": "单选", "multi": "多选", "blank": "填空"}.get(q["type"], q["type"])
        lines.append(f"### Q{i}.（{typ}）{q['question']}")
        if q.get("options"):
            letters = "ABCD"
            for j, o in enumerate(q["options"]):
                lines.append(f"- {letters[j]}. {o}")
        if q["type"] == "blank":
            ans = q["answer"]
        elif q["type"] == "multi":
            letters = "ABCD"
            ans = "".join(letters[i] for i in q["answer"])
        else:
            ans = "ABCD"[q["answer"]]
        lines.append("")
        lines.append(f"**答案**：{ans}")
        lines.append("")
        lines.append(f"**解析**：{q['explain']}")
        lines.append("")
open("quiz.md", "w", encoding="utf-8").write("\n".join(lines))

# ---------- flashcards.md ----------
lines = ["# 抽认卡", "", "正面只放问题，先自己答，再翻看背面。", ""]
cur = None
for f in m["flashcards"]:
    if f["chapterId"] != cur:
        cur = f["chapterId"]
        lines += [f"## {chs.get(cur, cur)}", ""]
    lines += [f"### 卡片：{f['front']}", f"- **背面**：{f['back']}", f"- **标签**：{', '.join(f.get('tags', []))}", f"- **章节**：{f['chapterId']}", ""]
open("flashcards.md", "w", encoding="utf-8").write("\n".join(lines))

# ---------- glossary.md ----------
lines = ["# 术语表", "", "| 术语 | 白话定义 | 章节 |", "|---|---|---|"]
for g in m["glossary"]:
    lines.append(f"| {g['term']} | {g['def']} | {g.get('chapterId', '')} |")
open("glossary.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

print("生成 quiz.md / flashcards.md / glossary.md")
print("测验", len(m["quizzes"]), "卡片", len(m["flashcards"]), "术语", len(m["glossary"]))
