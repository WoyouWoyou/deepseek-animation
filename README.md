# deepseek-animation

把中文文案、画风提示词和声音做成**前后连贯的代码动画**（Remotion / Canvas / HTML）的技能。

> 免费分享，欢迎免费使用、免费分享；请不要包装成付费课程、付费 skills 或收费资料出售。详见 [LICENSE.md](./LICENSE.md)。

## 它解决什么

做中文动画最容易做成「逐句贴卡的 PPT」：一句话一张图、图标加淡入、每镜时长平均。这个技能把「意思的变化」拆成可执行的流程——读懂全文 → 语义分镜 → 选画风 → 镜头/转场/动作/字体/声音 → Remotion 落地 → 检查返修。

## 包含什么

| 目录 | 内容 |
| --- | --- |
| `SKILL.md` | 总入口：创作顺序、能力路由、质量底线 |
| `modules/` | 方法与判断：语义、风格、字体、背景、运动、镜头、风格分支、影像、产品、音乐、实现、交接、质量 |
| `recipes/` | 具体配方：叙事、气势词、活的背景、群体翻面、镜头运动、转场、接缝、角色、纸偶、风格化、图片快闪、图表地图、音乐音效、UI 16 式 |
| `implementations/` | 可复用源码：motion-core、canvas 契约、Remotion kit、相机/角色/转场/背景/中文文字/数据 UI、specimen 实验场 |
| `adapters/` | 外部对接：341 风格库接口、Remotion、ACE-Step 本机音乐 |
| `templates/` | 任务卡、分镜表、音乐方案、返修表 |
| `examples/` | 7 个完整任务卡与演练 |
| `scripts/` | `doctor.py` 自检、`style_library.py` 风格库索引、`package.py` 打包、`validate_task.py` 任务卡校验、`glyph_outline.py` 字形轮廓 |
| `tests/` | 逻辑、Canvas 契约、任务卡契约测试 |
| `风格提示词/` | 341 种画风提示词原文，其中 193 种带同名静帧 `jpg` |
| `LICENSES/` | 第三方来源与许可；`LICENSES/风格库/` 记原库的说明、来源与三方许可 |

## 两种发布包

| 包 | 内容 | 适用 |
| --- | --- | --- |
| `deepseek-animation-<版本>-bundled.zip` | 技能 + `风格提示词/` 341 条原文与 193 张静帧（约 14 MB） | 开箱即用，不依赖外部路径 |
| `deepseek-animation-<版本>-index-only.zip` | 技能 + 索引快照，不含原文（约 0.3 MB） | 已有自己的一份库，或受分发授权限制 |

两种包解压后目录结构相同；`bundled` 包里的 `风格提示词/` 会被自动识别为库根，`index-only` 包则需要指定 `--root`。

## 安装

把整个 `deepseek-animation/` 目录复制进你的技能目录即可，包内全是相对路径、不依赖本机绝对路径：

```sh
git clone https://github.com/WoyouWoyou/deepseek-animation.git
cp -r deepseek-animation ~/.dsh/skills/    # 按你的技能目录位置调整
```

## 第一次使用

1. 库的解析顺序：`--root` > `FY_STYLE_LIBRARY_ROOT` > 包内 `风格提示词/` > `adapters/style-library.config.json` 的 `root`。`bundled` 包直接可用；`index-only` 包需要自己的库路径（库根下应有 `风格提示词/`，可选 `示例/`）。
2. 先跑一次自检：

   ```sh
   python scripts/doctor.py                     # 内置库
   python scripts/doctor.py --root /你的/风格库   # 外部库
   ```

3. 之后按 `SKILL.md` 的创作顺序调用；只交任务卡时不生成任何媒体。

## 打包

```sh
python scripts/package.py    # 输出到 dist/，按有无 风格提示词/ 自动选择 bundled 或 index-only
```

## 要求

- Python 3.10+（脚本与契约测试）
- Node 20+（`tests/test_logic.mjs`、`tests/test_canvas_contract.mjs`）
- Remotion / Canvas / HTML 任选其一落地，依赖按项目自带

## 测试

```sh
python scripts/doctor.py          # 核心文件与风格库自检
python tests/test_contracts.py    # 13 个任务卡契约用例
node tests/test_logic.mjs         # 12 个运动/时间逻辑用例
node tests/test_canvas_contract.mjs
```

## 下载

- Release 附件按版本提供 `bundled` 与 `index-only` 两种 zip
- 也可以直接用源码：整个目录复制即安装

## 许可

见 [LICENSE.md](./LICENSE.md)。包内第三方内容保留各自原有许可，来源、版权与许可声明记录在 [LICENSES/README.md](./LICENSES/README.md)。
