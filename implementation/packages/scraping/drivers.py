import sys
import os

import selenium.webdriver as webdriver
import selenium.common.exceptions as exceptions

__all__ = ['Drivers']


class Drivers(object):
    __ERR_MSG = '[FAIL] Driver error -> '
    __HALT_MSG = 'Execution aborted, please try again'
    __HEADLESS_FLAG = '--headless'

    def __init__(self):
        self.availableDrivers = dict(
            firefox='geckodriver',
            chrome='chromedriver',
            # safari='safaridriver',    # not supported at this time
            # edge='msdriver',          # not supported at this time
        )
        pass

    @staticmethod
    def geckodriver(bin, log, headless=False, params=None):
        # https://github.com/mozilla/geckodriver/releases (Aug 2019)

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.privatebrowsing.autostart", True)
        profile.set_preference("accept_untrusted_certs", True)

        options = webdriver.FirefoxOptions()

        if params is not None:
            for param in params:
                if param != Drivers.__HEADLESS_FLAG:
                    options.add_argument(param)

        if headless:
            os.environ['MOZ_HEADLESS'] = '1'
            options.add_argument(Drivers.__HEADLESS_FLAG)
        else:
            if hasattr(os.environ, 'MOZ_HEADLESS'):
                del os.environ['MOZ_HEADLESS']

        try:
            return \
                webdriver.Firefox(
                    executable_path=bin,
                    service_log_path=log,
                    firefox_options=options,
                    firefox_profile=profile
                )
        except exceptions.WebDriverException as e:
            Drivers.__halt(e)
        except Exception as e:
            Drivers.__halt(e)

    @staticmethod
    def chromedriver(bin, log, headless=False, params=None):
        # https://sites.google.com/a/chromium.org/chromedriver/downloads (Aug 2019)

        args = ['--log-path=' + log]
        options = webdriver.ChromeOptions()

        if params is not None:
            for param in params:
                if param != Drivers.__HEADLESS_FLAG:
                    options.add_argument(param)

        if headless:
            options.add_argument(Drivers.__HEADLESS_FLAG)
            options.add_argument('--disable-gpu')
        # else:
            # options.add_argument('--start-maximized')

        options.add_argument("--log-level=3")
        options.add_argument('--disable-extensions')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--incognito')
        options.add_argument('test-type')
        options.add_argument('no-sandbox')

        try:
            return \
                webdriver.Chrome(
                    executable_path=bin,
                    service_args=args,
                    chrome_options=options
                )
        except exceptions.WebDriverException as e:
            Drivers.__halt(e)
        except Exception as e:
            Drivers.__halt(e)

    # @staticmethod
    # def safaridriver(bin, log, headless=False, init_params=None):
    # https://webkit.org/blog/6900/webdriver-support-in-safari-10/ (Aug 2019)
    # pass

    # @staticmethod
    # def msdriver(bin, log, headless=False, init_params=None):
    # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ (Aug 2019)
    # pass

    @staticmethod
    def __halt(err):
        sys.exit('%s%s\n%s' % (Drivers.__ERR_MSG, str(err), Drivers.__HALT_MSG))
