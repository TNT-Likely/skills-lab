---
name: portal-dashboard
description: Use when building a local docs/scripts portal dashboard in this style.
---

# Portal Dashboard（Clash 面板风文档优先门户）

一套「暖灰底 + 近白卡片 + iOS 蓝 + 大圆角胶囊 + tabular 数字」的文档优先门户视觉系统。适合本地知识库门户、文档/脚本面板、开发者首页——**以文档浏览为主体、仪表盘数字为点缀**的单页门户。取样自一张 Clash 代理面板截图，采样记录见 [references/measurements.md](references/measurements.md)；自包含起步模板见 [assets/starter.html](assets/starter.html)（零依赖、file:// 直开）。

## 版式系统

自上而下的单列流，**无侧栏**。页面容器 `max-width:1440px; margin:0 auto; padding:40px 44px 84px`（≤900px 收紧为 `24px 18px 60px`）。

```
┌ header：logo+标题 ············· 搜索胶囊 ········ [自动|☀|☾] 分段开关 ┐
├ hero 行（2fr 1fr 1fr，≤900px 两列、≤680px 单列）                      ┤
│   hero-mini：运行中 pill + 32px 大数字 + meta ····· blob 装饰+⟳刷新    │
│   metric：知识库（29px 数字 + spark 面积图）· 工具与脚本（同款）        │
├ services：服务胶囊条（7px 绿点 · 名称 :端口，在线=浅绿底）             ┤
├ toolbar：分类 chips ─────── ⭐收藏 · 🗑垃圾箱 · 只看当前 ○ 开关       ┤
├ area「总览」 ● 标题 · N 篇 ···················· 区域索引 →            ┤
│   doc-grid：repeat(auto-fill,minmax(330px,1fr))                      │
├ area「开发与联调」● ···（每个区域一段，顺序由数据侧约定）              ┤
├ 工具与脚本 ● ····· 全部工具 →  （永远放最后，margin-top:54px）         ┤
│   tool-grid：repeat(auto-fill,minmax(290px,1fr))                     │
├ footer：门户信息 · 同步时间 · 文件数                                  ┤
├ toast：底部居中胶囊（z-index 200）                                    ┤
└ 弹窗层：overlay（模糊遮罩 z-300）+ modal（560px 卡片 z-301）          ┘
```

1. **header**：左品牌（42px 蓝底圆角 logo + 标题 28px/700 + 副标 12.5px dim）；右搜索胶囊 + 右上角三态模式**分段开关**（不再是大按钮）；搜索用 `margin-left:auto` 顶到右边。
2. **hero 行**：`grid-template-columns:2fr 1fr 1fr; gap:18px`，替代旧版 5 格统计行。左侧 `hero-mini`（大卡）：状态 pill + 32px 大数字（带 13px 单位）+ meta 行（服务在线/已同步）+ 右侧 blob 有机形装饰 + 46px 蓝色圆形 ⟳ 刷新按钮；右侧两张 `metric` 卡：12px 标签 + 29px 大数字 + 底部 62px 蓝色 spark 面积图（inline SVG）。≤900px 两列（hero-mini 跨两列），≤680px 单列、blob 缩小。
3. **服务胶囊条**：`display:flex; gap:10px; flex-wrap:wrap`，左起「服务」标签 11.5px dim，每服务一颗胶囊（状态圆点 + 名称 + `:端口`）。
4. **工具栏**：左分类 chips，右「⭐ 收藏」「🗑 垃圾箱」两个 viewbtn + 「只看当前」开关（`margin-left:auto`）。
5. **区域分组**（文档主体，可多个）：区域头 = 10px 彩色圆点（3px 圆角）+ 标题 20px/700 + 篇数 11.5px dim + 右侧「区域索引 →」蓝链；区域头下方 1px `--line` 分隔线。区域圆点按区域分配固定色相，参考实现示例：总览 `#8a8a8e`、开发 `#ff9f0a`、车辆通信 `#34c759`、后端 `#0091ff`、运营 `#8b7ce8`、制造 `#ff6b5a`、飞书 `#00b8d9`。
6. **工具与脚本**：永远放最后，区域头同款但圆点用 `--blue`；网格 `minmax(290px,1fr)`。
7. **页脚**：`border-top:1px solid var(--line)`，11.5px dim，`margin-top:64px`，左信息 + 右占位。
8. **弹窗层**：overlay 全屏模糊遮罩 + 560px 居中卡片弹窗（收藏夹/垃圾箱/确认删除共用）。
9. **toast**：固定底部居中胶囊，浮于所有内容之上。

