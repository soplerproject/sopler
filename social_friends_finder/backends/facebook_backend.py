from social_friends_finder.backends import BaseFriendsProvider
from social_friends_finder.utils import setting
import facebook
import urlparse

if setting("SOCIAL_FRIENDS_USING_ALLAUTH", False):
    USING_ALLAUTH = True
    from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
    
else:
    USING_ALLAUTH = False

    
class FacebookFriendsProvider(BaseFriendsProvider):

    def fetch_friends(self, user, paginate=False):
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
	
	# Get the access_token
        graph = facebook.GraphAPI(oauth_token)
	friends = graph.get_connections("me", "friends")

        if paginate:
            total_friends = friends.copy()
            total_friends.pop('paging')
            
            while 'paging' in friends and 'next' in friends['paging'] and friends['paging']['next']:
                next_url = friends['paging']['next']
                next_url_parsed = urlparse.urlparse(next_url)
                query_data = urlparse.parse_qs(next_url_parsed.query)
                query_data.pop('access_token')
                for k, v in query_data.items():
                    query_data[k] = v[0]
                    
                friends = graph.get_connections("me", "friends", **query_data)
                total_friends['data'] = sum([total_friends['data'], friends['data']], [])
        else:
            total_friends = friends

        return total_friends

    def fetch_friend_ids(self, user, **kwargs):
        """
        Fethces friend id's from facebook
        Return:
            collection of friend ids
        """
        friends = self.fetch_friends(user, **kwargs)
        friend_ids = []
        for friend in friends['data']:
            friend_ids.append(friend['id'])
        return friend_ids
