# Learn Skill Suite — 学习流水线技能套件

四个 skill 可以**独立使用**，也可以通过 `learn` 编排成完整流水线。两种方式完全等价——`learn` 只是省掉了手动衔接的步骤。

## 项目结构

```
learn_skill/
├── learn/              ← 🚀 编排层（可选）— 一键串联全流程
├── book-to-skill/      ← 📖 原料层 — PDF/文档 → knowledge skill
├── knowledge-graph/    ← 🗺️ 加工层 — 笔记+skill → 知识图谱
├── exam-quiz/          ← ✍️ 检验层 — 图谱 → 递进测验
├── CLAUDE.md
└── .gitignore
```

## 方式一：独立使用（每个 skill 零依赖）

```
/book-to-skill 教材.pdf                         # 把教材转成 skill
/knowledge-graph 笔记目录                         # 把笔记整理成知识图谱
/knowledge-graph 笔记目录 教材.pdf                 # 笔记+PDF，自动调 book-to-skill
/exam-quiz start                                # 从图谱出题自测
```

适合：只需要其中某个环节、手上已有中间产物、想精细控制每一步。

## 方式二：learn 编排（一键流水线）

```
/learn 大学物理 笔记目录 教材.pdf                   # 完整流水线：提取→图谱→(可选)测验
/learn 近代史 笔记目录                             # 只整理笔记
/learn 刑法学 --extract 教材.pdf                   # 只提取教材
```

适合：从零开始学一门课、想一句话触发全流程。

## 调用关系

```
方式二（编排）:                     方式一（独立）:
                                   
/learn 学科 笔记 教材                /book-to-skill 教材.pdf
  │                                /knowledge-graph 笔记/
  ├── Skill("book-to-skill")       /exam-quiz start
  ├── Skill("knowledge-graph")     
  └── Skill("exam-quiz")           每个都可以单独调用
```

`learn` 本身不处理文档也不构建图谱——它只做两件事：解析用户意图 + 按正确顺序调用子 skill。
