---
sidebar_position: 3
---

# Supabase 同步

使用免费的 PostgreSQL 云数据库同步数据。

## 什么是 Supabase？

[Supabase](https://supabase.com/) 是一个开源的 Firebase 替代品，提供免费的 PostgreSQL 数据库和对象存储。

## 优势

- ✅ 免费额度充足（500MB 数据库 + 1GB 存储）
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

### 3. 创建 Storage Bucket

1. 在左侧菜单点击「Storage」
2. 点击「New bucket」
3. 输入 bucket 名称：`beecount-backups`
4. **不要勾选** Public bucket（保持 Private）
5. 创建 bucket

### 4. 配置 RLS 策略

为了让 App 能正常读写数据，需要配置 RLS（行级安全）策略，确保用户只能访问自己的数据：

1. 进入「Storage」→ 选择 `beecount-backups` bucket
2. 点击「Policies」标签
3. 分别创建以下 4 条策略：

| 策略名称 | 操作类型 |
|---------|---------|
| Allow user SELECT | SELECT |
| Allow user INSERT | INSERT |
| Allow user UPDATE | UPDATE |
| Allow user DELETE | DELETE |

每条策略的配置方式相同：

- **Target roles**: 选择 `authenticated`
- **Policy definition**: 输入以下表达式

```sql
((bucket_id = 'beecount-backups'::text) AND ((storage.foldername(name))[1] = 'users'::text) AND ((storage.foldername(name))[2] = (auth.uid())::text))
```

> 此策略确保用户只能访问 `beecount-backups/users/<自己的用户ID>/` 路径下的文件。

### 5. 获取配置信息

在「Project Settings」→「API」中找到：

- **Project URL** - 项目地址
- **anon public key** - 公开密钥

### 6. 配置蜜蜂记账

1. 进入「我的」→「云服务」
2. 选择「Supabase」
3. 输入 Project URL
4. 输入 anon key
5. 输入 Storage Name：`beecount-backups`
6. 保存并测试连接

### 7.配置同步
1. 在Supabase项目左侧菜单点击「Authentication」
2. 在「User」界面点击「Add user」→「Create new user」
3. 创建邮箱和密码
4. 进入蜜蜂记账「我的」→「同步」
5. 点击「登录」，输入第三步的邮箱和密码

## 注意事项

- 免费版有一定限制，个人使用足够
- 长期不活跃的项目可能被暂停（7 天内登录即可恢复）
- 建议定期导出数据备份
