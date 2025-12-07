---
sidebar_position: 3
---

# Supabase 同步

使用免费的 PostgreSQL 云数据库同步数据。

## 什么是 Supabase？

[Supabase](https://supabase.com/) 是一个开源的 Firebase 替代品，提供免费的 PostgreSQL 数据库。

## 优势

- ✅ 免费额度充足（500MB 数据库）
- ✅ 跨平台（iOS/Android）
- ✅ 实时同步
- ✅ 数据完全可控

## 配置步骤

### 1. 注册 Supabase

访问 [supabase.com](https://supabase.com/) 注册账号。

### 2. 创建项目

1. 点击「New Project」
2. 输入项目名称
3. 设置数据库密码
4. 选择区域（推荐选择亚洲）
5. 创建项目

### 3. 获取配置信息

在项目设置中找到：

- **Project URL** - 项目地址
- **anon public key** - 公开密钥

### 4. 配置蜜蜂记账

1. 进入「我的」→「云服务」
2. 选择「Supabase」
3. 输入 Project URL 和 anon key
4. 保存并测试连接

## 数据库表

首次连接会自动创建所需的数据表，无需手动操作。

## 注意事项

- 免费版有一定限制，个人使用足够
- 长期不活跃的项目可能被暂停
