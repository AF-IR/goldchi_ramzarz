# 🤖 Nobitex → Bale Crypto Price Bot (USD)

ربات خودکار ارسال قیمت دلاری ارزهای دیجیتال از **نوبیتکس** به کانال **بله**.

## ✨ ویژگی‌ها
- قیمت‌ها به **دلار (USDT)** از API عمومی نوبیتکس
- نمایش درصد تغییر روزانه با ایموجی
- **هشتگ** برای هر ارز (فارسی و انگلیسی)
- واترمارک `@GoldChi`
- اجرای خودکار روزانه با GitHub Actions

## 🚀 راه‌اندازی

### ۱. توکن بله
در بله به [@BotFather](https://ble.ir/BotFather) مراجعه و دستور `/newbot` را ارسال کنید. ربات را ادمین کانال کنید.

### ۲. تنظیم Secrets
در گیت‌هاب → **Settings → Secrets and variables → Actions**:
- `BALE_BOT_TOKEN`
- `BALE_CHANNEL_ID`

### ۳. اجرا
پس از Push، هر روز ساعت ۹ صبح اجرا می‌شود. برای تست دستی از تب Actions → Run workflow استفاده کنید.

## 🛠️ اجرای محلی
```bash
cp .env.example .env
pip install -r requirements.txt
python main.py
