from django.conf import settings


class SocialFriendsFinderBackendFactory():

    @classmethod
    def get_backend(self, backend_name):
        """
        returns the given backend instance
        """
        
        # Facebook Backend
        if backend_name == 'facebook':
            from social_friends_finder.backends.facebook_backend import FacebookFriendsProvider
            friends_provider = FacebookFriendsProvider()
            
        # Twitter Backend
        elif backend_name == 'twitter':
            from social_friends_finder.backends.twitter_backend import TwitterFriendsProvider
            friends_provider = TwitterFriendsProvider()
            
        # Google Backend
        #elif backend_name == 'google':
            #from social_friends_finder.backends.google_backend import GoogleFriendsProvider
            #friends_provider = GoogleFriendsProvider()
            
        else:
            raise NotImplementedError("provider: %s is not implemented")

        return friends_provider


def setting(name, default=None):
    """returns the setting value or default if not exists"""
    return getattr(settings, name, default)
