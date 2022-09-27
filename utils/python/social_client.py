import os
from discord_webhook import DiscordWebhook

class SocialClient:
    def __init__(self) -> None:
        # discord keys
        self.discord_sources_webhook_url = os.environ.get("DISCORD_SOURCES_WEBHOOK_URL", None)
        self.discord_resources_webhook_url = os.environ.get("DISCORD_RESOURCES_WEBHOOK_URL", "https://discord.com/api/webhooks/1024299514678493326/NCUpSnAEEHUu-bKUdWUaAHbppAsaO522lwIL2n8YXi_gIk2fwt2NbaJ4L-A5oBBJB7mS")

        # twitter keys
        
        # reddit keys
    
    def sendSourceNotification(self, source, url):
        self.sendDiscordSourceNotification(source, url)
        self.sendRedditSourceNotification(source, url)
        self.sendTwitterSourceNotification(source, url)

    def sendResourceNotification(self, resource_url):
        self.sendDiscordResourceNotification(resource_url)
        self.sendRedditResourceNotification(resource_url)
        self.sendTwitterResourceNotification(resource_url)    

    # discord notification handlers
    def sendDiscordSourceNotification(self, source, url):
        if self.discord_sources_webhook_url is not None:
            webhook = DiscordWebhook(url=self.discord_sources_webhook_url, rate_limit_retry=True, content=f"[{source} Added]({url})")
            webhook.execute()
    
    def sendDiscordResourceNotification(self, resource_url):
        if self.discord_resources_webhook_url is not None:
            webhook = DiscordWebhook(url=self.discord_resources_webhook_url, content=resource_url, rate_limit_retry=True)
            webhook.execute()

    # reddit notification handlers
    def sendRedditSourceNotification(self, source, url):
        pass
    
    def sendRedditResourceNotification(self, resource_url):
        pass

    # twitter notification handlers
    def sendTwitterSourceNotification(self, source, url):
        pass
    
    def sendTwitterResourceNotification(self, resource_url):
        pass