重点：**文档区域是页面主体，工具区永远殿后**；hero 行是仪表盘点缀。

## 设计令牌

light（`:root`，同时 `color-scheme:light`）：

```css
--bg:#f9f7fa; --card:#ffffff; --line:#e4e1e6; --soft:#f2f0f3;
--ink:#1d1d1f; --dim:#8a8a8e; --blue:#0091ff; --blue-soft:#e7f1ff;
--green:#34c759; --green-soft:#a1f7a1; --amber:#ff9f0a; --red:#ff3b30;
--shadow:0 1px 3px rgba(20,20,30,.05);
```

dark（`html[data-theme="dark"]`，同时 `color-scheme:dark`）：

```css
--bg:#0e0f12; --card:#1a1b20; --line:#2c2e35; --soft:#22242a;
--ink:#f2f2f7; --dim:#8e8e93; --blue:#0a84ff; --blue-soft:#10233c;
--green:#30d158; --green-soft:#1f4d2a; --amber:#ff9f0a; --red:#ff453a;
--shadow:0 1px 3px rgba(0,0,0,.35);
```

> 注：本套为 v2 现值。首版令牌（更贴原始采样）为 `--bg:#f2f0f3 --card:#fcf9fa --line:#e8e6e8 --shadow:0 1px 2px rgba(20,20,30,.035)`（dark `--card:#17181c --line:#2a2c31 --shadow:…rgba(0,0,0,.3)`），演进记录见 measurements.md。如追求最贴参考图可回退首版。

圆角：卡片 18–22px（doc/tool 卡 18px、hero/metric 卡 22px）、胶囊 999px、小元素 13–14px（logo 13px、`--r:20px --r-sm:14px` 供外部使用）。

字体栈：

- 正文/标题：`-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC",system-ui,sans-serif`
- 等宽（命令、文件类型、端口、路径）：`ui-monospace,SFMono-Regular,Menlo,Consolas,monospace`

## 主题系统

三态 auto / light / dark。CSS 骨架（dark 令牌块需在 `html[data-theme="dark"]` 与媒体查询中各写一遍）：

```css
:root { color-scheme:light; /* light tokens */ }
html[data-theme="dark"] { color-scheme:dark; /* dark tokens */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { color-scheme:dark; /* dark tokens */ }
}
```

JS 要点（完整实现见 starter.html）：

```js
function getMode() { try { return localStorage.getItem("hub-theme-mode") || "auto"; } catch (e) { return "auto"; } }
function setMode(m) {
  if (m === "auto") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.dataset.theme = m; // "light" | "dark"
  // 高亮分段开关中对应按钮（.on = 蓝底白字）
  try { localStorage.setItem("hub-theme-mode", m); } catch (e) {}
}
```

规则：

- localStorage 键名固定 `hub-theme-mode`；读写都要 try/catch（file:// 或隐私模式会抛异常）。
- **auto 时不写 data-theme 属性**（交给媒体查询）；显式 light/dark 时写 `data-theme`。
- 页面加载时立即 `setMode(getMode())` 恢复上次选择，避免闪错主题。
- 控件是三段分段开关（每段 32×32、胶囊容器 `padding:3px; gap:2px`、`role="group"` + aria-label），选中段蓝底白字 + `0 2px 8px rgba(0,145,255,.28)` 浮影；图标用 inline SVG（半圆=自动、太阳=浅色、月亮=深色），不用 emoji。

## 组件规格

