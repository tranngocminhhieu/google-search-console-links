# Google Search Console Links (GSCLinks)
![PyPI](https://img.shields.io/pypi/v/gsclinks) ![PyPI - Downloads](https://img.shields.io/pypi/dm/gsclinks) ![GitHub](https://img.shields.io/github/license/tranngocminhhieu/google-search-console-links)


Website administrators and SEOers will often monitor backlink data to know which websites are linking to their websites. From there, they can filter out bad backlinks to send to Google Disavow Links. This will help their website not be affected by bad backlinks and keep a good position on Google Search.

This package will help you scrape backlink data from Google Search Console with cookies.

![GSC](images/thumb.jpg?raw=true)

## Installation
GSCLinks is available on PyPI. You can install it through pip:
```commandline
pip install gsclinks
```

## Usage
### Get raw cookie
**Method 1:** Open Chrome Developer Tool (F12), then go to Network tab, then visit Google Search Console, and then copy the Cookie's value in Request Header.

![Cookie value in F12](https://github.com/tranngocminhhieu/google-search-console-links/blob/main/images/cookie-value-f12.png?raw=true)

**Method 2:** Use [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) extension on Chrome, visit Google Search Console, then open Cookie-Editor, and then export cookie as JSON.

![Cookie value in Cookie-Editor](https://github.com/tranngocminhhieu/google-search-console-links/blob/main/images/cookie-editor.png?raw=true)

Save the raw cookie in text file, such as `cookie.txt`.

### Import packages and set variables
Import packages:
```python
from gsclinks import parse_raw_cookie, SearchConsoleLinks
```

Set variables:
- `resource_id`: It can be `https://your-domain.com/` or `your-domain.com`. It depends on how you add the property to Google Search Console.
- `user_number`: If you're signed in to more than 1 Gmail on Chrome, enter the number you see in URL when you visit Google Search Console *(search.google.com/u/`user_number`/...)*, otherwise enter `None`.

```python
cookies = parse_raw_cookie(cookie_file='cookie.txt')
resource_id = 'https://your-domain.com' # or maybe your-domain.com
user_number = None # or maybe 0, 1, 2, ...
console = SearchConsoleLinks(cookies=cookies, resource_id=resource_id, user_number=user_number)
```

### Get backlink data
If you want the entire backlink data in a simple way then use this method.
```python
backlinks = console.get_all_links(sleep=10)
# sleep: time to rest between each request sending (seconds).
```

You can get backlink data step by step to be able to intervene in the process. For example, you may want to remove some sites that you no longer need to get data.
```python
# Get sites
sites = console.get_sites()

# Get all target pages
all_target_pages = console.get_all_target_pages(sites=sites, sleep=5)

# Get all linking pages
all_linking_pages = console.get_all_linking_pages(all_target_pages=all_target_pages, sleep=5)
```

