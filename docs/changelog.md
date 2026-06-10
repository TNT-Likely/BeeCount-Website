---
sidebar_position: 102
description: 蜜蜂记账版本更新历史与功能迭代日志。3.0 新增 BeeCount Cloud 自建云同步、Web 端访问等核心特性。
keywords: [蜜蜂记账更新日志, 蜜蜂记账版本, BeeCount changelog]
---

# 更新日志

查看蜜蜂记账的版本更新历史。

👉 [GitHub Releases](https://github.com/TNT-Likely/BeeCount/releases)

所有版本的详细更新记录、下载链接都可以在 GitHub Releases 页面查看。

## 3.4.0 亮点

- 📅 **每月起始日**:每个账本可把"本月"设为从任意一天(1-28)开始,发薪日/信用卡账单日党福音;首页、统计、预算、年报、小部件、AI 全链路按记账周期计算,多设备同步。详见[文档](./account/month-start-day.md)。自建云需配套升级 **BeeCount Cloud 1.4.0**(网页端同口径,升级自动修复历史账户统计漏算)
- 🍎 **iOS 27 适配**:快捷指令自动记账不再因未授权通知而中断,不开通知也能正常记账

## 3.3.0 亮点

- 🎨 **皮肤**:首页顶部装饰跟随主题色,内置渐变/场景/几何多款,亮暗通用,多设备同步,配置可导入导出
- ➕ **记账键盘四则运算**:长按/双击切换 + − × ÷,AA 分摊直接在键盘上算
- 👤 **自定义昵称**:「我的」页头像入口编辑昵称,配合时段问候

## 3.2.4 / 3.2.5 要点

- 🤖 AI 记账兼容性:字符串金额、中文时间、推理模型参数自适应,关闭自动标签开关后不再挂标签
- 🗂 分类支持收/支同名;交易列表常驻显示分类名
- 💳 账户与资产管理优化:编辑页重做、信用卡展示对齐(Web 端同步对齐,资产页按币种隔离)
- 🔁 周期账单禁止选择历史开始日期,避免回溯生成脏数据

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
