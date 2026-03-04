# 🎫 大麦抢票助手 - 配置文件

## 观演人信息 ✅ 已配置

| 序号 | 姓名 | 身份证号 |
|------|------|----------|
| A | 孔令征 | 320104198504011216 |
| B | 叶波 | 320105198701191427 |

## 演出信息

| 项目 | 值 |
|------|-----|
| 演出 | 孙燕姿《就在日落以后》巡回演唱会 - 苏州 |
| 日期 | 2026 年 4 月 12 日 |
| 场馆 | 苏州奥林匹克体育中心体育场 |
| **开票时间** | **2026-03-06 14:00:00** |
| 目标价位 | ¥680 |
| 张数 | 2 张 |

---

## 各平台配置状态

### ✅ Android 应用
- 观演人信息：已硬编码到 `AccessibilityService.kt`
- 默认配置：`MainActivity.kt` 中的 `DEFAULT_ATTENDEES`
- 开票时间：`2026-03-06 14:00:00`

### ✅ 浏览器油猴脚本
- 文件：`damai-assistant.user.js`
- 配置位置：`CONFIG.attendees`
- 开票时间：`2026-03-06T14:00:00+08:00`

### ✅ Python 自动抢票
- 文件：`auto_buy.py`
- 配置位置：`CONFIG['attendees']` 和 `CONFIG['id_cards']`
- 开票时间：`2026-03-06 14:00:00`

### ✅ 桌面提醒助手
- 文件：`remind.py`
- 配置位置：`CONFIG['attendees']`
- 开票时间：`2026-03-06 14:00:00`

---

## Android 应用构建步骤

### 方法 1：Android Studio（推荐）

1. 打开 Android Studio
2. `File` → `Open` → 选择 `damai-helper/android-app` 目录
3. 等待 Gradle 同步完成
4. `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
5. APK 输出位置：`app/build/outputs/apk/debug/app-debug.apk`

### 方法 2：命令行构建

```bash
cd /Users/konglingzheng/.openclaw/workspace/damai-helper/android-app

# 首次构建需要下载 Gradle
./gradlew assembleDebug

# APK 位置
ls -la app/build/outputs/apk/debug/app-debug.apk
```

### 安装到手机

```bash
# 通过 ADB 安装
adb install app/build/outputs/apk/debug/app-debug.apk

# 或通过文件传输到手机后直接安装
```

---

## 使用前配置

### Android 应用
1. 安装 APK 后打开应用
2. 点击「⚙️ 配置」确认开票时间和价位
3. 点击「开始抢票」前需要开启**无障碍权限**
4. 按提示前往设置 → 无障碍 → 找到「大麦抢票助手」并开启

### 浏览器脚本
1. 安装 Tampermonkey 扩展
2. 复制 `damai-assistant.user.js` 内容到 Tampermonkey
3. 打开大麦演出详情页
4. 看到倒计时浮窗即表示成功

### 桌面提醒
```bash
cd /Users/konglingzheng/.openclaw/workspace/damai-helper
python3 remind.py
```

---

## 注意事项

⚠️ **开票时间待确认** - 当前配置为 `2026-03-06 14:00:00`，请根据实际开票时间修改

⚠️ **无障碍权限** - Android 应用必须开启无障碍权限才能自动点击

⚠️ **测试** - 建议先用测试演出或预售场次测试功能

---

*最后更新：2026-03-04 12:55*
