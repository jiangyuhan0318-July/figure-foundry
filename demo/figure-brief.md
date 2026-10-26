# 示例绘图 brief

日期：2026-10-26。实际加载技能：`figure-foundry`，使用数据图路线及其 `references/data-plots.md`。

目的：演示一个可复跑的科研图件流程，展示学习趋势、逐次运行差异及精度/延迟取舍。数据由用户明确授权编造，全部标为合成，不代表真实实验。

- 画幅：180×140 mm；图内英文短标签，报告中文；不是特定期刊的尺寸规范。
- 配色：用户的暖橙组。Baseline=`#C8C8C8`/圆点/虚线；Variant A=`#F1D5B3`/方点/点划线；Variant B=`#F29440`/菱形/实线。深色描边为中性辅助色。
- A：整行宽的学习曲线，均值±1 SD；B：最终值的配对观测与均值±1 SD；C：逐运行延迟/最终值散点以及二维均值±1 SD。
- 原始数据：`synthetic_data.csv`，3方法×8模拟运行×21训练检查点=504行。同一run_id在方法间配对；检查点不是独立样本。
- 生成方式：固定种子20261026的饱和曲线、共享运行偏移与小幅噪声。数据中没有真实实验或真实模型结果。延迟是人为设定的模拟变量。
- 参考：实际查看了AgentFigureGallery的[图类型示例预览](https://github.com/Dsadd4/AgentFigureGallery/blob/0b55f26fd575a00b5ebacb619d953b0a008e0126/examples/plot_type_examples/figures/agentfiguregallery_plot_type_examples_preview.png)，借鉴白底、轻网格、原始观测和多面板组织，不复制其图像、代码或数据。
- 源场景：`plot_demo.py`读取CSV，经已安装技能的样式/导出帮助脚本生成PNG/SVG/PDF。
- 计划检查：行数与分组、均值/SD、检查点计数、配色、图内合成声明、文字边界、图像/矢量尺寸，以及实际图片中的重叠和可读性。
