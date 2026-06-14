import os
import requests
import time
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://mrwotas.github.io"   # ваш сайт

AFFILIATE_LINKS = {
    "рюкзак": "https://alipromo.com/...",      # ← вставьте свои партнёрские ссылки
    "наушники": "https://admitad.com/g/...",
    "по умолчанию": "https://admitad.com/..."
}
# -------------------------------

def generate_article(keyword):
        print("🔑 Ключ OpenRouter:", OPENROUTER_API_KEY[:10] + "..." if OPENROUTER_API_KEY else "НЕ ЗАГРУЖЕН")
    link = AFFILIATE_LINKS.get(keyword.split()[0].lower(), AFFILIATE_LINKS["по умолчанию"])
    prompt = f"""Ты полезный блогер. Напиши статью на тему "{keyword}" длиной 600–800 слов.
Структура: заголовок H1, подзаголовки H2, списки. В середине или в конце органично вставь рекомендацию товара со ссылкой {link}.
Оформи в Markdown: '# Заголовок'. После текста ничего не пиши."""

    # Список бесплатных моделей OpenRouter (актуален на июнь 2026)
    # Первая — самая стабильная и рекомендованная
    models = [
        "google/gemini-2.0-flash-thinking:free",  # Gemini 2.0 Flash (работает через OpenRouter без VPN)
        "nousresearch/hermes-3-llama-3.1-405b:free",  # запасная мощная
        "mistralai/mistral-nemo:free"               # если появится
    ]

    for model in models:
        print(f"📡 Пробую модель: {model}")
        for attempt in range(3):
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "Ты всегда отвечаешь на русском языке."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            data = response.json()
            print("📦 Ответ:", data)

            if "choices" in data:
                return data["choices"][0]["message"]["content"]

            error_code = data.get("error", {}).get("code")
            if error_code == 429:
                retry_after = data["error"]["metadata"]["retry_after_seconds"]
                print(f"⏳ Модель {model} ограничена. Жду {retry_after} сек (попытка {attempt+1}/3)")
                time.sleep(retry_after + 1)
                continue
            else:
                # 404, 401 и др. – переходим к следующей модели
                print(f"⚠️ Модель {model} недоступна: {data['error']['message']}")
                break  # выходим из попыток для этой модели

    raise Exception("❌ Все бесплатные модели временно недоступны. Попробуйте позже.")

def save_article(text, keyword):
    os.makedirs("_posts", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")[:40]
    filename = f"_posts/{date_str}-{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"{keyword}\"\ndate: {datetime.now().isoformat()}\ncategories: blog\n---\n")
        f.write(text)
    print(f"✅ Статья сохранена: {filename}")

# ... (функции для соцсетей оставьте как раньше)

if __name__ == "__main__":
    keywords = [
        "Как выбрать рюкзак для школы",
        "Топ бюджетных наушников 2026",
        # ... весь ваш список тем
    ]

    kw = keywords[datetime.now().hour % len(keywords)]
    print(f"📝 Генерирую: {kw}")
    article = generate_article(kw)
    save_article(article, kw)
    # ... постинг в соцсети
    print("🎉 Готово! Робот отработал.")
