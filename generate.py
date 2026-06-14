import os
import requests
import time
from datetime import datetime

# ---------- НАСТРОЙКИ ----------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SITE_URL = "https://mrwotas.github.io"   # ваш сайт

AFFILIATE_LINKS = {
    "рюкзак": "https://alipromo.com/...",      # ← вставьте свои партнёрские ссылки
    "наушники": "https://admitad.com/g/...",
    "по умолчанию": "https://admitad.com/..."
}
# -------------------------------

def generate_article(keyword):
    link = AFFILIATE_LINKS.get(keyword.split()[0].lower(), AFFILIATE_LINKS["по умолчанию"])
    prompt = f"""Ты полезный блогер. Напиши статью на тему "{keyword}" длиной 600–800 слов.
Структура: заголовок H1, подзаголовки H2, списки. В середине или в конце органично вставь рекомендацию товара со ссылкой {link}.
Оформи в Markdown: '# Заголовок'. После текста ничего не пиши."""

    print("📡 Отправляю запрос в DeepSeek...")
    for attempt in range(3):
        response = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты всегда отвечаешь на русском языке."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
        )
        data = response.json()
        print("📦 Ответ:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        error_code = data.get("error", {}).get("code")
        if error_code == "rate_limit_exceeded":
            print(f"⏳ Превышен лимит запросов. Жду 30 секунд... (попытка {attempt+1}/3)")
            time.sleep(30)
            continue
        else:
            raise Exception(f"❌ DeepSeek вернул ошибку: {data}")

    raise Exception("❌ Не удалось получить ответ от DeepSeek после нескольких попыток")

def save_article(text, keyword):
    os.makedirs("_posts", exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")[:40]
    filename = f"_posts/{date_str}-{slug}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"{keyword}\"\ndate: {datetime.now().isoformat()}\ncategories: blog\n---\n")
        f.write(text)
    print(f"✅ Статья сохранена: {filename}")

# (Функции для соцсетей остаются без изменений, возьмите из предыдущего ответа)
# def post_to_telegram(...)
# def post_to_twitter(...)
# def post_to_pinterest(...)

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
    telegram_chat_id = "@MrWotas_Blog"
    if telegram_bot_token:
        # post_to_telegram(...)  # раскомментируйте, когда добавите функцию
        pass

    # Аналогично для Twitter/Pinterest (оставлены для будущего)
    print("🎉 Готово! Робот отработал.")
