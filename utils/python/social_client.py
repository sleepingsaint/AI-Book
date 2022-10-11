import os
import tweepy
from discord_webhook import DiscordWebhook
from typing import Union

class SocialClient:
    def __init__(self) -> None:
        # discord keys
        self.discord_sources_webhook_url = os.environ.get("DISCORD_SOURCES_WEBHOOK_URL", None)
        self.discord_resources_webhook_url = os.environ.get("DISCORD_RESOURCES_WEBHOOK_URL", None)

        # twitter keys
        self.twitter_api_key = os.environ.get("TWITTER_API_KEY", None)
        self.twitter_api_key_secret = os.environ.get("TWITTER_API_KEY_SECRET", None)
        self.twitter_bearer_token = os.environ.get("TWITTER_BEARER_TOKEN", None)
        self.twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN", None)
        self.twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", None)

        self.twitter_client = self._getTwitterClient()
        # reddit keys
    
    def _getTwitterClient(self) -> Union[tweepy.Client, None]:
        secret_keys = [
            self.twitter_api_key,
            self.twitter_api_key_secret,
            self.twitter_bearer_token,
            self.twitter_access_token,
            self.twitter_access_token_secret
        ]
        
        for key in secret_keys:
            if key is None:
                return None

        client = tweepy.Client(
            bearer_token=self.twitter_bearer_token,
            consumer_key=self.twitter_api_key,
            consumer_secret=self.twitter_api_key_secret,
            access_token=self.twitter_access_token,
            access_token_secret=self.twitter_access_token_secret,
            wait_on_rate_limit=True
        )

        return client

    def sendSourceNotification(self, source, url):
        self.sendDiscordSourceNotification(source, url)
        self.sendRedditSourceNotification(source, url)
#         self.sendTwitterSourceNotification(source, url)

    def sendResourceNotification(self, resource_url):
        self.sendDiscordResourceNotification(resource_url)
        self.sendRedditResourceNotification(resource_url)
#         self.sendTwitterResourceNotification(resource_url)    

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
        if self.twitter_client is not None:
            self.twitter_client.create_tweet(text=f"{source} Added\n{url}")
    
    def sendTwitterResourceNotification(self, resource_url):
        if self.twitter_client is not None:
            self.twitter_client.create_tweet(text=f"{resource_url}\n{resource_url}")
