import urllib2
from bs4 import BeautifulSoup


class ResultsPage(object):
    def __init__(self, url):
        """
        Takes a url and constructs a ResultsPage object.
        """
        # Gets the page HTML from the url.
        html = urllib2.urlopen(url).read()
        page_soup = BeautifulSoup(html, "html.parser")
        # Gets the link for the next page (or sets the value to None).
        self.older_link = page_soup.find(class_='blog-pager-older-link')['href']
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
        self.timestamp = post.find('a', class_='timestamp-link').find('abbr')['title']
        self.tags = []
        for tag in post.find(class_='post-footer').find('span', class_='post-labels').find_all('a', rel='tag'):
            self.tags.append(tag)