- **hero-mini 大卡**：`border-radius:22px; padding:15px 22px; min-height:148px; box-shadow:0 2px 10px rgba(20,20,30,.06)`（dark `.35`）。内容三行：`pill.green`「运行中」（底 `#dcfce7`/字 `#166534`/1px 边 `#86efac`/点 `#16a34a`；dark `#14351f`/`#4ade80`/`#1f6b3a`）→ `hero-num` 32px/700/`-1.2px` tabular + 13px dim 单位 → `hero-meta` 11.5px dim（`<b>` 12.5px/600 ink）。
- **blob 装饰 + 刷新钮**：右 42% 区域一张纯 CSS 有机形（220×150 径向渐变 `#f4f9ff→#e4efff→#d8e9ff`、有机 border-radius、`::before` 副形；dark 深蓝渐变 `#16304f→#0d1c30`）；中心 46px 蓝底白字圆形 ⟳（`0 10px 24px rgba(0,145,255,.32)` 浮影），点击 360° 旋转 420ms + toast。≤680px 缩为 140×120 / 38px 按钮。
- **metric 卡 + spark**：`border-radius:22px; padding:14px 18px; min-height:148px`，同 hero 浮影。顶行 12px dim 标签（右侧计数）；29px/700/`-1.2px` 大数字 + 13px 单位；底部贴边 62px 高 spark 面积图——inline SVG：蓝色渐变填充（`#0091ff` 透明度 .18–.2 → 0）+ 1.6px 描边折线，`preserveAspectRatio="none"` 拉伸适配。
- **service pill**：`border-radius:999px; padding:4px 11px; font-size:11.5px; background:var(--card); border:0; box-shadow:var(--shadow)`。7px 圆形状态点：**在线绿点亮（`--green`）**，离线灰（light `#c9c7cc` / dark `#4a4d55`）；在线时文字转 `--ink` 且**底色转浅绿** `#f2fbf5`（dark `#12251a`）。hover 浮影加深 `0 3px 10px rgba(20,20,30,.12)`。
- **chip**：`border:0; border-radius:999px; padding:5px 14px; font-size:12.5px; background:var(--card); box-shadow:var(--shadow); color:var(--dim)`。**选中 = 蓝底白字**：`background:var(--blue); color:#fff; font-weight:600; box-shadow:0 3px 10px rgba(0,145,255,.24)`。计数 `<span class="n">` 10.5px、`opacity:.7`。
- **viewbtn（收藏/垃圾箱）**：与 chip 同规格（无边框胶囊 + `--shadow`），常显计数，点击打开对应弹窗。
- **switch**：40×24、`border-radius:999px`、无边框；关 = `#d8d5da`（dark `#3a3d44`），**开 = `--blue`**。白色圆钮 18px，`top:3px; left:3px`，开启 `translateX(16px)`，`transition:.15s`。旁标签 12px dim，整行可点。
- **doc card**：整卡 `<a>`，`min-height:150px; padding:18px 20px; border-radius:18px; background:var(--card); border:0; box-shadow:var(--shadow)`；hover `translateY(-2px)` + 浮影 `0 8px 22px rgba(20,20,30,.08)`。结构：顶行状态 badge + 右对齐等宽类型（MD/HTML/README，9.5px dim）；**标题 15px/600**（`line-height:1.4; padding-right:64px`，给悬浮按钮让位）；描述 12px dim **两行截断**（`-webkit-line-clamp:2`）；底部 foot `space-between` 10.5px dim：**更新日期** + 「更新」。状态 badge 色：当前 = 底 `#e7f9ec`/字 `#1a8f3a`（dark `#123522`/`--green`）；候选 = 底 `#fff4e0`/字 `#b26a00`（dark `#3a2a10`/`--amber`）；其余 = `--soft`/`--dim`。
- **card-actions（卡片悬浮操作层）**：hover / focus-within 时浮现，`inset:0` 全卡覆盖、居中排两个 38px 圆形按钮——☆/★ 收藏（激活与 hover 均为 `#f5a623`）、🗑 移入垃圾箱（hover 变 `--red`）；背底 `rgba(255,255,255,.62)` + `backdrop-filter:blur(3px)`（dark `rgba(12,13,17,.62)`）。`@media (hover:none)` 时改为常显、贴卡片右上角、32px 小按钮。
- **README 索引卡（doc-card.index）**：不再用虚线——**蓝色渐变卡**：`border:0; box-shadow:none; background:linear-gradient(160deg, var(--card) 30%, var(--blue-soft) 130%)`；hover 无位移无浮影；badge 用 `badge.blue`（`--blue-soft` 底 `--blue` 字）「索引」；foot 右标签为「区域入口」。区域内排序永远第一。
- **tool card**：`padding:16px 18px; border-radius:18px; display:flex; flex-direction:column; gap:8px`；hover 浮影同 doc 卡。顶行：**30px 圆形字母头像**（`border-radius:50%; background:var(--blue-soft); color:var(--blue); font-weight:700; font-size:12px`）+ 名称 13px/600 + 右对齐 tag（`background:var(--soft); color:var(--dim); border-radius:6px; font-size:9.5px`）。描述 11.5px dim 两行截断。底行：**命令 code 芯片**（等宽 10.5px，`color:var(--blue)` 配 `--blue-soft` 底、6px 圆角、单行 ellipsis）+ **复制**按钮（10px、`--line` 细边框）+ **打开 ↗** 按钮（无边框、13px、hover 变蓝）。
- **search 胶囊**：`width:380px; max-width:40vw; border-radius:999px; padding:13px 18px; background:var(--card); border:0; box-shadow:var(--shadow)`；内含 16px 放大镜 SVG（`color:var(--dim)`）+ 透明无边框 input 13.5px；**focus-within 加蓝环** `box-shadow:0 0 0 3px rgba(0,145,255,.16), var(--shadow)`。≤900px 占满整行（`order:3` 移到 header 下一行）。
- **modal 弹窗**：`width:min(560px,92vw); max-height:560px; border-radius:20px; background:var(--card); border:1px solid var(--line); box-shadow:0 24px 60px rgba(0,0,0,.25)`，开合 `scale(.96)→1`；overlay 全屏 `rgba(15,15,20,.42)` + blur(3px)。结构：头部（15.5px/700 标题 + 11.5px dim 副标 + 30×30 ✕ 关闭钮）→ 可滚动 body。列表项 `m-item`：`--soft` 底 12px 圆角，标题 13px/600 单行 ellipsis + 副行 11px dim + 右侧操作（打开蓝链 / 移除 / 恢复蓝钮）。
- **toast**：`position:fixed; left:50%; bottom:26px; transform:translateX(-50%)`；胶囊 `border-radius:999px; padding:10px 18px; font-size:12.5px`；light 黑底白字、dark 反转白底黑字；淡入 + 上浮 8px，1.8s 后消失；`pointer-events:none`。
- **empty**：无匹配时网格位置显示居中 dim 文案（如「没有匹配的文档」），`padding:40px 4px`。

