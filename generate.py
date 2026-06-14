import os
import requests
import time
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://mrwotas.github.io"   # ← ваш сайт

AFFILIATE_LINKS = {
    "рюкзак": "https://alipromo.com/...",      # ← вставьте свои ссылки
    "наушники": "https://admitad.com/g/...",
    "по умолчанию": "https://admitad.com/..."
}
# -------------------------------

def generate_article(keyword):
    link = AFFILIATE_LINKS.get(keyword.split()[0].lower(), AFFILIATE_LINKS["по умолчанию"])
    prompt = f"""Ты полезный блогер. Напиши статью на тему "{keyword}" длиной 600–800 слов.
Структура: заголовок H1, подзаголовки H2, списки. В середине или в конце органично вставь рекомендацию товара со ссылкой {link}.
Оформи в Markdown: '# Заголовок'. После текста ничего не пиши."""

    # Список бесплатных моделей (актуален на июнь 2026)
    models = [
        "nousresearch/hermes-3-llama-3.1-405b:free",
        "google/gemma-2-9b-it:free",
        "cohere/command-r:free",
        "mistralai/mistral-7b-instruct:free"   # если вернётся в free
    ]

    for model in models:
        print(f"📡 Пробую модель: {model}")
        for attempt in range(3):  # до 3 попыток на модель
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
                continue  # повторяем ту же модель
            else:
                # 404, 401 и др. – модель недоступна, переходим к следующей
                print(f"⚠️ Модель {model} недоступна: {data['error']['message']}")
                break  # выходим из цикла попыток для этой модели

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

def post_to_telegram(title, url, bot_token, chat_id):
    message = f"🔥 *{title}*\n\n{url}"
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    )
    print("📬 Сообщение в Telegram отправлено")

def post_to_twitter(title, url, creds):
    import tweepy
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_secret"]
    )
    tweet_text = f"{title}\n{url}"
    client.create_tweet(text=tweet_text)
    print("🐦 Твит опубликован")

def post_to_pinterest(title, url, image_url, board_id, access_token):
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

    post_url = f"{SITE_URL}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}"

    # Telegram
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = "@MrWotas_Blog"   # ← замените на ваш канал
    if telegram_bot_token:
        post_to_telegram(kw, post_url, telegram_bot_token, telegram_chat_id)

    # Twitter
    twitter_creds = {
        "api_key": os.getenv("TWITTER_API_KEY"),
        "api_secret": os.getenv("TWITTER_API_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET")
    }
    if all(twitter_creds.values()):
        post_to_twitter(kw, post_url, twitter_creds)

    # Pinterest
    pinterest_token = os.getenv("PINTEREST_ACCESS_TOKEN")
    pinterest_board_id = "1095641484287516870"  # ← ваш board_id
    pinterest_image_url = "https://via.placeholder.com/800x600.png?text=" + kw.replace(" ", "+")
    if pinterest_token:
        post_to_pinterest(kw, post_url, pinterest_image_url, pinterest_board_id, pinterest_token)

    print("🎉 Готово! Робот отработал.")
