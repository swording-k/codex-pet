# Codex Pet Collection

我的 Codex 自定义桌宠集合。每个桌宠都是一个可直接安装的文件夹，至少包含：

- `pet.json`
- `spritesheet.webp`

`contact-sheet.png` 用于预览和检查动作。

## 桌宠分类

| 分类 | 路径 | 说明 |
| --- | --- | --- |
| Original | [`pets/original`](./pets/original) | 原创桌宠 |
| One Piece | [`pets/one-piece`](./pets/one-piece) | 海贼王角色桌宠 |

## 当前桌宠

| 桌宠 | 路径 | 简介 |
| --- | --- | --- |
| Codex Buddy | [`pets/original/codex-buddy`](./pets/original/codex-buddy) | 健身小人 chibi 桌宠 |
| Luffy | [`pets/one-piece/luffy`](./pets/one-piece/luffy) | 路飞，橡胶动作和冒险表情 |
| Chopper | [`pets/one-piece/chopper`](./pets/one-piece/chopper) | 乔巴，害羞医生动作 |

## 安装方式

### 安装全部桌宠

```bash
git clone https://github.com/swording-k/codex-pet.git
cd codex-pet
./install.sh all
```

### 安装某个分类

```bash
./install.sh one-piece
./install.sh original
```

### 安装单个桌宠

```bash
./install.sh one-piece/luffy
./install.sh one-piece/chopper
./install.sh original/codex-buddy
```

安装后重启 Codex，让它重新读取 `~/.codex/pets`。

## 让 Codex 自动安装

你也可以直接把下面这段提示词给 Codex：

```text
请从 GitHub 安装这个 Codex 桌宠集合：
https://github.com/swording-k/codex-pet

请克隆仓库，然后运行 ./install.sh all，把所有 pets 安装到 ~/.codex/pets。不要删除我已有的其他桌宠。完成后提醒我重启 Codex。
```

只安装单个角色可以这样说：

```text
请从 GitHub 安装 Luffy 桌宠：
https://github.com/swording-k/codex-pet

请克隆仓库，然后运行 ./install.sh one-piece/luffy，把它安装到 ~/.codex/pets/luffy。完成后提醒我重启 Codex。
```

## 仓库结构

```text
pets/
  original/
    codex-buddy/
      pet.json
      spritesheet.webp
      contact-sheet.png
  one-piece/
    luffy/
      pet.json
      spritesheet.webp
      contact-sheet.png
    chopper/
      pet.json
      spritesheet.webp
      contact-sheet.png
```

Codex 最终读取的位置是：

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.webp
```
