# swording-k/codex-pet

我的 **Codex 自定义桌宠集合**。每个桌宠都在 `pets/<pet-name>/` 子目录下，有自己的元数据、图片、配置说明。

## 🐾 桌宠列表

| 桌宠 | 简介 | 类型 |
|---|---|---|
| [codex-buddy-pet](./pets/codex-buddy-pet) | 健身小人 chibi 形象，8x9 sprite sheet | `gym-buddy` |

## 🚀 如何安装桌宠

每个桌宠的 README 里都写明安装方式（通常是把 `pet.json` + 图片资源复制到 Codex 的桌宠目录），点进链接查看。

## 📝 通用安装流程（参考）

Codex 桌宠一般放在：
```
~/.codex/pets/<pet-name>/
  ├── pet.json
  ├── spritesheet.webp   (或 .png)
  └── contact-sheet.png  (可选)
```

具体路径以每个桌宠 README 为准。

## 🤝 添加新桌宠

1. 在 `pets/<new-pet-name>/` 下创建子目录
2. 放 `pet.json` + sprite 资源 + `README.md`
3. 在本 README 的"桌宠列表"加一行
4. 提 PR
