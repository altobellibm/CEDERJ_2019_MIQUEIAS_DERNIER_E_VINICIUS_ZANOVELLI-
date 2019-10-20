import os
import re
import datetime
import math
import json

import requests
import requests.exceptions

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from .logger import VerboseLogger
from .logger import LOG_FILE_EXTENSION
from .drivers import Drivers

__all__ = ['API']


class API(Drivers):
    __RESPONSE_SAMPLE_LENGTH = 60

    def __init__(self, script, fs, charset, parser, drivers, timestamp, verbose=True, debug=False):
        super().__init__()
        self.__logger = VerboseLogger(script, fs['logs'], charset, verbose, debug)
        self.__script = script
        self.__fs = fs
        self.__charset = charset
        self.__parser = parser
        self.__drivers = drivers
        self.__timestamp = timestamp
        self.__verbose = verbose
        self.__debug = debug
        self.__export_file = os.path.abspath(os.path.join(
            self.__fs['output'], self.__script
        ))
        self.response = None
        pass  # __init__

    def __bs4(self, data):
        self.debug('BeautifulSoup4 instance created: %s...' % str(data)[:API.__RESPONSE_SAMPLE_LENGTH])
        return BeautifulSoup(str(data), self.__parser)

    def __browser(self, browser_name, headless=False, options=None):
        browser = None

        # get browser driver binary path
        driver = self.availableDrivers[browser_name.lower()].lower()
        binary = self.__drivers[driver]

        # expose only supported drivers
        if not hasattr(self, driver):
            self.log('Driver "%s" not found or not supported' % driver, 'error')
        else:

            # create browser instance through drivers inheritance
            instance = getattr(self, driver)
            if callable(instance):
                log = os.path.abspath(os.path.join(self.__fs['logs'], '__' + driver + LOG_FILE_EXTENSION))
                browser = instance(binary, log, headless, options)
                headless = 'headless ' if headless else ''
                self.debug('New %sinstance of "%s" created' % (headless, browser_name))
                self.debug('Driver options: %s' % str(options))

        # return a new selenium browser driver instance or None
        return browser

    def start_browser(self, browser_name='Firefox', options=None):
        return self.__browser(browser_name, False, options)

    def headless_browser(self, browser_name='Firefox', options=None):
        return self.__browser(browser_name, True, options)

    def render(self, url, el_selector='*', timeout=30, browser_name='Firefox', options=None):
        data = None

        self.log('Rendering "%s" using "%s" (timeout=%d sec(s))' %
                 (el_selector, browser_name, timeout))
        self.debug('Driver options: %s' % str(options))
        self.log('GET %s' % url)

        # start a headless browser
        browser = self.headless_browser(browser_name, options)

        try:
            # get the response and close the browser
            browser.set_page_load_timeout(timeout)
            wait = WebDriverWait(browser, timeout)
            browser.get(url)
            if el_selector != '*':
                wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, el_selector)))
            data = browser.page_source
            self.debug('Response sample: %s' % str(data)[:API.__RESPONSE_SAMPLE_LENGTH])

        # catching just in case (not sure if drivers' .get methods throw exceptions)
        except Exception as e:
            self.log('Error trying to render %s using "%s": %s' % (url, browser_name, str(e)))

        # terminate browser/driver instance and return a BeautifulSoup4 instance
        browser.quit()
        return data if data is None else self.__bs4(data)

    def get(self, url, params=None, headers=None):

        bs4 = None
        params = [] if params is None else params
        headers = [] if headers is None else headers

        self.log('GET %s' % url)
        self.debug('PARAMETERS: %s' % str(params))
        self.debug('HEADERS: %s' % str(headers))

        try:
            # simple HTTP(S) GET request
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            self.response = response

        # catch exceptions
        except requests.exceptions.HTTPError as e:
            self.log('HTTP(S) error: %s' % str(e), 'error')
        except Exception as e:
            self.log('GET error: %s' % str(e), 'error')
        else:

            # handle GET response
            self.debug('%s GET %s' % (str(response.status_code), url))
            if response.status_code == 200:
                self.debug('Response sample: %s' % str(response.content)[:API.__RESPONSE_SAMPLE_LENGTH])
                response.encoding = self.__charset
                bs4 = self.__bs4(response.text)

        return bs4

    def post(self, url, payload, headers=None):

        bs4 = None
        payload = [] if payload is None else payload
        headers = [] if headers is None else headers

        self.log('POST %s' % url)
        self.debug('PAYLOAD: %s' % str(payload))
        self.debug('HEADERS: %s' % str(headers))

        try:
            # simple HTTP(S) POST request
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()

        # catch exceptions
        except requests.exceptions.HTTPError as e:
            self.log('HTTP(S) error: %s' % str(e), 'error')
        except Exception as e:
            self.log('POST error: %s' % str(e), 'error')
        else:

            # handle POST response
            self.debug('%s POST %s' % (str(response.status_code), url))
            if response.status_code == 200:
                self.debug('Response sample: %s' % str(response.content)[:API.__RESPONSE_SAMPLE_LENGTH])
                response.encoding = self.__charset
                bs4 = self.__bs4(response.content)

        return bs4

    def generic_save(self, data, save, file_name='', extension='json'):
        has_failed = False

        # building a very likely unique file name (no need to be too strict)
        file = file_name or self.__export_file + self.__timestamp.strftime("-%H_%M_%S-%f")+'.'+extension

        self.debug('Saving %s data to file: %s' % (extension, file))
        self.debug('Data sample: %s' % str(data)[:API.__RESPONSE_SAMPLE_LENGTH])

        try:
            save(file, data)
            self.log('%s data saved to file: %s' % (extension, file))

        # catching errors
        except Exception as e:
            self.log('Saving %s data to file %s has failed: %s' % (extension, file, str(e)), 'error')
            has_failed = True

        # considering (no errors raised) and (target file exists) = success
        if (not has_failed) and os.path.isfile(file):
            return file
        return ''


    def save_json(self, data, file_name=''):
        def save(file_name, data):
            with open(file_name, 'a', encoding=self.__charset) as json_file:
                # simply dumping the data (in json format) to file
                json_data = json.dumps(data, ensure_ascii=True)
                json_file.write(json_data)
                json_file.close()
        
        return self.generic_save(data, save, file_name=file_name, extension='json')


    def save_csv(self, data, file_name=''):
        def save(file_name, data):
            data.to_csv(file_name, sep=';', index=False)
        
        return self.generic_save(data, save, file_name=file_name, extension='csv')



    def download(self, url, filename, overwrite=True, params=None, headers=None, stream=False, chunk_bytes=524288):
        has_failed = False

        params = [] if params is None else params
        headers = [] if headers is None else headers

        # make sure we have a valid file name
        filename = str(filename).strip().replace(' ', '_')
        file = self.__export_file + self.__timestamp.strftime("-%H_%M_%S-%f-")
        file += re.sub(r'(?u)[^-\w.]', '', filename)

        self.log('Downloading from: %s' % url)
        self.log('Downloading to: %s' % file)

        # overwrite target file when applicable
        if os.path.isfile(file) and overwrite:
            self.debug('Removing file %s...' % file)
            os.remove(file)

        # if file exists and was not overwritten then abort
        if os.path.isfile(file):
            self.log('Can\'t download the file without overwriting', 'warning')
            has_failed = True

        else:
            timer = datetime.datetime.now()
            try:

                # simple HTTP(S) GET request
                response = requests.get(url, params=params, headers=headers, stream=stream)
                response.raise_for_status()

            # catch HTTP(S) exceptions
            except requests.exceptions.HTTPError as e:
                has_failed = True
                self.log('HTTP(S) error: %s' % str(e), 'error')
            except Exception as e:
                has_failed = True
                self.log('GET error: %s' % str(e), 'error')
            else:

                # handle GET response
                self.debug('%s GET %s' % (str(response.status_code), url))
                if response.status_code != 200:
                    self.log('Download has failed with status code: %s' % str(response.status_code), 'error')
                else:
                    try:
                        with open(file, 'wb') as output_file:

                            # write bytes to target file
                            for chunk in response.iter_content(chunk_bytes, True):
                                output_file.write(chunk)
                            output_file.close()

                            # logging results
                            delta_time = datetime.datetime.now() - timer
                            elapsed_time = str(math.ceil(delta_time.total_seconds()))
                            self.log('File downloaded in %s second(s)' % elapsed_time)

                    # catch file writing exceptions
                    except Exception as e:
                        has_failed = True
                        self.log('Download has failed with error(s): %s' % str(e), 'error')

        # considering (no errors raised) and (target file exists) = success
        return (not has_failed) and os.path.isfile(file)

    def log(self, message, level='info'):
        self.__logger.log(message, level)
        return self

    def debug(self, message):
        self.log(message, 'debug')
        return self
