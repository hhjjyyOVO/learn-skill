# Learn Skill Suite — 学习流水线技能套件

仓库根目录的四个文件夹即四个独立 skill——clone 后 symlink 到 `~/.claude/skills/` 即可使用。

## 目录即 skill

```
learn_skill/
├── learn/SKILL.md              ← 🚀 编排层 — 一键串联全流程
├── book-to-skill/SKILL.md      ← 📖 原料层 — PDF/文档 → knowledge skill
├── knowledge-graph/SKILL.md    ← 🗺️ 加工层 — 笔记+skill → 知识图谱
├── exam-quiz/SKILL.md          ← ✍️ 检验层 — 图谱 → 递进测验
├── README.md
├── CLAUDE.md
└── .gitignore
```

每个目录就是 Claude Code 的一个 skill（包含 `SKILL.md` + 辅助文件），可以被 Claude Code 直接加载。

## 安装

```bash
git clone <url> ~/learn_skill
ln -s ~/learn_skill/{learn,book-to-skill,knowledge-graph,exam-quiz} ~/.claude/skills/
```

## 使用

```
/learn 大学物理 笔记/ 教材.pdf     # 一键流水线
/book-to-skill 教材.pdf           # 或单独使用任一 skill
/knowledge-graph 笔记/
/exam-quiz start
```

四种 skill 完全等价——`/learn` 只是自动按顺序调用其余三个。
