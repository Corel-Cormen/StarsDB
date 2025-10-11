import requests
from typing import Tuple

from WebRequester.WebRequesterInterface import WebRequesterInterface, ReqStatus


class WebRequester(WebRequesterInterface):

    __MAX_REQ_DEBOUNCE = 3

    def getHTML(self, url: str) -> Tuple[ReqStatus, str]:
        html = ""

        reqDebouncing = 0
        while(reqDebouncing != self.__MAX_REQ_DEBOUNCE):
            try:
                response = requests.get(url)
                break
            except KeyboardInterrupt:
                raise
            except:
                print("Request timeout")
                reqDebouncing += 1

        if response.status_code == 200:
            html = response.text
            status = ReqStatus.OK
        elif response.status_code == 500:
            status = ReqStatus.NOT_EXIST
        else:
            status = ReqStatus.ERROR

        print(f"Request: {url} | code: {response.status_code}")

        return (status, html)
