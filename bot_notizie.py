import requests
import os
from datetime import datetime

# Configurazione ("Secrets" di GitHub per sicurezza)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news():
    # Usiamo NewsData.io (registrati per la key gratuita)
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&language=it&q=tecnologia&timeframe=24&prioritydomain=top"
    
    try:
        response = requests.get(url).json()
        articoli = response.get('results', [])[:5] # Prendiamo le prime 5 notizie

        if not articoli:
            return "📭 Nessuna notizia rilevante nelle ultime 24 ore."

        data_oggi = datetime.now().strftime("%d/%m/%Y")
        report = f"🗞 **REPORT MATTUTINO - {data_oggi}**\n\n"
    
        for art in articoli:
            titolo = art.get('title', 'Titolo non disponibile')
            link = art.get('link', '#')
            report += f"📍 **{titolo}**\n🔗 [Leggi l'articolo]({link})\n\n"
    
        return report
    except Exception as e:
        return f"⚠️ Errore nel recupero notizie: {e}"

def send_telegram_message(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown"
        "link_preview_options": {
            "is_disabled": False
            "prefer_small_media": True
        }
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    notizie = get_news()
    send_telegram_message(notizie)
