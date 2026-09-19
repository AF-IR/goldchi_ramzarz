"""
ربات ارسال قیمت روزانه ارزهای دیجیتال از نوبیتکس به کانال بله
- قیمت‌ها به دلار (USDT)
- دارای هشتگ
- واترمارک @GoldChi
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== تنظیمات ====================
BALE_BOT_TOKEN = os.getenv("BALE_BOT_TOKEN")
BALE_CHANNEL_ID = os.getenv("BALE_CHANNEL_ID")
WATERMARK = "@GoldChi"

# ارزهای محبوب (نمادهای مبدا در نوبیتکس)
POPULAR_COINS = [
    "BTC", "ETH", "BNB", "SOL", "XRP",
    "ADA", "DOGE", "TON", "TRX", "DOT"
]

# هشتگ‌های مرتبط با هر ارز
COIN_HASHTAGS = {
    "BTC": "#Bitcoin #بیت_کوین",
    "ETH": "#Ethereum #اتریوم",
    "BNB": "#BNB #بایننس_کوین",
    "SOL": "#Solana #سولانا",
    "XRP": "#XRP #ریپل",
    "ADA": "#Cardano #کاردانو",
    "DOGE": "#Dogecoin #دوج_کوین",
    "TON": "#Toncoin #تون",
    "TRX": "#Tron #ترون",
    "DOT": "#Polkadot #پولکادات",
}


# ==================== دریافت داده از نوبیتکس ====================
def fetch_nobitex_stats_usd():
    """
    دریافت آمار بازار از API عمومی نوبیتکس با ارز مقصد USDT (دلار)
    """
    url = "https://apiv2.nobitex.ir/market/stats"
    headers = {
        "Accept": "application/json",
        "User-Agent": "TraderBot/CryptoPriceBot-2.0.0"
    }
    params = {
        "srcCurrency": ",".join([c.lower() for c in POPULAR_COINS]),
        "dstCurrency": "usdt"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            raise Exception(f"خطای API: {data.get('message', 'نامشخص')}")

        return data.get("stats", {})
    except requests.exceptions.RequestException as e:
        print(f"[خطا] عدم اتصال به نوبیتکس: {e}")
        return None


# ==================== فرمت‌دهی پیام ====================
def format_message(stats):
    """ساخت متن پیام با قیمت دلاری و هشتگ‌ها"""
    now = datetime.now().strftime("%Y/%m/%d - %H:%M")
    lines = [
        "📊 **گزارش روزانه بازار رمزارزها (دلاری)**",
        f"🕐 {now}",
        "━━━━━━━━━━━━━━━━━━━━",
    ]

    for coin_symbol in POPULAR_COINS:
        key = f"{coin_symbol.lower()}usdt"
        if key not in stats:
            continue

        coin = stats[key]
        price_usd = float(coin.get("latest", 0))
        change = float(coin.get("dayChange", 0))
        coin_name = coin.get("title", coin_symbol)

        if change > 0:
            emoji = "🟢"
            sign = "+"
        elif change < 0:
            emoji = "🔴"
            sign = ""
        else:
            emoji = "⚪"
            sign = ""

        hashtags = COIN_HASHTAGS.get(coin_symbol, f"#{coin_symbol}")

        lines.append(f"{emoji} **{coin_name}** ({coin_symbol})")
        lines.append(f"   💵 ${price_usd:,.2f}  |  {sign}{change:.2f}%")
        lines.append(f"   {hashtags}")

    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("🔗 منبع: نوبیتکس")
    lines.append(WATERMARK)

    return "\n".join(lines)


# ==================== ارسال به بله ====================
def send_to_bale(message):
    """ارسال پیام به کانال بله از طریق API سفیر"""
    url = "https://safir.bale.ai/api/v3/send_message"
    headers = {
        "api-access-key": BALE_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "chat_id": BALE_CHANNEL_ID,
        "text": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("ok"):
            print("[✓] پیام با موفقیت ارسال شد.")
            return True
        else:
            print(f"[✗] خطای ارسال: {result}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[✗] عدم اتصال به بله: {e}")
        return False


# ==================== اجرای اصلی ====================
def main():
    print("🚀 شروع دریافت قیمت‌های دلاری...")

    stats = fetch_nobitex_stats_usd()
    if not stats:
        print("❌ دریافت داده ناموفق بود.")
        return

    message = format_message(stats)
    print("\n--- محتوای پیام ---")
    print(message)
    print("-------------------\n")

    send_to_bale(message)


if __name__ == "__main__":
    main()
