"""
Celery tasks
Run the following command to run celery:
    celery -A mysite worker -l info
"""
from __future__ import absolute_import
from celery import shared_task
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

@shared_task
def crawl_task(sender, instance_id):
    """Task to crawl seed_url to the given depth.
    seed_url and depth are obtained using CrawlRequest id. 
    The task will update the status of CrawlRequest to Success/Error.
    """
    from .models import CrawlRequest, CrawledImages
    my_crawl_request = CrawlRequest.objects.get(id = instance_id)
    urls_to_crawl = get_urls(my_crawl_request.seed_url, my_crawl_request.depth)  # Get all urls to crawl.
    my_images = get_images(urls_to_crawl)  # Crawl urls and get images.
    
    # Add images to the database.
    images_to_insert = []
    for image in my_images:
        images_to_insert.append(CrawledImages(crawl_request = my_crawl_request, image_url = image))
    CrawledImages.objects.bulk_create(images_to_insert)

    # Update status of the CrawlRequest record to success.
    my_crawl_request.status = "Success"
    my_crawl_request.save()

def get_urls(seed_url, depth):
    """A function that returns a set of distinct URLs resulted from crawling
    by providing a seed_url and depth.
    """
    # my_urls contain the final list of urls.
    # current_urls store the urls to be crawled at the current level.
    my_urls = current_urls = set([seed_url])
    current_depth = 1  # Initialize current_depth.

    # Crawl urls at each depth and add to my_urls.
    while current_depth < depth:
        new_urls = set([])
        # Crawl each URL in current_urls for links
        for url in list(current_urls):
            # Fetch URL and parse the html document
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.find_all('a')
            domain = get_domain(url)

            # Populate new_urls with valid urls.
            for link in links:
                try:
                    link_url = link['href']
                    if '//' not in link_url:
                        # Found url without scheme.
                        # Add to the domain url.
                        if '#' not in link_url:
                            # This is not an intrapage link
                            new_urls.add(urljoin(domain, link_url))
                    else:
                        # Scheme was found.
                        new_urls.add(link_url)
                except KeyError, IOError:
                    pass
        current_depth += 1  # Increment depth
        current_urls = new_urls.difference(my_urls)  # Add newly found urls not in my_urls to current_urls
        my_urls.update(current_urls)  # Add newly found urls to my_urls

    return list(my_urls)


def get_images(url_list):
    """A function that return a list of images by visiting pages specified
    in the input url_list.
    """
    my_images = set([])  # The final set of images that will be returned.

    # Fetch URL and parse the html document.
    for url in url_list:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')  # Find all the images in the page.
        domain = get_domain(url)

        # Get urls for the images and add them to my_images.
        for image in images:
            try:
                image_url = image['src']
                if 'data:image' in image_url:
                    # Skip inline images
                    pass
                elif '//' not in image_url:
                    # If url does not contain scheme, add url to domain
                    my_images.add(urljoin(domain,image_url)) 
                else:
                    my_images.add(image_url)
            except KeyError:
                pass

    return list(my_images)


def get_domain(url):
    """Return domain name of a given URL"""
    parsed_url = urlparse(url)
    return '%s://%s' %(parsed_url.scheme, parsed_url.netloc)