import requests
import os

# Configurazione (Useremo le "Secrets" di GitHub per sicurezza)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news():
    # Usiamo NewsData.io come esempio (registrati per la key gratuita)
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&language=it&q=tecnologia"
    response = requests.get(url).json()
    
    articoli = response.get('results', [])[:5] # Prendiamo le prime 5 notizie
    report = "🗞 **REPORT MATTUTINO**\n\n"
    
    for art in articoli:
        report += f"🔹 **{art['title']}**\n"
        report += f"🔗 [Leggi di più]({art['link']})\n\n"
    
    return report

def send_telegram_message(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    notizie = get_news()
    send_telegram_message(notizie)
