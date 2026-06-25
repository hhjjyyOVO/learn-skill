# Learn Skill Suite

> 一键学习流水线：从教材提取 → 知识图谱 → 递进测验，四个 Claude Code skill 覆盖完整学习闭环。

## 是什么

把"我要学这门课"变成一句话指令。四个 skill 各司其职，可以独立使用，也可以通过 `learn` 一键串联：

```
教材 PDF                         笔记文件夹
    │                                │
    ▼                                ▼
┌──────────────┐            ┌──────────────────┐
│ book-to-skill │ ──skill──→│  knowledge-graph  │
│ 提取教材框架   │            │ 构建知识图谱       │
└──────────────┘            └────────┬─────────┘
                                     │
                            知识点索引 + 关系链
                                     │
                                     ▼
                            ┌──────────────────┐
                            │    exam-quiz      │
                            │  递进自适应测验     │
                            └────────┬─────────┘
                                     │
                                     ▼
                               Obsidian 复习
```

## 快速开始

### 方式一：一键流水线

```bash
/learn 大学物理 d:\笔记\物理\ d:\教材\大学物理学.pdf
```

`learn` 自动完成：提取教材 → 构建图谱 → 询问是否测验。

### 方式二：按需单独使用

```bash
# 只想把教材转成 skill
/book-to-skill d:\教材\大学物理学.pdf

# 只想把笔记整理成知识图谱
/knowledge-graph d:\笔记\物理\

# 想用已有图谱直接开始刷题
/exam-quiz start
```

## 四个 Skill

### 🚀 learn — 编排层

学习流水线入口。解析用户意图，按正确顺序调度其余三个 skill。

| 模式 | 命令 | 流程 |
|:---|:---|:---|
| 完整流水线 | `/learn 学科 笔记/ 教材.pdf` | book-to-skill → knowledge-graph → exam-quiz |
| 只整理笔记 | `/learn 学科 笔记/` | knowledge-graph |
| 只提取教材 | `/learn 学科 --extract 教材.pdf` | book-to-skill |

### 📖 book-to-skill — 原料层

把教材/文档转换成结构化的 knowledge skill。支持 PDF、EPUB、DOCX、HTML、Markdown、TXT、RTF、MOBI 等格式。

```bash
/book-to-skill d:\教材\大学物理学.pdf
```

**输出**：`~/.claude/skills/<书名-slug>/` — 包含 SKILL.md、章节摘要、术语表、模式速查。

### 🗺️ knowledge-graph — 加工层

从笔记 + 教材 skill 构建三层知识网络：知识点索引 → 知识关系链 → 应用模式。自动识别学科类型（公式型/概念型/混合型/叙事型），适配输出格式。

```bash
/knowledge-graph d:\笔记\物理\                     # 纯笔记（无教材核对）
/knowledge-graph d:\笔记\物理\ 大学物理学.pdf        # 笔记 + PDF（自动调 book-to-skill）
/knowledge-graph d:\笔记\物理\ college-physics      # 笔记 + 已有 skill
```

**输出**：Obsidian 兼容的 `知识点索引.md` + `知识关系链.md`，可折叠 callout + 双向链接。

### ✍️ exam-quiz — 检验层

基于知识图谱自动生成递进式测验。逐题交互、错题追踪、薄弱点分析。轮次不限，自适应出题直到全部掌握。

```bash
/exam-quiz start                       # 自动扫描，开始测验
/exam-quiz start --scope "第1-5章"     # 限定范围
/exam-quiz start --target 95           # 目标正确率 95%
/exam-quiz continue                    # 继续上次
/exam-quiz review                      # 查看薄弱点
```

**特点**：即使没有知识图谱也能独立启动——系统会询问考试范围。

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
# Claude Code 全局 skills
git clone https://github.com/your-org/learn_skill.git ~/.claude/skills/learn_skill/

# 或者 Amp 全局 skills
git clone https://github.com/your-org/learn_skill.git ~/.config/agents/skills/learn_skill/
```

### 依赖

- **Claude Code** 或 **Amp**（支持 Skill 调用的 agent 环境）
- **Python 3.10+**（仅 `book-to-skill` 的文档提取脚本需要）
- Python 可选包：`pymupdf`（PDF）、`python-docx`（DOCX）、`ebooklib`（EPUB）、`beautifulsoup4`（HTML）——脚本会自动检测并提示安装

## 项目结构

```
learn_skill/
├── learn/                          # 编排层 skill
│   └── SKILL.md
├── book-to-skill/                  # 原料层 skill
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── extract.py              # 文档提取入口
│   │   └── extractor/              # 提取引擎
│   │       ├── config.py
│   │       ├── dependencies.py
│   │       ├── exceptions.py
│   │       ├── utils.py
│   │       └── parsers/            # 格式解析器
│   │           ├── pdf.py
│   │           ├── epub.py
│   │           ├── docx.py
│   │           ├── html.py
│   │           ├── text.py
│   │           ├── rtf.py
│   │           └── calibre.py
│   └── tools/
│       └── validate_skill.py
├── knowledge-graph/                # 加工层 skill
│   ├── SKILL.md
│   └── templates/
│       ├── 知识点索引.md
│       └── 知识关系链.md
├── exam-quiz/                      # 检验层 skill
│   └── SKILL.md
├── README.md
├── CLAUDE.md
└── .gitignore
```

## 适用场景

| 学科类型 | 示例 | 效果 |
|:---|:---|:---|
| 理工科 | 物理、化学、电路、热力学 | ⭐ 最佳 — 公式推导链天然适配 |
| 数学/经济 | 微积分、线代、信号处理 | ⭐ 很好 — 推导+分类混合 |
| 生医/法学 | 解剖学、药理学、民法 | ✅ 好 — 概念包含链+分析框架 |
| 文史哲 | 近代史、文学史、哲学 | ✅ 可用 — 因果链+论述框架 |
| 编程/CS | 数据结构、算法、系统设计 | ✅ 好 — 可视为混合型 |

## 设计原则

- **零依赖启动**：每个子 skill 都可以脱离 learn 独立调用
- **原材料不限**：PDF 教材、已有 skill、散装笔记——都可以作为输入
- **自适应格式**：自动识别学科类型，公式型输出符号表，概念型输出术语表
- **Obsidian 兼容**：知识图谱输出为 Obsidian 标准 Markdown，可折叠 callout + `[[双向链接]]`
- **递进式复习**：测验不只检测——它会记住你的薄弱点，下一轮集中攻击

## 许可

MIT
