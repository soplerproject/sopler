from social_friends_finder.backends import BaseFriendsProvider
from social_friends_finder.utils import setting

if setting("SOCIAL_FRIENDS_USING_ALLAUTH", False):
    USING_ALLAUTH = True
    from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
else:
    USING_ALLAUTH = False
    #from social_auth.backends.facebook import FacebookBackend

import facebook
    
class FacebookFriendsProvider(BaseFriendsProvider):

    def fetch_friends(self, user):
        """
        Fethces friends from facebook.
        Returns:
            collection of friend objects fetched from facebook
        """
        if USING_ALLAUTH:
	  social_app = SocialApp.objects.get_current('facebook')
	  oauth_token = SocialToken.objects.get(account=user, app=social_app).token
            
        else:
	  pass
	  #social_auth_backend = FacebookBackend()
	  #tokens = social_auth_backend.tokens(user)
	  #oauth_token = tokens['access_token']

        graph = facebook.GraphAPI(oauth_token)
        return graph.get_connections("me", "friends")

    def fetch_friend_ids(self, user):
        """
        Fethces friend id's from facebook
        Return:
            collection of friend ids
        """
        friends = self.fetch_friends(user)
        friend_ids = []
        for friend in friends['data']:
            friend_ids.append(friend['id'])
        return friend_ids
