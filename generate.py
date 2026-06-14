import os
import requests
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://MrWotas.github.io"   # ← замени твой_логин

AFFILIATE_LINKS = {
    "рюкзак": "https://alipromo.com/...",      # ← вставь свои ссылки
    "наушники": "https://admitad.com/g/...",
    "по умолчанию": "https://admitad.com/..."
}
# -------------------------------



def save_article(text, keyword):
    os.makedirs("_posts", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")[:40]
    filename = f"_posts/{date_str}-{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"{keyword}\"\ndate: {datetime.now().isoformat()}\ncategories: blog\n---\n")
        f.write(text)
    print(f"✅ Статья сохранена: {filename}")

def post_to_twitter(title, url, twitter_creds):
    """Публикует твит с заголовком и ссылкой"""
    import tweepy
    client = tweepy.Client(
        consumer_key=twitter_creds["api_key"],
        consumer_secret=twitter_creds["api_secret"],
        access_token=twitter_creds["access_token"],
        access_token_secret=twitter_creds["access_secret"]
    )
    tweet_text = f"{title}\n\nЧитать: {url}\n#полезное #совет"
    client.create_tweet(text=tweet_text)
    print("🐦 Твит опубликован")
    
def generate_article(keyword, max_retries=3):
    link = AFFILIATE_LINKS.get(keyword.split()[0].lower(), AFFILIATE_LINKS["по умолчанию"])
    prompt = f"""Ты полезный блогер. Напиши статью на тему "{keyword}" длиной 600–800 слов.
Структура: заголовок H1, подзаголовки H2, списки. В середине или в конце органично вставь рекомендацию товара со ссылкой {link}.
Оформи в Markdown: '# Заголовок'. После текста ничего не пиши."""

    # Список резервных бесплатных моделей (обновлён на июнь 2026)
    models = [
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-nemo:free",
        "nousresearch/hermes-3-llama-3.1-405b:free",
        "google/gemma-2-9b-it:free",
        "cohere/command-r:free"
    ]

    for model in models:
        print(f"📡 Пробую модель: {model}...")
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

        # Ошибка 429 – ждём и пробуем эту же модель
        if data.get("error", {}).get("code") == 429:
            retry_after = data["error"]["metadata"]["retry_after_seconds"]
            for attempt in range(max_retries):
                print(f"⏳ Слишком много запросов. Жду {retry_after} секунд... (попытка {attempt+1}/{max_retries})")
                import time
                time.sleep(retry_after + 1)
                response = requests.post(...)  # повторный запрос с той же моделью
                data = response.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
        # Другие ошибки (404 и т.п.) – переходим к следующей модели
        else:
            print(f"⚠️ Модель {model} недоступна: {data.get('error', {}).get('message')}")

    raise Exception("❌ Все резервные модели недоступны.")

def post_to_telegram(title, url, bot_token, chat_id):
    """Отправляет сообщение в Telegram-канал"""
    message = f"🔥 *{title}*\n\n{url}"
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    )
    print("📬 Сообщение в Telegram отправлено")


def post_to_pinterest(title, url, image_url, board_id, access_token):
    """Создаёт пин с картинкой"""
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "board_id": board_id,
        "title": title,
        "description": title,
        "source_url": url,
        "media_source": {"source_type": "image_url", "url": image_url}
    }
    r = requests.post("https://api.pinterest.com/v5/pins", json=data, headers=headers)
    if r.status_code == 201:
        print("📌 Пин создан")
    else:
        print(f"⚠️ Ошибка Pinterest: {r.text}")
