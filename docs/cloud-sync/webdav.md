---
sidebar_position: 5
---

# WebDAV 同步

通过 WebDAV 将记账数据保存在自己的网盘或 NAS 中，支持坚果云、群晖、Nextcloud 等服务。

:::tip 遇到 404，先检查地址和路径
「服务器地址」要填完整的 **WebDAV 接口地址**；「远程路径」填这个地址下面用于存放数据的文件夹。网盘首页、分享链接、NAS 管理后台地址都不能直接当作 WebDAV 地址。

可以先对照下方的[平台示例](#provider-examples)，再按 [404 排查步骤](#troubleshooting-404)检查。
:::

## 服务器地址和远程路径怎么填 {#address-and-path}

进入「我的」→「云服务」，选择「自定义 WebDAV」，填写以下四项：

手机阅读时，表格可左右滑动查看完整内容。

| 配置项 | 填写内容 | 示例（坚果云） |
| --- | --- | --- |
| WebDAV 服务器地址 | 服务商提供的完整接口地址，包括 `https://`、端口（如有）和接口路径 | `https://dav.jianguoyun.com/dav/` |
| 用户名 | 有 WebDAV 访问权限的账号 | 坚果云注册邮箱 |
| 密码 | 服务商要求的密码或应用专用密码 | 坚果云生成的应用密码 |
| 远程路径 | 相对于上述接口地址的存储目录，以 `/` 开头 | `/BeeCount` |

**服务器地址和远程路径会拼接成最终的存储目录。** 例如：

```text
服务器地址：https://dav.jianguoyun.com/dav/
远程路径：  /BeeCount
存储目录：  https://dav.jianguoyun.com/dav/BeeCount/
```

- `/` 表示直接使用服务器地址对应的目录；`/BeeCount` 表示使用它下面的 `BeeCount` 文件夹。
- 服务器地址已包含 `/dav/` 时，远程路径不要再填 `/dav/BeeCount`，否则会变成 `/dav/dav/BeeCount/`。
- 如果服务器地址已经以 `/BeeCount/` 结尾，远程路径填 `/` 即可，避免重复一层 `BeeCount`。
- 远程路径只填文件夹路径，不填完整网址、本机路径（如 `C:\Backup`）或 NAS 内部路径（如 `/volume1/Backup`）。目录名大小写应与服务器一致。

:::note 已经同步过的用户
当前应用的远程路径默认是 `/`，`/BeeCount` 是本文为新配置建议的独立目录，应用不会自动追加这一层。已经成功同步的设备请沿用原来的地址和路径；更改目录不会自动搬迁旧数据，可能导致看不到原有云端账本。
:::

## 支持的服务与填写示例 {#provider-examples}

下面是一组配套的「服务器地址 + 远程路径」示例。除坚果云的固定接口地址外，请替换示例域名、端口、用户名和目录名；自建服务以管理员实际提供的 WebDAV 地址为准。

| 平台 | WebDAV 服务器地址示例 | 远程路径示例 |
| --- | --- | --- |
| 坚果云 | `https://dav.jianguoyun.com/dav/` | `/BeeCount` |
| 群晖 Synology | `https://nas.example.com:5006/Backup/` | `/BeeCount` |
| Nextcloud | `https://cloud.example.com/remote.php/dav/files/alice/` | `/BeeCount` |
| ownCloud Server（传统版） | `https://cloud.example.com/remote.php/webdav/` | `/BeeCount` |
| 威联通 QNAP | `https://nas.example.com:PORT/Backup/` | `/BeeCount` |
| OpenList / AList | `https://files.example.com/dav/` | `/Storage/BeeCount` |

### 坚果云配置

1. 注册并登录[坚果云网页版](https://www.jianguoyun.com/)。
2. 进入「账户信息」→「安全选项」→「第三方应用管理」，添加应用密码，例如命名为「蜜蜂记账」。
3. 在蜜蜂记账中填写表格中的地址和路径，用户名填写坚果云注册邮箱，密码填写刚生成的**应用密码**。

注意保留服务器地址末尾的 `/dav/`，不要使用坚果云首页地址或账号登录密码。详见[坚果云官方授权说明](https://help.jianguoyun.com/?p=2064)。

### 群晖 NAS 配置

1. 在 DSM「套件中心」安装并打开 **WebDAV Server**，启用 HTTPS，确认实际端口（默认 `5006`）。
2. 创建或选择已有共享文件夹，例如 `Backup`，为使用的 NAS 账号授予该文件夹的读写权限及 WebDAV 服务访问权限。
3. 按表格填写：服务器地址包含共享文件夹名，用户名和密码填写 NAS 账号信息。示例最终存储目录为 `https://nas.example.com:5006/Backup/BeeCount/`。

不要填写 DSM 管理后台的 `5000` / `5001` 端口或 QuickConnect 网页链接。如果只在局域网启用了 HTTP，默认 WebDAV 端口是 `5005`，地址应相应使用 `http://`；以实际启用的协议和端口为准。远程访问时，手机需要能访问该 WebDAV 地址。

详见[群晖 WebDAV Server 官方说明](https://kb.synology.com/en-us/DSM/help/WebDAVServer/webdav_server?version=7)。

### Nextcloud 配置

在 Nextcloud 网页端的「文件」→「文件设置」中复制 **WebDAV 地址**，完整粘贴到服务器地址栏。表格中的 `alice` 需要替换为实际用户 ID，不一定是显示昵称。

如果 Nextcloud 安装在子目录下，需要保留子目录。例如网页地址为 `https://example.com/nextcloud/`，接口地址通常是 `https://example.com/nextcloud/remote.php/dav/files/alice/`。

用户名使用该账号的登录名，密码建议在「个人设置」→「安全」中生成应用密码；开启双重验证时使用应用密码。以页面复制的地址和生成的凭据为准，避免只填写域名或漏掉用户目录。详见 [Nextcloud 官方 WebDAV 说明](https://docs.nextcloud.com/server/stable/user_manual/en/files/access_webdav.html)。

### ownCloud 配置

表格示例适用于传统 **ownCloud Server**，用户名和密码使用具有文件读写权限的 ownCloud 账号凭据；如果实例要求应用密码，按管理员要求生成并填写。

如果安装在 `/owncloud/` 子目录下，服务器地址需要包含该前缀，例如 `https://example.com/owncloud/remote.php/webdav/`。使用 Infinite Scale 或托管版本时，向管理员获取实际 WebDAV 地址，不要直接套用传统版路径。详见 [ownCloud Server 官方 WebDAV 说明](https://doc.owncloud.com/server/10.15/classic_ui/files/access_webdav.html)。

### 威联通 QNAP 配置

先在 NAS 中启用 WebDAV，并为账号设置目标共享文件夹的读写权限。将表格中的 `PORT` 替换为配置的 HTTPS WebDAV 端口，`Backup` 替换为已有共享文件夹名；用户名和密码使用获授权的 NAS 账号。

请从 WebDAV 设置中确认协议和端口，不要套用群晖的 `5006`，也不要直接复制 QTS 管理后台地址。详见 [QNAP 官方连接说明](https://www.qnap.com/en-uk/how-to/faq/article/connecting-to-webdav-shared-folders-on-a-qnap-nas-in-windows-10)。

### OpenList / AList 配置

- 服务器地址通常是网页服务地址加 `/dav/`，用户名和密码使用 **OpenList / AList 自身的账号**。
- 将表格中的 `Storage` 替换为该用户可见的实际网盘挂载目录。若账号的根目录已经指向目标网盘，远程路径可填 `/BeeCount`，无需再重复挂载目录名。
- 在用户权限中开启 WebDAV 读取、WebDAV 管理，以及创建目录、上传、删除等所需权限；底层网盘也必须支持相应的写入操作。
- 网盘挂载目录要先配置好。建议先在网页端进入目标目录，确认可以创建文件夹和上传文件。

详见 [OpenList 官方 WebDAV 说明](https://doc.oplist.org/guide/advanced/webdav)和 [AList 官方 WebDAV 说明](https://alistgo.com/guide/webdav)。

## 保存后如何确认配置成功 {#verify-configuration}

1. 保存配置，在云服务页面启用 WebDAV，并点击「测试连接」。
2. 在账本的同步功能中手动上传一次，再到网盘或 NAS 中确认目标目录出现了数据。
3. 其他设备使用同一账号，并填写指向同一存储目录的地址和路径。

:::info 测试连接成功，但上传仍然失败？
「测试连接」只检查服务器入口是否响应，并不验证远程路径是否存在或是否可写。如果测试通过，但同步时报错，请继续检查目标目录、账号写入权限及反向代理配置。
:::

## 404 和其他常见问题 {#troubleshooting}

### 提示 404 / 路径不存在 {#troubleshooting-404}

404 通常表示请求到达了服务器，但对应的接口或目录没有找到。请按顺序检查：

1. **确认是 WebDAV 接口地址。** 对照平台示例，检查坚果云的 `/dav/`、Nextcloud 的 `/remote.php/dav/files/用户ID/` 等是否完整。网页登录地址和文件分享链接不能替代接口地址。
2. **把服务器地址和远程路径拼起来检查。** 查看是否出现 `/dav/dav/`、`/BeeCount/BeeCount/`，或漏掉安装子目录、共享文件夹名、网盘挂载目录。注意目录名大小写。
3. **确认父目录已经存在。** NAS 共享文件夹、OpenList / AList 挂载目录需先在服务端配置。应用会尝试创建远程目录，但不能替你创建共享文件夹或挂载网盘；多级路径建议先在网页端建好。
4. **区分报错阶段。** 点「测试连接」就返回 404，优先核对服务器地址和端口；测试成功但上传、下载时报 404，继续核对远程路径、文件是否存在和账号权限。
5. **自建服务检查反向代理。** 确认完整的 WebDAV 路径转发到了正确服务，且没有被改写为登录页或普通网页。可用其他 WebDAV 客户端以同一账号连接并读写同一目录，帮助定位问题。

仅用浏览器打开网址无法确认 WebDAV 是否可用：浏览器的网页请求与同步时的目录读取、文件上传请求不同。

### 其他错误怎么排查

| 提示或现象 | 优先检查 |
| --- | --- |
| `401` / 认证失败 | 用户名、密码是否正确；坚果云是否使用应用密码；开启双重验证后是否需要应用密码 |
| `403` / 拒绝访问 | 账号是否有 WebDAV 和目标目录的读写权限；OpenList / AList 是否开放管理及上传权限 |
| `405` / 方法不允许 | 是否连到了普通网页或错误端口；服务端或反向代理是否允许 `OPTIONS`、`PROPFIND`、`MKCOL`、`PUT`、`GET`、`DELETE` 等 WebDAV 请求 |
| `409` / 目录冲突 | 父目录是否存在；先在网页端创建完整目录，再重试 |
| 连接超时 / 无法连接 | 手机是否能访问 NAS 所在网络；域名、端口、防火墙和端口转发是否正确 |
| 证书错误 / SSL 错误 | HTTPS 证书是否有效，是否与访问域名匹配 |
| 连接成功但找不到旧账本 | 是否与原设备使用同一账号和存储目录；是否改过远程路径或多填了一层文件夹 |

## 同步目录

同步数据保存在「服务器地址 + 远程路径」指向的目录下，应用还会在其中管理自己的数据子目录和文件。目录并不固定为 `/BeeCount/`，也不等同于 NAS 的磁盘根目录。

例如，坚果云使用本文示例时存放在 `dav/BeeCount/` 下，群晖示例则存放在共享文件夹 `Backup` 的 `BeeCount` 子目录下。已经同步的设备应保持配置一致，不要手动改名或移动应用管理的文件。
