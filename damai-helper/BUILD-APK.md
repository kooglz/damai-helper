# 📱 在线编译 Android APK 指南

## 方法：使用 GitHub Actions 自动编译

### 步骤 1️⃣：创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名：`damai-helper`（或你喜欢的名字）
3. 设为 **Public** 或 **Private** 都可以
4. 点击「Create repository」

### 步骤 2️⃣：上传代码到 GitHub

```bash
# 进入项目目录
cd /Users/konglingzheng/.openclaw/workspace/damai-helper

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 大麦抢票助手 Android 应用"

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/damai-helper.git

# 推送
git push -u origin main
```

### 步骤 3️⃣：触发自动编译

推送代码后，GitHub Actions 会自动开始编译：

1. 打开你的 GitHub 仓库页面
2. 点击 **「Actions」** 标签
3. 看到 「Build Android APK」工作流正在运行
4. 等待约 5-10 分钟

### 步骤 4️⃣：下载 APK

编译完成后：

1. 在 GitHub Actions 页面点击最近的运行记录
2. 滚动到页面底部「Artifacts」区域
3. 点击 **`app-debug`** 下载 APK 文件
4. 解压后得到 `app-debug.apk`

### 步骤 5️⃣：安装到手机

**方法 A：通过数据线**
```bash
# 手机开启 USB 调试后
adb install app-debug.apk
```

**方法 B：直接传输**
1. 将 APK 文件发送到手机（微信文件传输助手、QQ 等）
2. 在手机上点击 APK 文件安装
3. 允许「未知来源应用」安装

---

## 手动触发编译（推荐）

如果需要重新编译（比如修改了配置）：

1. 打开 GitHub 仓库
2. 点击 **Actions** → **Build Android APK**
3. 点击右侧 **「Run workflow」** 按钮
4. 选择分支（main）
5. 点击「Run workflow」

---

## 编译产物

编译成功后会生成：
- **APK 文件**: `app/build/outputs/apk/debug/app-debug.apk`
- **大小**: 约 5-10 MB
- **签名**: Debug 签名（测试用）

---

## 注意事项

⚠️ **首次编译较慢** - GitHub 需要下载 Android SDK 和依赖（约 5-10 分钟）

⚠️ **后续编译更快** - 使用 Gradle 缓存，约 2-3 分钟

⚠️ **Debug 版本** - 当前配置生成 Debug 版 APK，适合测试使用

⚠️ **发布版本** - 如需正式版，需要配置签名证书

---

## 故障排查

### 编译失败

查看 GitHub Actions 日志：
1. Actions → 点击失败的运行记录
2. 展开 `Build Debug APK` 步骤
3. 查看错误信息

### 常见问题

**错误：SDK not found**
- GitHub Actions 会自动安装，无需担心

**错误：Gradle build failed**
- 检查 `build.gradle` 配置
- 查看具体错误日志

**错误：Kotlin version mismatch**
- 确保 `build.gradle` 中 Kotlin 版本一致

---

## 下一步

编译完成后：
1. 安装 APK 到手机
2. 打开应用，授予通知权限
3. 点击「开始抢票」，开启无障碍权限
4. 配置开票时间和价位
5. 等待开售自动抢票

**祝你好运！🎫**