## 字体与数字

- 基准：`font:13px/1.55 <系统栈>`；层级 28px 标题 / 32px hero 大数字 / 29px metric 数字 / 20px 区域题 / 15px 卡题 / 12.5–13px 正文 / 10.5–12px 辅助。
- **数字一律 `font-variant-numeric:tabular-nums`**：统计、端口、计数、日期等宽对齐。
- **大数字 24–44px，`font-weight:700`，负字距**：29–32px → `-1.2px`，28px 标题 → `-.7px`，更大字号加大负值。
- 地址/命令/类型等机器可读信息一律等宽栈，绝不用正文字体。

## 交互规范

- **搜索实时过滤（含全文）**：`input` 事件驱动，对 `title + desc + cat + search`（全文索引，预置小写）做小写包含匹配；同时过滤文档区域与工具；工具计数显示「命中 / 总数」；无结果显示 empty。
- **`/` 聚焦**：全局 keydown，按 `/` 且焦点不在输入框时 `preventDefault` 并聚焦搜索框。
- **chips 过滤**：点选分类即时重渲染区域与 chips（选中态蓝底白字），chips 带每类计数，第一项为「全部」。
- **只看当前开关**：即时生效——重渲染 + toast 反馈（「只显示当前文档 / 显示全部状态」）。
- **卡片点击打开目标**：文档卡整卡 `<a>` **同页导航**（v2 不再 `target="_blank"`）；服务胶囊在线时跳转 url；工具「打开」同页跳转源文件；「复制」走 Clipboard API（失败回落 toast 提示，不用 prompt）。
- **收藏 / 垃圾箱 / 删除流程**：卡片 hover 浮出 ☆/🗑 → 收藏 toggle、删除走确认弹窗（danger 红钮）；工具栏 ⭐/🗑 打开对应弹窗，支持移除收藏、恢复、过期转档。所有写操作走 `api()`：`fetch POST`（JSON），**失败时 toast「该操作仅在线门户可用」并保持只读**——file:// 离线版可完整浏览不可写。后端只需四个接口：`/api/favs`（toggle，返回全量数组）、`/api/trash`（移入）、`/api/trash/restore`（恢复）、`/api/trash/purge`（过期转档）。
- **弹窗**：Esc 或点遮罩/✕ 关闭；`role="dialog" aria-modal="true"`。
- **hero 刷新钮**：点击 360° 旋转 420ms + toast 状态回执。
- **排序**：区域内 README 索引卡永远第一；其余按状态（当前 > 候选 > 其他）再按更新日期倒序。
- 动效克制：仅 hover 位移/浮影、开关滑块、toast 淡入、弹窗缩放四类 `0.12–0.18s` 过渡；`prefers-reduced-motion: reduce` 时全部关闭。

