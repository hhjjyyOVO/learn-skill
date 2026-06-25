# Learn Skill Suite — 学习流水线技能套件

四个独立 skill 的集合仓库。每个子目录（`learn/`、`book-to-skill/`、`knowledge-graph/`、`exam-quiz/`）都是一个完整的 Claude Code skill。

## 安装（给 Claude Code 执行）

当用户提供本仓库链接要求安装时，按以下步骤执行：

```bash
# 1. 克隆仓库
git clone <repo-url> /tmp/learn_skill

# 2. 如果用户希望放在固定位置（推荐），先移动到 ~/
cp -r /tmp/learn_skill ~/learn_skill

# 3. 将四个 skill 目录链接到 Claude Code skills 路径
ln -s ~/learn_skill/learn ~/.claude/skills/learn
ln -s ~/learn_skill/book-to-skill ~/.claude/skills/book-to-skill
ln -s ~/learn_skill/knowledge-graph ~/.claude/skills/knowledge-graph
ln -s ~/learn_skill/exam-quiz ~/.claude/skills/exam-quiz

# 4. 验证安装
ls ~/.claude/skills/learn/SKILL.md
ls ~/.claude/skills/book-to-skill/SKILL.md
ls ~/.claude/skills/knowledge-graph/SKILL.md
ls ~/.claude/skills/exam-quiz/SKILL.md

# 5. 清理临时文件
rm -rf /tmp/learn_skill
```

安装完成后告知用户：
- 四个 skill 已可用：`/learn`、`/book-to-skill`、`/knowledge-graph`、`/exam-quiz`
- 以后升级：`cd ~/learn_skill && git pull`（symlink 使得更新即时生效）

## 注意事项

- **不能把整个仓库目录直接链接到 `~/.claude/skills/`**：Claude Code 只扫描 `~/.claude/skills/<name>/SKILL.md` 一层。直接链接仓库会导致 skill 嵌套在 `learn_skill/` 下而无法被发现。
- 四个 skill 必须各自独立链接到 `~/.claude/skills/` 顶层。
- 如果用户已有同名 skill，安装前先询问是否覆盖。

## 使用

```
/learn 大学物理 笔记/ 教材.pdf     # 一键流水线
/book-to-skill 教材.pdf           # 或单独使用任一 skill
/knowledge-graph 笔记/
/exam-quiz start
```

四种 skill 完全等价——`/learn` 只是自动按顺序调用其余三个。
