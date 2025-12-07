---
sidebar_position: 100
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

目前主要支持人民币，多币种功能在规划中。

### Q: 支持记录投资收益吗？

可以通过创建「投资」分类和「投资账户」来记录，但暂不支持自动计算收益率等功能。

### Q: 可以多人共享账本吗？

目前不支持多人实时协作，但可以通过共享云同步配置实现简单的数据共享。

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
