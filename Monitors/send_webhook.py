import requests
from datetime import datetime


def send_webhook(_url, embed_title, description, embed_image, lowest_price):
    webhook_url = 'https://discord.com/api/webhooks/807177309828284427/Sx3vfY5_WQcot2bNYO2QrOYC9KZdMLlavC9xRRX43hgeleRR0ZrvexsgLOSHOradNNKd'
    current_time = datetime.now().strftime("%H:%M:%S")
    data = {"username": "Bob the builder", "embeds": [
        {
            "title": embed_title,
            "description": f'[{description}]({_url})',
            "color": 1127128,
            "footer": {"text": f"onlyFNF [{current_time}]", "icon_url": "https://i.imgur.com/fKL31aD.jpg"},
            "fields": [{"name": "Price", "value": lowest_price}],
            "thumbnail": {"url": embed_image},
        }
    ]}

    res = requests.post(webhook_url, json=data)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        print(f"Payload delivered successfully, code{res.status_code}")
