from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import CrawlerHelper
from utils.utils import map_eams_status

if __name__ == "__main__":
    crawler_helper = CrawlerHelper()
    raw_table_content = (
        crawler_helper
        .set_chrome_helper(ChromeHelper())
        .login()
        .go_to_wo_tracking_page()
        .search_wo("5000138669")
    )
    wo_status = map_eams_status(raw_table_content)
    print(f"{wo_status=}")
