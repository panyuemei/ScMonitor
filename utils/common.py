import re


absolute_http_url_regexp = re.compile(r"^https?://", re.I)

def build_url(base_url, url, raise_exception=None):
    if absolute_http_url_regexp.match(url):
        return url
    elif base_url:
        return "{}/{}".format(base_url.rstrip("/"), url.lstrip("/"))
    else:
        if raise_exception:
            raise raise_exception(f'请求地址有误，请检查是否正确：base_url={base_url}, url={url}')
        return None
