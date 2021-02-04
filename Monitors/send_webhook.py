from discord_webhook import DiscordWebhook, DiscordEmbed


def send_webhook(_url, embed_title, embed_image):
    webhook = DiscordWebhook(url=_url)
    embed = DiscordEmbed(title="Item restocked on Amazon", description="["+embed_title+"]("+amazon_url+")",color=3436348)
    embed.set_thumbnail(url=embed_image)

    embed.set_footer(text='Amazon Monitor', icon_url='url')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