if __name__ == "__main__":
    keywords = [
        "Как выбрать рюкзак для школы",
        "Топ бюджетных наушников 2026",
        "Лучшие увлажнители воздуха для дома",
        "Рейтинг недорогих фитнес-браслетов",
        "Как выбрать термокружку для школы",
        "Лучшие бюджетные смарт-часы",
        "Недорогие рюкзаки для путешествий",
        "Топ-5 беспроводных колонок до 1000 рублей",
        "Как выбрать пауэрбанк для телефона",
        "Рейтинг настольных ламп для учёбы",
        "Лучшие бюджетные электросамокаты для города",
        "Как выбрать недорогую веб-камеру для видеозвонков",
        "Топ-10 товаров для уборки с AliExpress",
        "Рейтинг ортопедических подушек для сна",
        "Как выбрать недорогой тонометр для дома",
        "Лучшие кухонные весы до 500 рублей",
        "Рейтинг недорогих USB-хабов и разветвителей",
        "Топ-5 силиконовых чехлов для смартфонов",
        "Как выбрать бюджетный электрический штопор",
        "Лучшие складные ножи для пикника",
        "Рейтинг недорогих кабель-каналов для проводов",
        "Топ-10 полезных мелочей для автомобиля",
        "Как выбрать дешёвый проектор для домашнего кинотеатра",
        "Лучшие бюджетные микрофоны для стримов",
        "Рейтинг недорогих настольных вентиляторов",
        "Топ-5 товаров для ванной с AliExpress",
        "Как выбрать солнечные батареи для кемпинга",
        "Лучшие дешёвые 3D-ручки для детей",
        "Рейтинг бюджетных массажёров для спины",
        "Топ-10 недорогих подарков на 8 марта",
        "Как выбрать шуруповёрт для мелкого ремонта",
        "Лучшие газонокосилки-триммеры до 3000 рублей",
        "Рейтинг недорогих светильников для аквариума",
        "Топ-5 бюджетных квадрокоптеров с камерой",
        "Как выбрать умную розетку для дома",
        "Лучшие недорогие замки для велосипеда",
        "Рейтинг садовых секаторов и ножниц",
        "Топ-10 компактных зонтов-автоматов",
        "Как выбрать рюкзак-кенгуру для малыша",
        "Лучшие недорогие электрические зубные щётки",
        "Рейтинг бюджетных кофеварок капельного типа",
        "Топ-5 товаров для уюта в комнате",
        "Как выбрать складной столик для ноутбука",
        "Лучшие дешёвые наушники-вкладыши",
        "Рейтинг недорогих ковриков для йоги",
        "Топ-10 кухонных принадлежностей до 200 рублей",
        "Как выбрать механический точилку для ножей",
        "Лучшие бюджетные очистители воздуха",
        "Рейтинг недорогих дорожных несессеров",
        "Топ-5 гаджетов для приготовления кофе"
    ]

    kw = keywords[datetime.now().hour % len(keywords)]
    print(f"📝 Генерирую: {kw}")
    article = generate_article(kw)
    save_article(article, kw)
        # --- Настройки соцсетей (замени на свои или бери из секретов) ---
    twitter_creds = {
        "api_key": os.getenv("TWITTER_API_KEY"),
        "api_secret": os.getenv("TWITTER_API_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET")
    }
        # --- Настройки Telegram ---
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = "@mrwotasvlog"   # ← замени на свой @username или числовой ID

    if telegram_bot_token:
        post_to_telegram(kw, f"{SITE_URL}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}", telegram_bot_token, telegram_chat_id)
        
    pinterest_token = os.getenv("PINTEREST_ACCESS_TOKEN")
    pinterest_board_id = "1095641484287516870"
    pinterest_image_url = "https://via.placeholder.com/800x600.png?text=" + kw.replace(" ", "+")

    # --- Постим (если заданы ключи) ---
    if all(twitter_creds.values()):
        post_to_twitter(kw, f"{SITE_URL}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}", twitter_creds)
    if telegram_bot_token:
        post_to_telegram(kw, f"{SITE_URL}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}", telegram_bot_token, telegram_chat_id)
    if pinterest_token:
        post_to_pinterest(kw, f"{SITE_URL}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}", pinterest_image_url, pinterest_board_id, pinterest_token)
    print("🎉 Готово! Робот отработал.")
