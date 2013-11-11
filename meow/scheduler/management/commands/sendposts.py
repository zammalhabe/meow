from django.core.management.base import BaseCommand, CommandError
from scheduler.models import *
import tweepy
from facepy import GraphAPI
from facepy.exceptions import *
from scheduler.models import *
from datetime import datetime
from django.utils import timezone
import urllib2
from bs4 import BeautifulSoup
import HTMLParser

class Command(BaseCommand):
    help = "Sends the appropriate social media posts"

    def sendTweet(self, smpost, section, bitly_link):
        print "Send tweet"
        try:
            print smpost.post_twitter.encode('ascii','ignore')
            CONSUMER_KEY = MeowSetting.objects.get(setting_key='twitter_consumer_key').setting_value
            CONSUMER_SECRET = MeowSetting.objects.get(setting_key='twitter_consumer_secret').setting_value
            ACCESS_KEY = section.twitter_access_key
            ACCESS_SECRET = section.twitter_access_secret
        
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        
            api = tweepy.API(auth)
        
            # Check for bitly link
            if bitly_link is not None:
                url = bitly_link
            else:
                url = smpost.story_url

            # Make the tweet follow DB social media standards
            tweet = smpost.post_twitter

            if smpost.story_url is not None:
                tweet = tweet + " " + url
        
            api.update_status(tweet)
        
        except tweepy.TweepError as e:
            smpost.log_error(e, section)
        

    def sendFacebookPost(self, smpost, section, bitly_link):
        print "send fb"
        try:
            print smpost.post_facebook.encode('ascii','ignore')
            #follow these steps: http://stackoverflow.com/questions/17620266/getting-a-manage-page-access-token-to-upload-events-to-a-facebook-page
            #Facebook needs the following permissions:
            # status_update, manage_pages
        
        
            # Initialize the Graph API with a valid access token (optional,
            # but will allow you to do all sorts of fun stuff).
        
            # Get token from here: https://developers.facebook.com/docs/opengraph/howtos/publishing-with-app-token/
            # appGraph = GraphAPI('72296391616|_vtz8ShgOfzLSgKeDw2quIS1pCc')
            GRAPH_KEY = section.facebook_key
            graph = GraphAPI(GRAPH_KEY) # This should not expire

            PAGE_ID = section.facebook_page_id

            # Get the post HTML
            try:
                usock = urllib2.urlopen(smpost.story_url)
                post_html = usock.read()
                usock.close()
            except urllib2.HTTPError as e:
                if e.code != 500:
                    raise
                else:
                    smpost.log_error(e, section)
                    post_html = ""
            
            post_dom = BeautifulSoup(post_html)
            post_image_tag = post_dom.find('img', "wp-post-image")
        
            # Detect if the post has an actual image/src we can use (why not be too careful)
            has_image = False;
            if post_image_tag is not None:
                post_image_url = post_image_tag.attrs['data-lazy-src']
                if post_image_url is None:
                    post_image_tag.attrs['src']
                # Set the flag
                if post_image_url is not None:
                    has_image = True
        
            # Check for bitly link
            if bitly_link is not None:
                url = bitly_link
            else:
                url = smpost.story_url

            ### Now actually post to Facebook
        
            # The story does not have an image
            if has_image is False:
                DEFAULT_PHOTO = MeowSetting.objects.get(setting_key='fb_default_photo').setting_value
                graph.post(
                    path = PAGE_ID+'/feed',
                    message = smpost.post_facebook,
                    link = smpost.story_url,
                    picture = DEFAULT_PHOTO,
                )
        
            # The story has an image
            else:
                graph.post(
                    path = PAGE_ID+'/photos',
                    message = smpost.post_facebook + "\n\nRead more: " + url,
                    type= "photo",
                    source = urllib2.urlopen(post_image_url),
                )

        except (FacepyError, FacebookError, OAuthError, HTTPError, SignedRequestError, urllib2.URLError, urllib2.HTTPError, HTMLParser.HTMLParseError) as e:
            smpost.log_error(e, section)

    def handle(self, *args, **options):
        send_posts = MeowSetting.objects.get(setting_key="send_posts").setting_value
        if send_posts == "No" or send_posts == "no":
            print "Post sending is currently off!"
            return
            

        # Get posts from the database that are ready to send
        posts = SMPost.objects.filter(
                pub_date__lte=datetime.now().date()
            ).filter(
                pub_time__lte=datetime.now().time()
            ).filter(
                pub_ready_copy=True
            ).filter(
                pub_ready_online=True
            ).exclude(
                sent=True
            ).exclude(
                section=None
            )
        
        for post in posts:
            try:
                # Make sure nothing else is trying to send this post right now
                # This is not atomic; if meow ever scales a lot more, this will need to be re-written
                if post.sending:
                    continue
                else:
                    post.sending = True
                    post.save()
            
                # This is just Bitly -- it won't throw any exceptions
                # send_url[0] is canonical. send_url[1] is short url.
                send_url = post.get_send_url()
                
                # Post to facebook
                if post.post_facebook:
                    # Section's account
                    if (post.section.facebook_page_id and post.section.facebook_key):
                        self.sendFacebookPost(post, post.section, link)
                    # Also post to account
                    if (post.section.also_post_to and 
                        post.section.also_post_to.facebook_page_id and post.section.also_post_to.facebook_key):
                        self.sendFacebookPost(post, post.section.also_post_to, link)
                # Post to twitter
                if post.post_twitter:
                    # Section's account
                    if (post.section.twitter_access_key and post.section.twitter_access_secret):
                        self.sendTweet(post, post.section, link)
                    # Also post to account
                    if (post.section.also_post_to and 
                        post.section.also_post_to.twitter_access_key and post.section.also_post_to.twitter_access_secret):
                        self.sendTweet(post, post.section.also_post_to, link)
            # These are the only cases we'll retry (4xx, 5xx)
            except urllib2.HTTPError as e:
                # We'll only get here for a non-3xx error. Don't send the post out.
                post.log_error(e, section, True)
            except:
                pass
            
            # Now save whatever we changed to the post
            try:    
                post.sending = False;        
                post.sent = True
                post.sent_time = timezone.now()
                post.save()
            except:
                print "Something is very wrong"
                pass # But we can still try the rest of the posts that are going to be sent
