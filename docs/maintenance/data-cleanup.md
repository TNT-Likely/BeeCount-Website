---
sidebar_position: 1
title: 数据清理
description: 蜜蜂记账「数据清理」工具使用指南 — App 端清理本地孤儿数据,Web 端管理员清理服务端孤儿数据,扫描 / 勾选 / 批量删,释放磁盘空间。
keywords: [数据清理, 孤儿数据, 蜜蜂记账维护, 附件清理, 磁盘空间, 自托管管理]
---

# 数据清理

长期使用记账软件,本地数据库或附件目录里难免堆积一些**"孤儿数据"**:已删交易残留的标签关联、附件文件没了 DB 行、二级分类的父分类被删了……这些不影响日常使用,但占空间、拖慢同步,长期看也是定时炸弹。

3.2.0 / 1.3.0 起,蜜蜂记账提供了**手动数据清理工具**:扫描出所有孤儿数据,分组列出,用户勾选确认后再删 — 不自动跑、不偷偷删,**所有清理都可见**。

App 端和 Web 端各有一套工具,分别负责自己侧的数据。

## App 端:本地数据清理

### 入口

「我的」→「数据管理」→「数据清理」

### 适用范围

只清理**当前设备上的本地数据**:Drift / SQLite 数据库行 + 应用沙盒里的附件 / 图标文件 + sync_queue 待同步队列。不会动 BeeCount Cloud 服务端的数据。

### 工作流

1. 打开页面自动开始扫描(也可以点右上角刷新手动重扫)
2. 扫到的孤儿数据按三组显示:
   - **数据库孤儿**(A 类,10 种)
   - **磁盘文件孤儿**(B 类,3 种)
   - **同步队列孤儿**(C 类,1 种)
