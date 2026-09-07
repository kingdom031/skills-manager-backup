---
name: dark-geek-infographic
description: 暗黑极客科技风信息长图与卡片排版技能。用于将技术调研、单品深度拆解、性能基准评测、开源/AI 项目榜单横评等内容，自动生成适合手机竖屏阅读和高清截图分享的单文件 HTML + Tailwind CSS 代码。
---

# 暗黑极客科技风信息长图排版规范 (Dark Geek Tech Infographic)

本技能用于将技术评测、产品拆解、开源/AI 榜单、性能对比等内容，转化为极致视觉美感的**“暗黑极客科技风”**单文件 HTML 信息长图代码。生成的页面专为手机竖屏阅读优化，并具有直接截图生成社交媒体科技长图的工业级质感。

---

## 1. 核心视觉规范 (Design Tokens)

### 1.1 画布尺寸与背景 (Canvas & Background)
- **容器尺寸**：移动端竖屏固定宽度（推荐 `w-[480px]` 至 `w-[520px]`，默认 `w-[500px]` 居中排版），高度根据内容自适应（`min-h-screen`）。
- **页面背景**：深邃夜空黑到近黑纵向渐变：
  ```html
  bg-gradient-to-b from-[#0b0c16] via-[#090b14] to-[#04060b]
  ```
- **内边距与溢出**：容器自带 `p-6` 内边距，且设置 `overflow-hidden`。
- **顶部极客环境光 (Top Glow Effect)**：在容器顶部增加轻微径向光晕：
  ```css
  .glow-top {
    background: radial-gradient(120% 60% at 50% 0%, rgba(56,189,248,0.18), rgba(168,85,247,0.10) 40%, transparent 70%);
  }
  ```

### 1.2 毛玻璃卡片与发光边框 (Glassmorphic Glow Cards)
- **卡片底色**：半透明深蓝/深灰背景：
  - 外层主卡片：`bg-[#131728]/70` 或 `bg-[#151a30]/80`，带 `backdrop-blur-md`
  - 嵌套深色内衬小区块：`bg-[#0e1222]`
- **圆角规范**：外层卡片统一采用 `rounded-2xl`，内嵌子模块采用 `rounded-xl` 或 `rounded-lg`。
- **发光边框与外发光阴影 (Glow Border & Shadow)**：
  - 默认微光边框：`border border-indigo-500/30`
  - 暖金黄高亮：`border border-yellow-500/40 shadow-[0_0_22px_-6px_rgba(250,204,21,0.35)]`
  - 玫粉色高亮：`border border-pink-500/40 shadow-[0_0_22px_-6px_rgba(244,63,94,0.35)]`
  - 天青蓝高亮：`border border-sky-500/40 shadow-[0_0_22px_-6px_rgba(56,189,248,0.35)]`
  - 电光紫高亮：`border border-purple-500/40 shadow-[0_0_22px_-6px_rgba(168,85,247,0.35)]`
  - 荧光绿高亮：`border border-emerald-500/40 shadow-[0_0_22px_-6px_rgba(52,211,153,0.35)]`

### 1.3 色彩与微光点缀 (Accent Colors)
| 颜色角色 | 色值 / Tailwind 类 | 适用场景 |
| :--- | :--- | :--- |
| **天青蓝 (Sky/Cyan)** | `#38bdf8` / `text-sky-400` / `text-cyan-400` | 核心技术关键词、首位强调、科技感分类 Badge |
| **电光紫 (Purple/Indigo)** | `#a855f7` / `text-purple-400` / `text-indigo-300` | 架构名词、类别胶囊、辅助强调 |
| **荧光绿 (Emerald/Green)** | `#34d399` / `text-emerald-400` / `text-green-400` | 优势项 (Pros)、已通过基准、性能提升指标 |
| **暖金黄 (Yellow/Amber)** | `#facc15` / `text-yellow-400` | TOP 1 榜首、核心综合高分、Star 星标 |
| **玫粉色 (Pink/Rose)** | `#f43f5e` / `text-pink-400` | 重点突破项、劣势/局限 (Cons)、预警标识 |

