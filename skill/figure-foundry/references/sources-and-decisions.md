# 来源筛选与合并决策

本技能由 July 与 Codex 在 2026-10-26 整理。目标是以论文数据图为主、方法/架构图为辅的完整绘图流程。说明经过重写与分流，原仓库不是运行时依赖。

## 五个候选的核验

星标来源为 GitHub 仓库 REST API，核验日期 2026-10-26（Asia/Shanghai）；归档时间 02:12。星标随时间变化，且不等于某个子技能的独立使用量或绘图质量。

| 仓库 | Stars | 实际查看的许可 | 决策 |
|---|---:|---|---|
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 60,995 | MIT | 选入：视觉层次、语义优先、少量强调、连线/标签与导出检查。 |
| [BAIKEMARK/happy-figure-skill](https://github.com/BAIKEMARK/happy-figure-skill) | 172 | CC BY-NC-SA 4.0 | 未选入：主要交付绘图提示词；不补足数据作图执行，且该许可带来不同的复用条件。 |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | 170 | MIT | 选入：实际参考图、稳定的类别/偏好、从参考到绘图代码。 |
| [gxCaesar/open-research-skills](https://github.com/gxCaesar/open-research-skills) | 58 | Apache-2.0 | 选入其中 build-scientific-visualizations：源数据、独立单位、整图构图、可编辑源与实际渲染检查。该星标是整个工具箱的数量。 |
| [plbbl/academic-diagram-skill](https://github.com/plbbl/academic-diagram-skill) | 6 | 原创指令/文档为 MIT，参考图另有权利范围 | 未选入：设计思路有价值，但在本次三源组合中与示意图路线重合，不再增加第四套流程。 |

因此不是机械取星标前三。选入三个互补的来源：通用视觉设计、参考图选择、科研图件执行。未把“只有六星”解释为质量较差，也没有复制任何仓库的第三方论文图片或图库。

## 固定的来源版本

| 来源 | 仓库提交 | 被分析的入口 |
|---|---|---|
| Diagram Design | `0b9b10cab3dbf695642fa1a6c4b4f60df9083689` | [skills/diagram-design/SKILL.md](https://github.com/cathrynlavery/diagram-design/blob/0b9b10cab3dbf695642fa1a6c4b4f60df9083689/skills/diagram-design/SKILL.md) |
| AgentFigureGallery | `0b55f26fd575a00b5ebacb619d953b0a008e0126` | [skills/agent-figure-gallery/SKILL.md](https://github.com/Dsadd4/AgentFigureGallery/blob/0b55f26fd575a00b5ebacb619d953b0a008e0126/skills/agent-figure-gallery/SKILL.md) |
| Open Research Skills | `c79bac60f882b626e1754bff95101441e165e4ec` | [skills/build-scientific-visualizations/SKILL.md](https://github.com/gxCaesar/open-research-skills/blob/c79bac60f882b626e1754bff95101441e165e4ec/skills/build-scientific-visualizations/SKILL.md) |

另外检查了 Diagram Design 的 style-guide，以及科研绘图的 source-data-contract、diagram-style-profiles、image-concept-to-vector 中与冲突相关的部分。三份主入口全文阅读；没有声称精读三个仓库的全部参考文件和源代码。

## 重复步骤与冲突处理

| 重复或冲突 | 原始位置/行为 | 本技能的统一处理 |
|---|---|---|
| 多次询问样式 | Diagram Design §0 首次品牌设定 gate；图库要求人选图；科研图另选风格/配色。 | 只建立一次 brief，优先复用已给偏好；一般绘图不等待投票。用户要求选图时再进入交互选择。 |
| 输出格式不同 | Diagram Design §12 强制单 HTML，并默认不主动导出；科研图示意图默认可编辑 PPTX。 | 数据图由代码输出 PNG+SVG/PDF；示意图默认矢量源，按请求选 PPTX/HTML。用户明确的窄格式优先。 |
| 强制概念生图 | 科研图的新示意图默认 GPT Image 2.5 概念稿→PPTX重建。 | 生图探索成为可选支线，不绑定具体后端版本。定量图始终从数据绘制。 |
| 固定字体/颜色 | Diagram Design 默认品牌字体、Coral强调及特定背景；科研图另有六组配色。 | 一个样式注册表，使用 July 的三组原始配色和本机可用字体；不拉取网络字体或改动项目既有样式。 |
| 颜色强调与类别编码混用 | 编辑型示意图偏好最多1–2个强调色；数据图可能需要3个等价类别。 | 前者只用于视觉重点，后者保持类别颜色一致，并补充形状/线型，不设全局“最多两色”。 |
| 连线规则适用范围 | Diagram Design §6 对示意图要求正交连线；数据折线、散点关系或科学几何不服从该布局。 | 正交线作为盒状流程的默认偏好，按语义允许曲线/斜线；不拿它约束数据曲线。 |
| 节点预算与整页科学内容 | Diagram Design §7 的常规节点预算/导入例外，与科研多面板图的完整角色覆盖不同。 | 按可读性安排总览、局部放大或分图；不跨模式套用一个节点数上限。原源的例外被视为有条件规则，不误报成内部矛盾。 |
| 必选图库与外部知识库 | AgentFigureGallery 需要KB路径、CLI、最多50候选、偏好数据库与bundle。 | 保留“真正看参考再画”的思想；现有参考或少量预览即可。大图库和持久偏好仅在确实需要时使用。 |
| 多层契约和重复检查 | 科研图默认多份manifest、blueprint和分阶段schema；三源都有QA。 | 普通单图只需简短brief、数据/脚本、caption与QA；复杂/受控任务再扩充。合并成一次布局→实际渲染→问题修正→导出核对。 |
| 固定精修轮数 | 科研图提供默认三轮示意图精修，其他源也有检查清单。 | 围绕实际问题迭代；满足目的与检查后停止，不为凑轮数重复绘制。 |

## 保留的质量要求

真实数据与示意内容分开；合成数据经授权并明示；误差条注明含义和独立单位；颜色不是唯一识别通道；有实际图片检查和可编辑源；同一源产生各导出；完整保留来源与许可。

## 新增的个人化部分

July 的暖橙、紫蓝粉、浅肤蓝三组颜色；数据图/示意图双路线；简化的 Matplotlib 样式/导出帮助脚本；先独立读取源数据，再绘制和核对的演示流程。没有复制第三方图库、图片、样例数据或整套运行框架。

## 许可与归属

本次重新组织和新增部分采用 Apache-2.0，源自 MIT 的相关内容继续保留原始声明。见根目录 `LICENSE`、`NOTICE`，以及 [Diagram Design MIT](../LICENSES/MIT-diagram-design.txt)、[AgentFigureGallery MIT](../LICENSES/MIT-AgentFigureGallery.txt)。参考源的许可不意味着第三方论文图、字体或外部素材自动取得同样许可。
