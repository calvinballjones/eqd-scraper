import datetime

import pytz
from blog_classes import ResultsPage

datetime_format_string = "%b %d, %Y"
first_post_datetime = datetime.datetime(2011, 1, 18, tzinfo=pytz.utc)
download_offset_in_seconds = 2

# Main Function
if __name__ == '__main__':
    # current_results_page = ResultsPage('http://equestriadaily.com')
    current_results_page = ResultsPage('http://www.equestriadaily.com/search?updated-max=2011-01-30T15:30:00-07:00&max-results=13&start=26&by-date=false')
    last_page_get_datetime = datetime.datetime.now(tz=pytz.utc)

    while True:
        time_to_go = current_results_page.posts[-1].timestamp - first_post_datetime

        try:
            soonest_result_time = current_results_page.posts[0].timestamp.strftime(datetime_format_string)
        except AttributeError:
            soonest_result_time = "Unknown"

        try:
            furthest_result_time = current_results_page.posts[-1].timestamp.strftime(datetime_format_string)
        except AttributeError:
            furthest_result_time = "Unknown"

        print "Grabbed new results page from %s to %s. Only %s days left to go." % (
            soonest_result_time,
            furthest_result_time,
            time_to_go.days
        )
        # print current_results_page.older_link
        for post in current_results_page.posts:
            post.save_to_db()

        while datetime.datetime.now(tz=pytz.utc) < last_page_get_datetime + datetime.timedelta(
                seconds=download_offset_in_seconds):
            pass

        if not current_results_page.older_link:
            break
        else:
            current_results_page = ResultsPage(current_results_page.older_link)
            last_page_get_datetime = datetime.datetime.now(tz=pytz.utc)

    print "Finished Scraping!"
