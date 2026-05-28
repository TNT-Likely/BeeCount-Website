---
sidebar_position: 102
description: 蜜蜂记账版本更新历史与功能迭代日志。3.0 新增 BeeCount Cloud 自建云同步、Web 端访问等核心特性。
keywords: [蜜蜂记账更新日志, 蜜蜂记账版本, BeeCount changelog]
---

# 更新日志

查看蜜蜂记账的版本更新历史。

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

所有版本的详细更新记录、下载链接都可以在 GitHub Releases 页面查看。

## Cloud 1.3.8 亮点

- 🐛 **净资产计算修复**:web 端"资产"页之前对所有账户余额取绝对值再相加,透支的资产账户(如 cash / bank_card balance<0)会被翻成正数算进总资产;生产数据 5 个账户实际 8.95 万 UI 错显 16.7 万。改为带符号累加,跟 mobile 端 `getNetWorthBreakdown` 口径完全一致
- 🎯 **首页 Top 卡片按当前账本统计**:之前 OverviewPage 拉 workspace accounts/tags 不带 ledgerId,聚合的 tx_count / balance / expense_total 是用户所有账本汇总,跟首页其它当前账本视角错位
- 🔀 **详情弹窗加账本作用域切换**:账户 / 分类 / 标签三个详情弹窗顶部加"全部账本 / 当前账本"segmented toggle。资产/分类/标签一级页面进入默认跨账本,行内显示账本名 chip;首页 Top 卡片 + 跳分类等场景默认当前账本
- 🖱 **首页热门标签 / 活跃账户卡片接入详情弹窗**:之前只能跳搜索结果页,现在点击直接打开对应详情弹窗,跟 mobile 端体验对齐

## Cloud 1.3.7 亮点

- 🧹 **新增 `scripts/compact_sync_changes.sh`**:一次性清理 `sync_changes` 表的历史重复(同 user × entity_type × entity_id 多余行合并到只剩最大 change_id 那条)。长期运行的老实例同步日志会越积越多,执行一次可显著减小数据库体积、加快 fullPull 速度

## Cloud 1.3.6 亮点

- 🤝 **共享账本 Editor 删除 tx 同时清理附件**:之前 Editor 删带附件的交易,服务端只删 tx 记录、附件文件留下变孤儿,跑一次孤儿清理才能扫出来;现在 delete 时直接级联清理,跟 Owner 删 tx 的行为对齐
- 🗜 **实体 delete 自动压缩 `sync_changes`**:同 entity 的历史 update 行在 delete 写入时先合并掉,进一步控制同步日志体积膨胀

## 3.2.3 亮点

- 📅 **日历页直接记账**:选中某天后直接在该日期下记账,不用先切日历日期再去加,日历交互更紧凑;首次进入页面用骨架屏占位,过渡更顺
- 🤖 **AI 一次识别多笔**:图片 / 语音 / 文本三个入口都升级为"一次识别多笔交易",连续记账场景效率明显提升
- 🛡 **修复多设备同步日志膨胀**:并发 fullPush 不再重复推送,sync_changes 表不会因为多端同时唤起而无序膨胀

## 3.2.2 亮点

- 🤖 **修复 AI 自定义提示词失效**:部分入口漏初始化导致始终走默认模板,现在所有路径都吃用户设置的自定义 prompt
- 💬 **AI 识别失败提示更准确**:不再统一报"未配置 AI",具体原因(网络 / API key / 配额 / 模型不支持)单独提示并写入日志,排查更直接
- 📲 **修复 in-app 更新选错 APK 架构**:之前 arm64 真机可能被装上 armv7 包,跑起来严重卡顿,严重影响首次安装体验

## 3.2.1 亮点

- 📦 **Android APK 体积砍 77%**(70.2 MB → 16 MB):删 OCR + 拆 ABI + 删 tflite 死代码;按 ABI 分发(arm64 主包 / armv7 兼容 / x86_64 模拟器 / universal 兜底)
- 🤖 **OCR 改走 AI 视觉**:删 google_mlkit_text_recognition,全面切换 GLM-4V 等 LLM 视觉模型;UI / Android 截图监听 / iOS 自动记账后台路径统一,AI 未配置时有清晰兜底提示
- ⚡ **同步性能大幅提升**:WebDAV / Supabase 从远端拉万条数据从几分钟降到秒级;带标签 CSV 导入万条数据从几十分钟降到秒级
- 🛡 **同步稳定性**:整页 rollback + cursor 应用后才推进、e2e 测试基础设施 32 个测试、UI ↔ SyncEngine 解耦走 SyncEvent stream,首页不再闪烁
- 🎯 **默认账本可选**:欢迎页币种选择下加复选框,可不创建默认账本;首页空账本时胶囊变「+ 新建账本」,点击直接弹创建对话框
- 🧭 **菜单信息架构调整**:预算管理挪到「账本管理 → 长按账本」(每个账本独立预算);应用锁挪到「个性化设置」(冷门功能并入应用偏好);「外观设置」改名「个性化设置」

## 3.2.0 亮点

- 🤝 **共享账本**:支持多人协同记账,Owner 邀请 Editor 加入同一账本,分类/账户/标签 server 端 fan-out 给所有成员
- 🌐 域名切换到 `beejz.com` 系
- 🔧 user-global 资源(自定义分类/账户/标签 + 自定义图标):server 端按 user_id 维度同步,跨账本共享
- 📦 sync_engine 拆分为多 part 文件:realtime / apply / serialization / attachments / resolvers / status
- 🤖 MCP 工具集 + TestFlight 渠道
- 📱 上架合规:iOS 名本地化、去 OpenAI 字样、Google Play 权限剥离(剥离 READ_MEDIA_*)

## 3.0.0 亮点

- 🆕 支持 [**BeeCount Cloud**](./cloud-sync/beecount-cloud) 自建云同步服务
- 🌐 Web 管理端内置于 Docker 镜像,支持 PWA 安装
- 🔄 多设备实时协同:手机 + Web + 平板秒级同步
- 👥 多用户独立:一个服务器可多人使用,数据互相隔离
