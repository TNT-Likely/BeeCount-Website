---
sidebar_position: 100
description: 蜜蜂记账常见问题解答 FAQ:数据备份、云同步、自动记账、多端同步、安全隐私等高频问题集中解答。
keywords: [蜜蜂记账常见问题, 记账FAQ, 记账数据备份, 蜜蜂记账帮助]
---

# 常见问题

## 数据相关

### Q: 如何备份数据？

有以下几种方式：

1. **云同步**（推荐）- 开启 iCloud/Supabase/WebDAV/S3 同步
2. **导出 CSV** - 导出交易数据到本地
3. **导出配置** - 导出分类、账户等设置

### Q: 换手机如何迁移数据？

- **iOS → iOS**: 使用 iCloud 同步，新设备登录同一 Apple ID 即可
- **Android → Android**: 使用 Supabase/WebDAV/S3 同步
- **跨平台**: 使用 Supabase/WebDAV/S3 同步，或导出 CSV 后导入

### Q: 数据存储在哪里？

数据默认存储在设备本地。开启云同步后，会同步到你选择的云服务（iCloud/Supabase/WebDAV/S3），蜜蜂记账不收集任何数据。

## 功能相关

### Q: 支持多币种吗？

支持多币种，可在创建账本时选择币种。但同一个账本内只能使用一种币种，不支持同账本多币种混用。

### Q: 支持记录投资收益吗？

可以通过创建「投资」分类和「投资账户」来记录，但暂不支持自动计算收益率等功能。

### Q: 可以多人共享账本吗？

**支持。** 部署 [BeeCount Cloud](./cloud-sync/beecount-cloud) 自建云端后,Owner 可以一键生成邀请码邀请家人 / 朋友加入同一个账本,所有人实时秒级同步,每条交易自动标记"谁记的 / 谁编辑的"。Owner / Editor 双角色权限分明,iOS / Android / Web 三端都能用。详细使用见 [共享账本](./shared-ledger)。

> 仅 BeeCount Cloud 后端支持共享账本(其它同步方案如 iCloud / WebDAV / S3 是单人多设备场景,数据不互通)。

## 同步相关

### Q: 同步不生效怎么办？

1. 检查网络连接
2. 检查云服务配置是否正确
3. 尝试手动触发同步
4. 查看同步日志排查问题

### Q: 可以同时使用多个云同步吗？

目前只能选择一个云同步方式。

## 其他问题

### Q: App Store 中国区下载不了？

中国区 App Store 上架需要备案，正在办理中。目前可以使用 TestFlight 安装。

### Q: 有 Android 版本吗？

有的，可以在 [GitHub Release](https://github.com/TNT-Likely/BeeCount/releases) 下载 APK 安装。

### Q: 是免费的吗？

是的，完全免费，没有广告，没有会员，没有任何隐藏收费。

---

还有其他问题？欢迎 [提交 Issue](https://github.com/TNT-Likely/BeeCount/issues) 反馈。