3. 每条记录显示主标题 + 副标题(如「预算 #5 · 金额 ¥3000 · 账本已删」),可单条勾选或分组全选
4. 底部统计「已选 N 项,可释放 X MB」
5. 点「清理已选」→ 二次确认 → 执行删除 → 自动重扫

### App 端检测项清单

#### A 类:数据库引用断链

| 编号 | 类型 | 说明 |
|---|---|---|
| A1 | 预算指向已删账本 | budgets 行的 ledger_id 在 ledgers 表中已不存在 |
| A2 | 附件行指向已删交易 | transaction_attachments 行的 transaction_id 失主 |
| A3 | tag 关联指向已删交易 | transaction_tags 行的 transaction_id 失主 |
| A4 | tag 关联指向已删标签 | transaction_tags 行的 tag_id 失主 |
| A5 | 交易的账户失主 | tx 的 account_id 或 to_account_id 找不到对应 accounts 行 |
| A6 | 交易的分类失主 | tx 的 category_id 找不到对应 categories 行 |
| A7 | 二级分类失父 | categories 行的 parent_id 找不到父分类 |
| A8 | 预算分类失主 | budgets 行的 category_id 找不到对应分类 |
| A9 | 共享二级分类失父 | shared_ledger_categories 的 parent_sync_id 失主 |
| A10 | tag override 失主交易 | transaction_tag_overrides 行的 tx 已删 |

#### B 类:磁盘文件孤儿

| 编号 | 类型 | 说明 |
|---|---|---|
| B1 | 附件原图无引用 | attachments 目录下的文件,没有 transaction_attachments 行引用 |
| B2 | 分类自定义图标无引用 | category_icons 目录下的文件,没有 categories.custom_icon_path 引用 |
| B3 | 共享分类图标缓存无引用 | shared_ledger 共享分类的图标 sha256 缓存,无引用 |

#### C 类:同步状态孤儿

| 编号 | 类型 | 说明 |
|---|---|---|
| C1 | sync_queue 失主实体 | local_changes 行对应的主实体已被删 |

### 常见场景

- **大量 A2/A3**:批量删过交易后,关联表行没级联清干净
- **B1 占了几百 MB**:附件原图删了 tx 但文件留在沙盒里(早期版本未自动清)
- **A9 + B3**:用过共享账本但被踢/退出了,镜像数据还在本地

### 注意事项

:::warning 清理前先备份
执行清理前建议先**导出 CSV / 触发一次云同步**。清理操作**不可撤销**,且不会上传到云端备份。
:::

:::tip 失败处理
极少数情况(如附件文件被其他应用占用)会失败,失败列表会提示具体原因,可重新扫描后再试。
:::

## Web 端:管理员数据清理

### 入口

右上角头像下拉菜单 → 「管理员 · 数据清理」(仅管理员可见)

直链:`https://你的部署域名/app/admin/data-cleanup`

:::warning 仅管理员可访问
普通用户在头像菜单里看不到这个入口。如果你是自托管管理员,需要先把账号 `is_admin` 设为 `true`,详见 [BeeCount Cloud 部署文档](../cloud-sync/beecount-cloud)。
:::

### 适用范围

清理**服务端跨所有用户的孤儿数据**:Postgres / SQLite 数据库行 + `/data/attachments` 目录里的附件 + sync_changes 异常记录。

与 App 端工具**完全独立** — Web 端清的是服务端,App 端清的是设备本地,两者不冲突也不互相替代。

### 工作流

跟 App 端一致:扫描 → 三组列表 → 勾选 → 单删 / 批量删 → 二次确认 → 自动重扫。

### Web 端检测项清单

#### A 类:数据库引用断链

| 编号 | 类型 | 说明 |
|---|---|---|
| A1 | 交易分类失主 | tx_missing_category — read_tx_projection 行的 category 已删 |
| A2 | 交易账户失主 | tx_missing_account |
| A3 | 交易源账户失主(转账场景) | tx_missing_from_account |
| A4 | 交易目标账户失主(转账场景) | tx_missing_to_account |
| A5 | 预算分类失主 | budget_missing_category |
| A6 | sync_changes 失主实体 | sync_change 行的主实体已删,丢弃后续 LWW 影响 |

#### B 类:附件 / 文件

| 编号 | 类型 | 说明 |
|---|---|---|
| B1 | 附件 DB 行无引用 | AttachmentFile 行没被任何 tx / category icon 引用 |
| B2 | 附件文件丢失 | AttachmentFile.storage_path 指向的文件在磁盘上找不到 |
| B3 | 磁盘文件无 DB 行 | `/data/attachments` 下文件存在,但 AttachmentFile 表里无对应行(自动跳过 `profile-avatars/`) |
| B4 | 交易引用断链 | tx 的 attachments_json 里的 fileId 在 AttachmentFile 表中不存在 |

### 注意事项

:::warning 操作影响所有用户
Web 端清理操作**作用于全部用户的数据**。删除 sync_changes 行不会逆向给客户端,等同于直接放弃了一次 LWW 写入;删除 storage 文件后,任何客户端再请求该附件都会 404。
:::

:::tip 建议先备份
管理员清理前建议先执行一次 [数据备份](../cloud-sync/beecount-cloud#数据备份)(整个 `data/` 目录 rsync,或 `sqlite3 .backup` / `pg_dump`)。
:::

### 头像目录保护

工具会自动跳过 `profile-avatars/` 目录,不会把用户头像误识别为"无 DB 行的孤儿文件"。这是 1.3.1 起的修复 — 之前老版本可能把头像清掉,如果还在跑老版本请尽快升级。

## 设计原则

两端工具都遵循以下原则:

- **手动触发**:不自动跑、不后台静默清理。所有删除都是用户主动操作。
- **完全可见**:每条孤儿数据都有标题 + 副标题描述,用户清楚自己在删什么。
- **分组 + 勾选**:支持单条 / 分组全选,精细控制删除范围。
- **二次确认**:点「清理」后弹确认弹窗,告知操作不可撤销。
- **失败容错**:批量删除时单条失败不影响其他,失败列表展示具体原因。
- **空间统计**:文件类孤儿显示大小,帮助用户判断"值不值得清"。

## 何时该用

定期(比如每季度)进入一次看看有没有孤儿数据;或者在以下场景:

- 应用占用空间显著上升,但实际数据没多多少
- 大批量删过交易 / 账本 / 分类后
- 共享账本退出后想清干净本地镜像
- 自托管管理员发现 storage 目录莫名变大
- 升级后某次同步报奇怪的引用错误

## 隐私说明

- App 端工具完全离线运行,扫描结果不上传任何地方。
- Web 端工具运行在你自己的 BeeCount Cloud 部署上,数据不出你的服务器。
- 蜜蜂团队不会通过工具收集任何用户数据,这两个工具都是纯本地 / 本地化运算。