### 1.4 文本层级与排版安全 (Typography & Anti-Wrap)
- **一级大标题**：`text-white font-bold`（主标题 `text-[26px]` 至 `text-[28px]`，`leading-tight`）。
- **二级标题/卡片主标题**：`text-white font-bold text-base`。
- **正文及特性描述**：浅灰蓝 `text-slate-300`（`text-xs` 或 `text-sm`，重点词使用 `<span class="text-white font-semibold">`）。
- **辅助技术参数/底座信息**：弱化灰 `text-slate-500`（`text-[11px]` 或 `text-[10px]`）。
- **防换行溢出**：
  ```css
  .no-break { word-break: keep-all; overflow-wrap: anywhere; }
  ```
  在胶囊 Badge、评分、标签等关键单行文本上必须加上 `no-break` / `truncate`，确保文字不挤压、不换行破坏整体版式。
- **发光数字 (Score Ring)**：
  ```css
  .score-ring { text-shadow: 0 0 18px currentColor; }
  ```

### 1.5 极简图标规范 (Native Unicode / Emoji)
- 严禁引入庞大的外部图标字体或 SVG 库，保持单文件纯粹性。
- 纯天然使用原生 Unicode 符号与科技感 Emoji：
  - ★ (Star / 标星)
  - ⑂ (Fork / 分支)
  - ⚡ / 🚀 (架构性能 / 核心能力)
  - 💎 / 🛠️ (特性与机制)
  - ✅ / ✔ (官方优势 Pros)
  - ⚠️ / ✖ (官方局限 Cons)
  - 💡 (选型建议 / 核心观点)
  - 🏷️ / 📌 (标签与元信息)

---

## 2. 核心版式体系 (Layout Systems)

根据输入内容的类型与诉求，严格选择以下两套版式之一构建：

### 【版式 A：单品深度拆解卡片 (Deep-Dive Spec Sheet)】
适用于：单一技术方案、具体开源项目/工具、架构升级、新版模型的全方位深度剖析。

```
┌────────────────────────────────────────────────────────┐
│  [ Header ]                                            │
│  [胶囊定位 Badge] (如 "最佳综合推荐 / 适合可视化学习")  │
│  h1 标题：项目名称 + 核心定位短语                      │
│  副标题：版本发布时间 / 研发团队 / 评测环境            │
├────────────────────────────────────────────────────────┤
│  [ 模块一：核心技术架构 / 实测基准数据 ]               │
│  🏷️ 标题 (如 ⚡ 官方核心技术架构)                       │
│  • 2~3 条要点列表，关键名词加粗并高亮为白色            │
│  底部底座/语言元信息 (text-[11px] text-slate-500)      │
├────────────────────────────────────────────────────────┤
│  [ 模块二：特性与机制 / 输出能力 ]                     │
│  💎 标题 (如 🛠️ 核心机制与工作流)                      │
│  嵌套深色内衬卡片 (bg-[#0e1222] p-3 rounded-xl)        │
│  带有 01 / 02 / 03 编号加粗项与关键解析                │
├────────────────────────────────────────────────────────┤
│  [ 模块三：优劣对比 (Pros & Cons) ]                    │
│  双列并排 Grid (grid grid-cols-2 gap-3)                │
│  ┌───────────────────────┐  ┌───────────────────────┐  │
│  │ ✅ 核心优势 (绿色系)  │  │ ⚠️ 局限/需注意(粉色系)│  │
│  │ • 优势要点 1          │  │ • 局限要点 1          │  │
│  │ • 优势要点 2          │  │ • 局限要点 2          │  │
│  └───────────────────────┘  └───────────────────────┘  │
├────────────────────────────────────────────────────────┤
│  [ Footer 底部 ]                                       │
│  单行居中小字号弱化摘要定位语或适用场景结论            │
└────────────────────────────────────────────────────────┘
```

---

### 【版式 B：榜单/多项目横评流 (Rank / Comparison List)】
适用于：多款工具横评、技术生态排行榜、主流框架选型对比。

