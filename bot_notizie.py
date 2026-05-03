import requests
import os
from datetime import datetime

# Configurazione ("Secrets" di GitHub per sicurezza)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def get_news():
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&language=it&q=tecnologia&q=sport&prioritydomain=top"
    
    try:
        response = requests.get(url).json()
        
        if response.get('status') != "success":
            # Se c'è ancora un errore, lo stampiamo per capire
            return f"❌ Errore API: {response.get('results', {}).get('message', 'Errore generico')}"

        articoli = response.get('results', [])
        
        if not articoli:
            return "📭 Nessuna notizia trovata al momento."

        data_oggi = datetime.now().strftime("%d/%m/%Y")
        report = f"🗞 **REPORT MATTUTINO - {data_oggi}**\n"
        report += "______________________________\n\n"
        
        for art in articoli[:5]:
            titolo = art.get('title', 'Titolo non disponibile')
            link = art.get('link', '#')
            # Prendiamo anche la data di pubblicazione per sicurezza
            pub_date = art.get('pubDate', '')
            
            report += f"📍 **{titolo}**\n"
            if pub_date:
                report += f"🕒 *Pubblicato il: {pub_date}*\n"
            report += f"🔗 [Leggi l'articolo]({link})\n\n"
        
        return report

    except Exception as e:
        return f"⚠️ Errore tecnico: {e}"

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
