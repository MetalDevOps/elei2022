from httpx import (
    Client,
    HTTPError,
    HTTPStatusError,
    InvalidURL,
    NetworkError,
    ReadTimeout,
    RequestError,
    StreamError,
    TimeoutException,
    TooManyRedirects,
)
from json import JSONDecodeError
from time import sleep


from logger import get_logger


log = get_logger(__name__)


class MakeRequest:
    def __init__(self):
        self.session = Client()
        # self.session = Session()
        self.max_retries = 3
        self.sleep_between_retries = 1
        self.tries = 0

    def request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        # response = self.session.request(method, url, **kwargs)
        while self.tries < self.max_retries:
            try:
                response.raise_for_status()
                if response.status_code == 200 or 201:
                    log.info(f"{method} {url}")
                    log.info(f"Requisição <<{method}>> realizada com sucesso, status code: {response.status_code}")
                    return response
                else:
                    continue
            except (
                HTTPError,
                NetworkError,
                RequestError,
                InvalidURL,
                StreamError,
                TimeoutException,
                TooManyRedirects,
                HTTPStatusError,
                ReadTimeout,
                TimeoutError,
                JSONDecodeError
            ) as e:
                log.error(str(e))
                self.tries += 1
                log.warning(f"Tentando novamente, {self.tries}/{self.max_retries}")
                sleep(self.sleep_between_retries)
                if self.tries == self.max_retries:
                    log.critical(f"Critical error: {e}, saindo...")
                    raise SystemExit(e)
                continue
        return response