## 硬规则

1. **不用侧边栏**。本风格明确无侧栏，单列自上而下（header → hero 行 → services → toolbar → 区域 → 工具 → 页脚）。参考图有左侧栏，落地时已移除（见 measurements.md 差异说明）；任何「加个侧栏导航」的需求都与本风格冲突。
2. **文档优先于仪表盘**。文档区域是页面主体，hero/metric 行只是三张仪表盘卡；工具区永远放最后。
3. **不依赖 CDN**。纯内联 HTML/CSS/JS（含 inline SVG），无外部字体、图标库、脚本；file:// 直开可用。
4. **响应式 390px 可用**。断点 900px / 680px：hero 行 2 列→1 列、网格单列、搜索整行、blob 缩小；任何元素不给超出屏幕的 min-width。
5. **阴影近乎扁平**。基础 `--shadow` 仅 1px 3px 极低透明度；hover 反馈用位移 + 中度浮影，不做夸张立体。

## 文件

- `assets/starter.html`：自包含起步模板，内联假数据演示全部组件与交互；接入真实数据时替换脚本顶部的 `DOCS / FAVS0 / TRASH0 / TOOLS / SERVICES / GIT / LINK_BASE / TOOL_BASE` 常量，接入后端时实现四个 `/api/*` 接口即可。
- `references/measurements.md`：参考图采样色值、OCR 布局观测、落地差异与 v1→v2 演进记录。

## 参照来源

本风格取样自**用户提供的 Clash 代理面板截图**（2000×1233）。采样色值（背景 `#f2f0f3`、卡片 `#fcf9fa`、边框 `#e8e6e8`、蓝 `#0091ff`、绿 `#a1f7a1` 等）与 OCR 观测到的布局要点（大字数字统计、等宽 IP、服务表、策略组 tile、右上角勾选控件）记录在 [references/measurements.md](references/measurements.md)。**截图不复制进仓库**，需复测时向用户索取原图。落地时保留了参考图的暖灰底、近白卡、iOS 蓝、胶囊大圆角、tabular 数字语言，但按「文档优先门户」重组了版式（去侧栏、工具殿后）；v2 进一步把表面提亮（`#f9f7fa`/`#ffffff`）并加入 hero 行、收藏/垃圾箱体系，差异与演进明细见 measurements.md。
