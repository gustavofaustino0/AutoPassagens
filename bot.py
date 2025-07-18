import requests
import urllib.parse


def enviar_mensagem(mensagem):
    chat_id = "-1002763074361"
    token = "7754573882:AAGjggAWXmgYBI32Y8jDCrqAK-Xk7BYfA2Q"

    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote(mensagem)}&parse_mode=HTML"
    response = requests.get(url)
    print("Status code:", response.status_code)
