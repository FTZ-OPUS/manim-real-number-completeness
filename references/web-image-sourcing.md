# 联网搜图方法论（肖像 / 插图素材）

> 用途：历史人物肖像（如样板间的柯西、魏尔斯特拉斯、戴德金、康托尔）、封面插图、定理人物头像等。
> 本文件写给**执行 agent**（你或客户的 AI），按此流程用自带的联网工具完成搜集与落盘。

## 1. 版权红线（先读）

1. **只收公共领域（Public Domain）或 CC0** 的图。19 世纪及更早人物的翻拍肖像在 Wikimedia Commons 上绝大多数是 PD——这正好覆盖数学史主角群（欧拉、高斯、柯西、魏尔斯特拉斯、戴德金、康托尔、黎曼…）。
2. 优先 `Wikimedia Commons`；其次 Flickr Commons、博物馆开放接口（大英图书馆、Rijksmuseum 等）。
3. **CC-BY 可以用但必须署名**；任何带水印、来路不明的百度图片/谷歌图片直链**禁止**入片。
4. 每张图登记来源：`assets/portraits/SOURCES.md` 一行一图：`文件名 | 来源URL | 许可 | 作者/拍摄年代`。

## 2. 搜索工作流（agent 工具映射）

| 步骤 | 工具 | 做法 |
|---|---|---|
| ① 定候选 | `WebSearch` / 搜索引擎 | query 模板见 §3 |
| ② 进 Commons 条目页 | `WebFetch` | 读文件页拿**原图直链**、许可、分辨率 |
| ③ 下载 | `curl -L -o` / 浏览器 | 落盘到 `assets/portraits/`，见 §4 命名 |
| ④ 质检 | `ffprobe`/看图 | 分辨率 ≥800px、面部完整、无水印、风格与全片协调 |
| ⑤ 登记 | Write | 更新 SOURCES.md |

Commons 直链规律：文件页 `https://commons.wikimedia.org/wiki/File:XXX.jpg` → 原图在
`https://upload.wikimedia.org/wikipedia/commons/...`；也可用 Special:FilePath 重定向：
`https://commons.wikimedia.org/wiki/Special:FilePath/XXX.jpg?width=1200`（`width` 参数直接要缩放版，省流量）。

## 3. 搜索词模板

```
# 英文（命中率最高）
<人名拉丁转写> portrait wikimedia commons          # 如 "Karl Weierstrass portrait wikimedia commons"
<人名> mathematician 19th century photograph public domain
# 中文
<人名> 数学家 肖像 公有领域 维基共享
# 插图类
mathematical illustration <主题> public domain line art
```

优先级：**照片（19 世纪达盖尔/银版）> 版画 engraved > 油画**。同一人物可同时收照片版与版画版
（命名 `cauchy.jpg` / `cauchy_engraved.jpg`），总览画卷用照片、个人特写用版画增加变化（样板间即此用法）。

## 4. 落盘与代码对接

```
assets/portraits/
├── cauchy.jpg            # 全小写人名，下划线分隔
├── cauchy_engraved.jpg
├── SOURCES.md            # 来源登记（见 §1.4）
```

```python
# 场景代码里永远基于 BASE_DIR 相对寻址，禁止写死用户目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTRAITS_DIR = os.path.join(BASE_DIR, "assets", "portraits")
img = ImageMobject(os.path.join(PORTRAITS_DIR, "cauchy.jpg"))
img.scale_to_fit_height(3.0)          # 相框内图高 2.7~3.0 单位
# ImageMobject 不是 VMobject：多元素组合用 Group，不能用 VGroup！
card = Group(frame_box, img, t_name, t_desc)
```

## 5. 质量与风格统一

- 全片人物图**色调统一**：样板间在深色相框（`fill_color="#182230"` 圆角矩形）中呈现，暖旧照片与黑白版画都协调。
- 分辨率下限 800px（1080p 全屏占 1/3 时不出糊）；≤2MB/张，避免拖慢渲染。
- 人物名条：图下 `zh("柯西 (A. Cauchy)")` + 一行 `zh(desc, color=MUTED)`，字号 24~26/18~20。

## 6. 兜底顺序

1. Commons PD 原图（首选）→ 2. 同人物另一风格版本 → 3. 时代相近的同国籍数学家群像裁切（谨慎，需客户确认）→
4. 纯排版方案（姓名+年代+贡献的大字卡片，无图也不塌）——样板间历史篇的卡片结构可直接复用。
**绝不使用**：AI 生成人物肖像冒充历史照片（学术诚信红线，除非客户明确要求并接受标注）。
