import requests
import os
from datetime import datetime

# Configurazione ("Secrets" di GitHub per sicurezza)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news():
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&language=it&q=mondo&timeframe=24&prioritydomain=top"
    
    try:
        response = requests.get(url).json()
        
        # Controlliamo se l'API ha risposto con un errore (status != success)
        if response.get('status') != "success":
            errore_msg = response.get('results', {}).get('message', 'Errore sconosciuto')
            return f"❌ Errore dall'API delle notizie: {errore_msg}"

        articoli = response.get('results', [])
        
        if not articoli:
            return "📭 Nessuna notizia rilevante nelle ultime 24 ore."

        data_oggi = datetime.now().strftime("%d/%m/%Y")
        report = f"🗞 **REPORT MATTUTINO - {data_oggi}**\n"
        report += "______________________________\n\n"
        
        # Prendiamo i primi 5 articoli in modo sicuro
        for art in articoli[:5]:
            titolo = art.get('title', 'Titolo non disponibile')
            link = art.get('link', '#')
            report += f"📍 **{titolo}**\n🔗 [Leggi l'articolo]({link})\n\n"
        
        return report

    except Exception as e:
        return f"⚠️ Errore tecnico nel recupero notizie: {e}"

def send_telegram_message(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": testo,
        "parse_mode": "Markdown",
        "link_preview_options": {
            "is_disabled": False,
            "prefer_small_media": True
        }
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    notizie = get_news()
    send_telegram_message(notizie)
