""" this script is designed to interact with the Vomanc web application API """
import asyncio
import aiohttp


DOMAIN = 'http://127.0.0.1:8000/api/v1/'
URL_LOGIN = 'auth/token/login/'
URL_USER = 'user/1'
URL_USER_LIST = 'users-list/'
URL_TWITTER = 'social/twitter/'
URL_TWEET_POSTED = 'social/tweet-create/'
URL_TWEET_MEDIA_POSTED = 'social/tweet-media/'
URL_TWITTER_UPDATE = 'social/tweet-update/'
URL_TWITTER_CLEAR = 'social/tweet-clean/'

HEADERS = {
    "Content-Type": "application/json",
    }

USER_AUTH = {
    "username": "",
    "password": "",
    }


# PAYLOAD_TWEET = [{
#     'tweet_id': '2637431000677470215',
#     'screen_name': '@new',
#     'user': '@api',
#     'tweet_text': 'my text',
#     'preview': 'http://127.0.0.1:8000',
#     'media_url': ['http://127.0.0.1:8000','http://127.0.0.1:8000']
# }]


class VomancApi():
    """ For request """
    def __init__(self):
        """ Created session """
        self.session = aiohttp.ClientSession()

    async def request_delete(self, url, auth=None):
        """ Executes a delete request """
        async with self.session.delete(
            ''.join((DOMAIN, url)),
            headers=HEADERS,
            auth=auth
        ) as response:
            print('\n', response.status, '\n', url, '\n',
                  response.headers['Allow'], '\n', '-' * 20)
            return await response.json()

    async def request_post(self, url, payload, auth=None):
        """ Executes a post request to get a token"""
        async with self.session.post(
            ''.join((DOMAIN, url)),
            headers=HEADERS,
            json=payload,
            allow_redirects=True,
            auth=auth
        ) as response:
            print('\n', response.status, '\n', url, '\n',
                  response.headers['Allow'], '\n', '-'*20)
            return await response.json()

    async def request_get(self, url, params=None, auth=None, token=None):
        """ Executes a get request with setting the token if it is specified"""
        if token is not None:
            HEADERS["Authorization"] = f'Token {token}'
        async with self.session.get(
                ''.join((DOMAIN, url)), headers=HEADERS, params=params, auth=auth) as response:
            print('\n', response.status, '\n', url, '\n',
                  response.headers['Allow'], '\n', '-' * 20)
            return await response.json()

    async def add_tweet_list(self, tweets_list, auth):
        """ Add TWEET and TWEET MEDIA """
        for tweet in tweets_list:
            if tweet['media_url']:
                media_urls = tweet['media_url']
                tweet['media_url'] = []
            else:
                media_urls = None

            tweet_id = await self.request_post('social/tweet-create/', tweet, auth)
            print(tweet_id)
            if media_urls:
                for i in media_urls:
                    media = {
                        "owner": tweet_id['id'],
                        "url": i
                    }
                    resp = await self.request_post(URL_TWEET_MEDIA_POSTED, media, auth)
                    print(resp)


async def main():
    """ GET USERS LIST """
    auth = aiohttp.BasicAuth("username", "password")
    api = VomancApi()
    # # USER
    # user = await api.request_get(URL_USER)
    # print(user)

    # # USER_LIST
    # token = await api.request_post(URL_LOGIN, USER_AUTH)  # TOKEN
    # users_list = await api.request_get(URL_USER_LIST, token=token["auth_token"])
    # print(users_list)

    # # USER_LIST 2
    # users_list = await api.request_get(URL_USER_LIST, auth=auth)
    # print(users_list)

    # # TWITTER LIST
    # params = {'twitter_list': 'True'}
    # # tweet_list = await api.request_get(URL_TWITTER, params, token=token["auth_token"])
    # # OR
    # tweet_list = await api.request_get(URL_TWITTER, params, auth)
    # print(tweet_list)
    # for tweet in tweet_list['results']:
    #     # For pagination
    #     print(tweet)

    # # TWITTER
    # params = {'tweet': '1'}
    # tweet = await api.request_get(URL_TWITTER, params=params, auth=auth)
    # print(tweet)

    # # ADD TWEET
    # resp = await api.add_tweet_list(PAYLOAD_TWEET, auth)
    # print(resp)

    # # UPDATE TWITTER
    resp = await api.request_get(URL_TWITTER_UPDATE, auth=auth)
    print(resp)

    # # TWITTER CLEAR
    # resp = await api.request_delete(URL_TWITTER_CLEAR, auth=auth)
    # print(resp)

    # # CLOSE SESSION
    await api.session.close()


asyncio.run(main())
