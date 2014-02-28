
# ---------------------------------------------------------------------------------------------------------------------------------------
# An alternative implementation for :
# django-social-friends-finder "twitter_backend.py" [1] based on tweepy [2].
# -----------------------------------
# [1] https://github.com/laplacesdemon/django-social-friends-finder/blob/master/social_friends_finder/backends/twitter_backend.py
# [2] http://pythonhosted.org/tweepy/html/index.html
# ---------------------------------------------------------------------------------------------------------------------------------------
import time
from social_friends_finder.backends import BaseFriendsProvider
from social_friends_finder.utils import setting

if setting("SOCIAL_FRIENDS_USING_ALLAUTH", False):
    USING_ALLAUTH = True
    from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp

else:
    USING_ALLAUTH = False
    
import tweepy

class TwitterFriendsProvider(BaseFriendsProvider):

    def fetch_friends(self, user):
        """
	Fetches the friends from twitter.
	Returns:
	collection of friend objects fetched from twitter
	"""
	
        if USING_ALLAUTH:
	  
	    # Consumer keys and access tokens, used for OAuth
	    social_app = SocialApp.objects.get_current('twitter')
	    
	    # Consumer key and secret
	    consumer_key = social_app.client_id
	    consumer_secret = social_app.secret

	    oauth_token = SocialToken.objects.get(account=user, app=social_app).token
	    oauth_token_secret = SocialToken.objects.get(account=user, app=social_app).token_secret
	    
            consumer_key = consumer_key
            consumer_secret = consumer_secret
            access_token_key = oauth_token
            access_token_secret = oauth_token_secret
            
	    # OAuth process, using the keys and tokens
	    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	    auth.set_access_token(access_token_key, access_token_secret)

	    # Now fetch the twitter friends using `tweepy`
	    api = tweepy.API(auth)
	    
	    while True:
	      try:
		user = api.me()
		return user.followers_ids()
	      except tweepy.TweepError:
		time.sleep(2)
		user = api.me()
		return user.followers_ids()
	  
        else:
	    pass
	    


    def fetch_friend_ids(self, user):
        """
        Fethces friend id's from twitter
        Return:
            collection of friend ids
        """
        friends = self.fetch_friends(user)
        friend_ids = []
        for friend in friends:
            friend_ids.append(friend)
        return friend_ids
