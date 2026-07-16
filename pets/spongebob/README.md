# SpongeBob Codex Pets

SpongeBob 主题 Codex 桌宠集合。每个角色都按 Codex 的 9 行状态图集制作，保留角色的经典轮廓、表情和小动作。

## 角色

| 角色 | 路径 | 特色动作 |
| --- | --- | --- |
| SpongeBob | [`spongebob`](./spongebob) | 方形海绵身体、灿烂表情、铲子工作循环 |
| Mr. Krabs | [`mr-krabs`](./mr-krabs) | 红色蟹钳、数钱工作循环、老板式反应 |
| Plankton | [`plankton`](./plankton) | 单眼、触角、反派小手势和小装置动作 |
| Patrick | [`patrick`](./patrick) | 粉色海星身体、犯困表情、傻乎乎跳跃 |
| Squidward | [`squidward`](./squidward) | 长鼻子、厌世表情、单簧管工作循环 |

## 安装

从仓库根目录安装全部 SpongeBob 主题桌宠：

```bash
./install.sh spongebob
```

只安装一个角色：

```bash
./install.sh spongebob/spongebob
./install.sh spongebob/mr-krabs
./install.sh spongebob/plankton
./install.sh spongebob/patrick
./install.sh spongebob/squidward
```

## 版本说明

这一组目前是 Codex v1 宠物格式：`1536x1872`，8 列 x 9 行状态图集。v2 需要额外生成 16 个 look-direction 姿态；等生成路径稳定后再批量升级。
