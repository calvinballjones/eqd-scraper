import urllib2

import time

from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import pytz
from models import PostModel, TagModel, TagRelation


class ResultsPage(object):
    def __init__(self, url):
        """
        Takes a url and constructs a ResultsPage object.
        """
        # Gets the page HTML from the url.
        html = ""
        while True:
            try:
                html = urllib2.urlopen(url).read()
                break
            except urllib2.HTTPError:
                print "Could not get page. Trying again."
                time.sleep(2)
        page_soup = BeautifulSoup(html, "html.parser")
        # Gets the link for the next page (or sets the value to None).
        try:
            self.older_link = page_soup.find(class_='blog-pager-older-link')['href']
        except TypeError:
            self.older_link = None
        # Separates the posts out into separate Post objects and saves them as a list.
        self.posts = []
        for post in page_soup.find_all('li', class_='blog-post'):
            self.posts.append(Post(post))
            # TODO: Add Post code.


class Post(object):
    def __init__(self, post):
        """
        Takes a post BeautifulSoup tag object and constructs a Post object.
        """
        title_tag = post.find('h3', class_='post-title').find('a')
        self.link = title_tag['href']
        self.title = title_tag.string
        try:
            self.timestamp = date_parser.parse(
                post.find('a', class_='timestamp-link').find('abbr')['title']).astimezone(
                pytz.utc)
        except AttributeError:
            print "Could not find timestamp for %s." % post.title
            self.timestamp = None
        self.tags = []
        try:
            for tag in post.find(class_='post-footer').find('span', class_='post-labels').find_all('a', rel='tag'):
                self.tags.append(tag)
        except AttributeError:
            print "Could not find tags for %s." % post.title

    def save_to_db(self):
        # Only create a new post instance in the database if it doesn't exist already.
        try:
            PostModel.get(PostModel.link == self.link)
            return 1
        except PostModel.DoesNotExist:
            post_model = PostModel.create(title=self.title, link=self.link, timestamp=self.timestamp)
            post_model.save()

            # Save the tags
            for tag in self.tags:
                # Check that there is already a tag
                try:
                    tag_model = TagModel.get(TagModel.tag_name == tag.string)
                except TagModel.DoesNotExist:
                    tag_model = TagModel.create(tag_name=tag.string, tag_link=tag['href'])
                    tag_model.save()

                # Check that there isn't already a relationship
                try:
                    TagRelation.get(TagRelation.post_id == post_model.get_id(),
                                    TagRelation.tag_id == tag_model.get_id())
                except TagRelation.DoesNotExist:
                    tag_relation = TagRelation.create(post_id=post_model, tag_id=tag_model)
                    tag_relation.save()

            return 0
