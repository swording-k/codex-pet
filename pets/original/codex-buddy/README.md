# Codex Buddy 桌宠

[中文](README.md) | [English](README.en.md)

Codex Buddy 是一套自定义 Codex 桌宠资源：一个戴蓝色反戴帽、穿白色 T 恤和橙色星星短裤的健身小人，包含多种 Codex 状态动画。

这个资源包很轻量，Codex 自定义桌宠只需要两个核心文件：

- `pet.json`
- `spritesheet.webp`

`contact-sheet.png` 是动作预览图，方便安装前检查每一行动画。

## 手动安装

下载或克隆本仓库，把桌宠文件复制到 Codex pets 目录：

```bash
mkdir -p ~/.codex/pets/codex-buddy
cp pet.json spritesheet.webp ~/.codex/pets/codex-buddy/
```

最终结构应为：

```text
~/.codex/pets/codex-buddy/
├── pet.json
└── spritesheet.webp
```

复制完成后重启 Codex。如果 Codex 已经加载过其他桌宠，重启是让新图集生效的稳妥方式。

## 在 Codex 里启用

请先把 Codex 更新到最新版本，确保客户端已经支持自定义桌宠。重启后打开 Codex 设置，点击“外观”下拉菜单，在自定义宠物列表中选择 Codex Buddy。

如果没有看到 Codex Buddy，请检查 `pet.json` 和 `spritesheet.webp` 是否已经放在同一个目录下：

```text
~/.codex/pets/codex-buddy/
```

确认文件位置无误后，再重启一次 Codex。

## 让 Codex 帮你安装

也可以把这个仓库链接发给 Codex，让 Codex 自动下载并配置：

```text
请帮我安装这个 GitHub 仓库里的 Codex 桌宠：
https://github.com/swording-k/codex-buddy-pet

请下载仓库，把 pet.json 和 spritesheet.webp 复制到 ~/.codex/pets/codex-buddy/，不要删除其他桌宠。完成后提醒我重启 Codex。
```

## 状态动画

Codex 读取固定的 8 列 x 9 行图集。每一行对应一个应用状态：

| 行 | 状态 | 动画 |
| --- | --- | --- |
| 0 | `idle` | 平静站立与哑铃呼吸循环 |
| 1 | `running-right` | 向右移动 |
| 2 | `running-left` | 向左移动 |
| 3 | `waving` | 挥手问候 |
| 4 | `jumping` | 引体向上/跳跃动作 |
| 5 | `failed` | 卧推失败 |
| 6 | `waiting` | 等待输入 |
| 7 | `running` | 肩推任务循环 |
| 8 | `review` | 哑铃弯举检查 |

## 文件说明

- `pet.json`：Codex 自定义桌宠配置文件
- `spritesheet.webp`：支持透明背景的 WebP 图集，1536 x 1872 像素，每格 192 x 208
- `contact-sheet.png`：全部动作行的预览图
