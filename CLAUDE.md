# Learn Skill Suite — 学习流水线技能套件

> **主入口：`learn`** — 一键学习流水线编排器，调用其余三个 skill 完成从教材到测验的完整流程。

## 项目结构

```
learn_skill/
├── learn/              ← 🚀 主入口 skill（编排层）
├── book-to-skill/      ← 📖 教材提取 skill（原料层）
├── knowledge-graph/    ← 🗺️ 知识图谱构建 skill（加工层）
├── exam-quiz/          ← ✍️ 递进测验 skill（检验层）
├── CLAUDE.md           ← 项目说明
└── .gitignore
```

## 调用关系

```
用户输入 "帮我学XX"
       │
       ▼
   ┌──────────┐
   │  learn   │  编排层 — 解析意图、确认计划、按序调度
   └──┬───┬───┘
      │   │
      ▼   ▼
  ┌──────────────┐    ┌──────────────────┐
  │ book-to-skill │ ──→│ knowledge-graph   │
  │ PDF/文档→skill │    │ 笔记+skill→图谱    │
  └──────────────┘    └────────┬─────────┘
                               │
                      知识点索引 + 关系链
                               │
                               ▼
                      ┌──────────────────┐
                      │   exam-quiz       │
                      │   图谱→递进测验     │
                      └──────────────────┘
```

## 使用方式

```
/learn 学科名 笔记目录 [教材PDF路径]
```

### 三种运行模式

| 模式 | 命令 | 说明 |
|:---|:---|:---|
| 完整流水线 | `/learn 物理 笔记/ 教材.pdf` | book-to-skill → knowledge-graph → (可选 exam-quiz) |
| 只整理笔记 | `/learn 近代史 笔记/` | 仅 knowledge-graph |
| 只提取教材 | `/learn 刑法学 --extract 教材.pdf` | 仅 book-to-skill |

### 子 skill 也可独立使用

- `/book-to-skill 教材.pdf` — 单独提取教材
- `/knowledge-graph 笔记目录` — 单独构建图谱
- `/exam-quiz start` — 单独开始测验
