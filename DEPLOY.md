# Fly.io 部署指南

## 前置要求

1. 安装 [Fly CLI](https://fly.io/docs/getting-started/installing-flyctl/)
2. 注册 [Fly.io 账号](https://fly.io/)
3. 登录 Fly.io: `fly auth login`

## 部署步骤

### 1. 初始化 Fly.io 应用（如果还没有）

在项目根目录（包含 `fly.toml` 和 `Dockerfile` 的目录）执行：

```bash
fly launch
```

若提示是否使用现有的 `fly.toml`，选择 **Yes**。

### 2. 创建数据持久化 Volume

为了保存用户数据和管理员信息，需要创建一个 volume：

```bash
# 创建 volume（只需要执行一次）
fly volumes create rolex9_bot_data --size 1 --region sin
```

**注意：** 
- `--size 1` 表示 1GB 存储空间（足够存储大量用户数据）
- `--region sin` 必须与 `fly.toml` 中的 `primary_region` 一致
- 如果 volume 已存在，会提示错误，可以忽略

### 3. 设置环境变量

设置 Telegram Bot Token 和可选配置（通过 `fly secrets set`，不会写入代码仓库）：

```bash
# 设置 Bot Token（必需）
fly secrets set BOT_TOKEN="你的bot_token"

# 可选：覆盖频道或链接（不设置则使用 config.py 中的默认值）
# fly secrets set TELEGRAM_CHANNEL="https://t.me/你的频道"
# fly secrets set FREE_SPIN_URL="https://..."
# fly secrets set FREE_CREDIT_URL="https://..."
# fly secrets set DATA_DIR="/data"
```

### 4. 部署应用

在项目根目录执行（Fly 会使用当前目录的 `Dockerfile` 构建镜像）：

```bash
fly deploy
```

### 5. 查看日志

```bash
# 实时查看日志
fly logs

# 查看最近的日志
fly logs --tail 100
```

### 6. 检查应用状态

```bash
# 查看应用信息
fly status

# 查看应用详情
fly info
```

## 常用命令

```bash
# 重启应用
fly apps restart rolex9-bot

# 查看应用配置
fly config show

# SSH 连接到容器（调试用）
fly ssh console

# 查看应用监控
fly dashboard
```

## 注意事项

1. **数据持久化**: 机器人通过 `DATA_DIR`（默认 `/data`）读写数据。`fly.toml` 中已将 volume `rolex9_bot_data` 挂载到 `/data`，因此 `user_stats.json` 和 `admins.json` 会持久化保存，容器重启不会丢失。

2. **环境变量**: 敏感信息（如 `BOT_TOKEN`）必须用 `fly secrets set` 设置。其他配置（如 `TELEGRAM_CHANNEL`、`FREE_SPIN_URL`、`FREE_CREDIT_URL`）可在 `config.py` 中查看默认值，需要覆盖时用 `fly secrets set`。

3. **构建与运行**: 部署使用项目根目录的 `Dockerfile`（Python 3.11）和 `fly.toml`，进程命令为 `python bot.py`。区域在 `fly.toml` 的 `primary_region`（当前为 `sin` 新加坡），可改为 `hkg`、`nrt` 等。

4. **监控**: 使用 `fly logs` 监控运行状态，确保 bot 正常。

## 故障排查

如果 bot 无法启动：

1. 检查日志: `fly logs`
2. 检查环境变量: `fly secrets list`
3. 检查应用状态: `fly status`
4. SSH 进入容器检查: `fly ssh console`

## 更新部署

修改代码后，重新部署：

```bash
fly deploy
```
