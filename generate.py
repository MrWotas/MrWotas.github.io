# ✅ 1. Подключаем библиотеки
import requests
import os
from datetime import datetime

# ✅ 2. Настройки – сюда впиши свои данные из блокнота
OPENROUTER_API_KEY = "ВСТАВЬ_СВОЙ_API_КЛЮЧ_ОТ_OPENROUTER"
# Больше не нужно! TWITTER_API_KEY, GEMINI_KEY и т.д. убраны для простоты,
# но в будущем ты добавишь их обратно, как в оригинальном плане.

# Партнёрские ссылки для разных тем (можно добавить много)
AFFILIATE_LINKS = {
    "рюкзак": "https://alipromo.com/...твоя_партнёрская_ссылка_на_рюкзак",
    "наушники": "https://alipromo.com/...",
    "по умолчанию": "https://admitad.com/g/..."  # универсальная ссылка
}

# ✅ 3. Функция: ИИ пишет статью (теперь через OpenRouter)
def generate_article(keyword):
    # Выбираем подходящую партнёрскую ссылку по ключевому слову
    link = AFFILIATE_LINKS.get(keyword.split()[0].lower(), AFFILIATE_LINKS["по умолчанию"])
    
    # Промпт (запрос) для ИИ
    prompt = f"""Ты — полезный блогер. Напиши статью на тему "{keyword}" длиной 600-800 слов.
    Статья должна содержать заголовок H1, подзаголовки H2, списки. В середине или в конце естественно вставь рекомендацию товара
    со ссылкой {link}. Текст оформи в Markdown: заголовок статьи в начале как '# Название'.
    После текста не пиши ничего лишнего."""
    
    # НОВЫЙ КОД: Вызов OpenRouter API вместо Gemini
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat:free", # Используем бесплатную модель DeepSeek
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You always respond in Russian."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )
    # Достаём ответ ИИ из полученного JSON
    data = response.json()
    return data['choices'][0]['message']['content']

# ✅ 4. Сохранение статьи в формате Jekyll (GitHub Pages)
# Эта часть остаётся без изменений
def save_article(text, keyword):
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")[:30]
    filename = f"_posts/{date_str}-{slug}.md"
    # Убедимся, что папка _posts существует
    os.makedirs("_posts", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"{keyword}\"\ndate: {datetime.now().isoformat()}\ncategories: blog\n---\n")
        f.write(text)
    print(f"Статья сохранена: {filename}")

# ✅ 5. Публикация в соцсетях (функции-заглушки)
# Пока мы их пропустим, чтобы проверить основную логику. Ты добавишь их позже.
def post_to_twitter(title, url):
    print(f"ЗАГЛУШКА: Твит не отправлен. Тема: {title}, Ссылка: {url}")

def post_to_telegram(title, url):
    print(f"ЗАГЛУШКА: Сообщение в Telegram не отправлено. Тема: {title}, Ссылка: {url}")

# ✅ 6. Главный запуск
if __name__ == "__main__":
    # Список тем статей по очереди
    keywords = ["Как выбрать рюкзак для школы", "Топ-10 бюджетных наушников 2026", "Какой увлажнитель воздуха купить"]
    # Берём тему в зависимости от текущего часа
    index = datetime.now().hour % len(keywords)
    kw = keywords[index]
    
    print(f"Генерирую статью для: {kw}")
    article_md = generate_article(kw)
    save_article(article_md, kw)
    
    # Ссылка на сайт
    site_url = "https://твой-логин.github.io"
    post_url = f"{site_url}/{datetime.now().strftime('%Y/%m/%d')}/{kw.lower().replace(' ', '-')}"
    
    post_to_twitter(kw, post_url)
    post_to_telegram(kw, post_url)
    
    print("Готово! Робот отработал.")
