---
sidebar_position: 2
description: BeeCount Cloud 是蜜蜂记账官方推出的自建云同步服务,Docker 一键部署,支持手机+Web+平板多端实时协同,数据完全自主掌控。
keywords: [BeeCount Cloud, 蜜蜂记账自建云, Docker记账云, 自建记账同步, 多端同步记账]
---

# BeeCount Cloud 自建云

> 3.0 新增 · 官方推荐的多设备实时同步方案

BeeCount Cloud 是**官方推出的自建云同步服务端**,用 Docker 一行命令就能跑起来,支持:

- 🔄 **多设备实时协同**:手机 A 改一笔,几秒内推到手机 B 和 Web
- 🌐 **内置 Web 管理端**:一个 Docker 镜像包含 server + web + PWA,浏览器直接用
- 👥 **多用户独立**:一个服务器可以多人注册账号,各自数据完全隔离
- 🐳 **一键部署**:Docker Compose 配置文件不到 10 行

## 适合谁

| 用户类型 | 推荐理由 |
|---------|---------|
| 🏠 家庭多人记账 | 每人注册一个账号,数据各自独立(共享账本规划中) |
| 📱 单人多设备 | 手机 / iPad / Web 三端秒级同步,不用手动"上传下载" |
| 🖥️ 有 NAS / VPS 的用户 | Docker 一键跑起来,数据在自己机器上 |
| 👨‍💻 技术用户 | 开源、可审计,想二次开发也可以 |

## 一键部署

将下面的内容存为 `docker-compose.yml`:

```yaml
services:
  beecount-cloud:
    image: sunxiao0721/beecount-cloud:latest
    restart: unless-stopped
    ports:
      - "8869:8080"
    volumes:
      - ./data:/data
```

启动:

```bash
mkdir -p beecount && cd beecount
# 把上面 yaml 存为 docker-compose.yml
docker compose up -d
```

首次启动时,Docker 会:

1. 在 `./data/beecount.db` 自动建库 + 跑 migration
2. 生成 `./data/.jwt_secret`(32 字节强密钥,600 权限)
3. 自动创建一个**管理员账号**,随机 16 位密码

## 拿到管理员账号

### 方式 1:从日志里看(推荐)

```bash
docker compose logs beecount-cloud | grep -A 10 "初次启动"
```

会看到:

```
========================================================================
 BeeCount Cloud — 初次启动,已自动创建管理员账号:

   邮箱:    owner@example.com
   密码:    FIDodUnwprkw1zUi

   凭证已落盘到 /data/.initial_admin_password(volume 内,600 权限)
========================================================================
```

### 方式 2:从文件读

```bash
cat ./data/.initial_admin_password
```

## 登录使用

### Web 管理端

浏览器访问 `http://<你的服务器>:8869`,用管理员账号登录。

第一次登录后建议**立即修改密码**(右上角头像 → 账户设置)。

### 手机 App 连接

1. 打开蜜蜂记账 → **我的** → **云同步**
2. 选择 **BeeCount Cloud** 服务
3. 填服务器地址(例如 `http://192.168.1.100:8869`)+ 管理员邮箱密码
4. 登录后首次会全量上传本地所有账本到服务器

## 添加家人 / 队友

**BeeCount Cloud 不支持自助注册**(避免公网暴露被滥用),账号只能由管理员添加。

1. 管理员登录 Web 后台 → 左侧菜单 **用户**
2. 点击 **新增用户**,输入对方邮箱 + 临时密码
3. 把账号发给对方,让 ta 在手机 App 或 Web 登录

目前每个用户的数据独立,互相看不到对方账本。**共享账本(多人编辑同一个账本)已在规划中**,敬请期待。

## 进阶配置

### 自定义管理员账号

默认首次启动生成随机密码。如果想自己指定:

```yaml
services:
  beecount-cloud:
    image: sunxiao0721/beecount-cloud:latest
    restart: unless-stopped
    ports:
      - "8869:8080"
    environment:
      BOOTSTRAP_ADMIN_EMAIL: me@example.com
      BOOTSTRAP_ADMIN_PASSWORD: <你的强密码>
    volumes:
      - ./data:/data
```

两个环境变量**只在"库里一个 user 都没有"时生效**,之后改它们不会动老账号。

### 自定义 JWT 密钥

默认会自动生成 `/data/.jwt_secret`。如果你有密钥管理系统想自己托管:

```yaml
environment:
  JWT_SECRET: <32+ 字节的强随机串>
```

设置这个变量后,系统不会再生成或读取文件。

### 公网部署

建议在前面套一层 nginx / Caddy 做 HTTPS + 域名绑定:

```
用户 ─HTTPS─► Caddy/Nginx ─http://localhost:8869─► BeeCount Cloud
```

App 和 Web 都支持 `https://` 地址。

### 数据备份

所有持久化数据都在 `./data/` 目录:

- `beecount.db` —— SQLite 数据库(账本、交易、用户)
- `attachments/` —— 附件文件(头像、交易图片、分类自定义图标)
- `backups/` —— 备份归档
- `.jwt_secret` —— JWT 签名密钥(丢了所有用户 token 失效,需要重新登录)

备份整个 `data/` 目录就是完整备份,迁到新服务器直接 `rsync` 过去启动即可。

## Web 端支持 PWA

Web 管理端是**渐进式 Web 应用**(PWA):

- 浏览器地址栏右侧会出现"**安装**"图标,点一下装到桌面 / Dock / 开始菜单
- 装成独立 app 后,打开无浏览器地址栏,近似原生体验
- 离线时可以读缓存数据,回网后自动同步

## 升级

```bash
cd beecount
docker compose pull
docker compose up -d
```

数据库自动 migrate。`data/` 目录不动。

## 常见问题

### Q: 手机连不上服务器

检查:

- 防火墙是否放行 `8869`(或你自己映射的端口)
- 手机和服务器在同一网络(或通过公网 IP / 域名)
- 服务器地址前缀是 `http://` 还是 `https://`,别写错

### Q: 启动后 `docker compose logs` 没看到管理员 banner

可能已经不是首次启动了。密码文件在 `./data/.initial_admin_password`。
如果文件也丢了,可以用 `BOOTSTRAP_ADMIN_EMAIL` + `BOOTSTRAP_ADMIN_PASSWORD` env 配一个新账号(仅当库里没任何 user 时生效)。如果库里已有账号需要重置密码,管理员登录 Web → 用户 → 编辑修改即可。

### Q: 服务器迁到新机器

- 旧机器:`docker compose down`
- 把 `data/` 目录 `rsync` 到新机器
- 新机器:同样的 `docker-compose.yml`,`docker compose up -d`
- App 里服务器地址改成新的,重新登录

### Q: Web 端能改主题色吗

可以。右上角头像 → 账户设置 → 主题色。每个用户的偏好独立,不影响别人。

## 相关仓库

- [BeeCount-Cloud](https://github.com/TNT-Likely/BeeCount-Cloud) —— server + Web UI 代码
- [BeeCount](https://github.com/TNT-Likely/BeeCount) —— mobile app 代码