```
┌────────────────────────────────────────────────────────┐
│  [ Header ]                                            │
│  [分类 Badge 1]                   [分类 Badge 2]       │
│  h1 标题：年份 + 领域名称 + 横评榜 (高亮彩色重点字)    │
│  副标题：评测周期 · 实测方式 · 口碑加权说明            │
├────────────────────────────────────────────────────────┤
│  [ 横评卡片流 (Cards Stream) ]                         │
│                                                        │
│  ┌─── #1 (暖金黄边框发光) ──────────────────────────┐  │
│  │ [#1] 项目名称 (h2)             │ [ 9.6 ] 综合评分│  │
│  │ 公司/作者 · 定位类型           │ ★ 45.2k  Star   │  │
│  │ 亮点：加粗核心词 · 关键特性    │ ⑂ 3.1k   Fork   │  │
│  │ 底座：LLM底座 · 场景：适用领域 │                 │  │
│  └─── (左右 2 栏布局) ────────────┴─────────────────┘  │
│                                                        │
│  ┌─── #2 (玫粉色边框发光) ──────────────────────────┐  │
│  │ [#2] 项目名称 (h2)             │ [ 9.3 ] 综合评分│  │
│  │ ...                            │ ...             │  │
│  └────────────────────────────────┴─────────────────┘  │
│                                                        │
│  ┌─── #3 (天青蓝边框发光) ──────────────────────────┐  │
│  │ [#3] 项目名称 (h2)             │ [ 9.0 ] 综合评分│  │
│  │ ...                            │ ...             │  │
│  └────────────────────────────────┴─────────────────┘  │
│  (颜色按 黄、粉、蓝、紫 依次交替发光)                  │
├────────────────────────────────────────────────────────┤
│  [ Footer 底部 ]                                       │
│  💡 选型建议：一句话速查选型指引                       │
│  数据来源与估算说明 · 截图生成时间戳                   │
└────────────────────────────────────────────────────────┘
```

---

## 3. 完整代码生成模板

### 3.1 页面基础骨架
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title><!-- 页面标题 --></title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  html, body { margin: 0; padding: 0; background: #04060b; }
  body::-webkit-scrollbar { width: 0; height: 0; }
  .no-break { word-break: keep-all; overflow-wrap: anywhere; }
  .glow-top {
    background: radial-gradient(120% 60% at 50% 0%, rgba(56,189,248,0.18), rgba(168,85,247,0.10) 40%, transparent 70%);
  }
  .score-ring {
    text-shadow: 0 0 18px currentColor;
  }
</style>
</head>
<body class="flex justify-center">
  <main class="relative w-[500px] min-h-screen bg-gradient-to-b from-[#0b0c16] via-[#090b14] to-[#04060b] p-6 overflow-hidden">
    <div class="glow-top absolute inset-x-0 top-0 h-64 pointer-events-none"></div>

    <div class="relative z-10">
      <!-- 头部 Header -->
      <!-- 核心卡片列表 / 拆解模块 -->
      <!-- 底部 Footer -->
    </div>
  </main>
</body>
</html>
```

---

## 4. 规范与自检清单 (Pre-flight Checklist)

在输出 HTML 代码前，务必执行以下自检：
1. **单文件无外挂**：必须引入 Tailwind CDN，不依赖外部 CSS 文件或外部 icon font。
2. **移动端适配**：固定容器宽度为 `500px`（或 480px~520px），并在 `body` 采用 `flex justify-center` 居中。
3. **文字截断与防破行**：所有关键标题、Badge、数值处配置 `no-break`，防止截图时产生难看的换行与错位。
4. **层级对比**：白色高亮主文、浅灰蓝描述、弱化灰底座元数据，必须保持清晰明暗梯度。
5. **发光与质感**：背景暗黑渐变、卡片毛玻璃 `backdrop-blur-md`、发光阴影 `shadow-[0_0_22px_-6px_...]` 完整配齐。

---

## 5. 参考示例 (Examples)

- 版式 B 横评榜示例：查看 `examples/code-agent-review.html`
- 版式 A 单品深度拆解示例：查看 `examples/spec-sheet-deep-dive.html`
