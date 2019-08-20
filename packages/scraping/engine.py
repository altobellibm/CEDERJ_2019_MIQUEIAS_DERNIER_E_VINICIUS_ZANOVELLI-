import os
import sys
import platform
import datetime
import math
import importlib

from .logger import VerboseLogger
from .facade import API

__all__ = ['Bot']


class Bot(object):

    def __init__(self, params):

        # simple parse initialization parameters
        self.__caller = sys.argv[0]
        self.__parser = params['parser']
        self.__charset = params['charset']
        self.__verbose = params['verbose']
        self.__debug = params['debug']
        self.__fs = params['filesystem']
        self.__timestamp = datetime.datetime.now()
        self.__drivers = dict()
        self.__logger = None

        # resolve/create paths and convert "relative" ones to "absolute"
        for path in self.__fs:
            if type(self.__fs[path]) is dict:
                for driver in self.__fs[path]:
                    self.__drivers[driver] = self.__relative_to_absolute_path(self.__fs[path][driver])
            else:
                if path != 'output':
                    self.__fs[path] = self.__relative_to_absolute_path(self.__fs[path])
                else:
                    # set output path based on date/time
                    date = self.__timestamp.strftime("%Y/%m/%d")
                    self.__fs[path] = os.path.abspath(os.path.join(
                        self.__relative_to_absolute_path(self.__fs[path]), *date.split('/')
                    ))
                if not os.path.isdir(self.__fs[path]):
                    os.makedirs(self.__fs[path])

        # add input directory to system "PATH"
        sys.path.append(self.__fs['input'])

        self.__logger = VerboseLogger('__scraping', self.__fs['logs'], self.__charset, self.__verbose, self.__debug)
        self.__set_drivers_for_os()
        pass  # __init__

    def __relative_to_absolute_path(self, path):

        # work with slashes instead of backslashes
        sep = '/'
        dir = path.replace('\\', sep)

        if dir[:1] == '.':  # if path is indeed relative

            # do the "conversion"
            basedir = os.path.abspath((os.path.dirname(self.__caller)))
            dir = os.path.abspath(os.path.join(basedir, *dir.split(sep)))
            # print('%s converted to %s' % (path, dir))  # used for dev debugging

        return dir

    def __set_drivers_for_os(self):

        # get OS name
        plat = platform.system().lower()
        os_name = 'win' if 'windows' in plat or 'nt' in plat else 'linux'
        if 'darwin' in plat:
            os_name = 'mac'

        # address the appropriate driver according to OS and architecture
        for driver in self.__drivers:

            #  get OS architecture (must be inside drivers loop due to support variations)
            os_arch = None

            if os_name == 'mac':
                # Mac currently only has support for 64-bit versions (for both drivers)
                os_arch = 64
            else:

                if driver == 'chromedriver':
                    # Chrome currently supports only 64-bit for Linux and 32-bit for Windows
                    os_arch = 64 if os_name == 'linux' else 32

                elif driver == 'geckodriver':
                    # Mozilla supports 32 and 64-bit versions for both (Linux and Windows)
                    os_arch = 64 if (sys.maxsize > 2 ** 32) else 32

                else:
                    # no other drivers are supported for now
                    self.__drivers[driver] = ''

            # set the driver binary path
            bin_file_name = driver + '.exe' if os_name == 'win' else driver
            bin_file_path = os.path.join(self.__drivers[driver], os_name + str(os_arch), bin_file_name)
            if os.path.isfile(bin_file_path):
                self.__drivers[driver] = bin_file_path

        del self.__fs['drivers']
        pass  # __set_drivers_for_os

    def log(self, message, level='info'):
        self.__logger.log(message, level)
        return self

    def debug(self, message):
        self.log(message, 'debug')
        return self

    def run(self):

        # start engine (and input var scripts) execution
        start_time = datetime.datetime.now()

        self.log('***** Scraping started - %s *****' % start_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.debug('-> Input path: %s' % self.__fs['input'])
        self.debug('-> Output path: %s' % self.__fs['output'])
        self.debug('-> Logs path: %s' % self.__fs['logs'])
        self.debug('-> Chromedriver: %s' % self.__drivers['chromedriver'])
        self.debug('-> Geckodriver: %s' % self.__drivers['geckodriver'])
        self.debug('-> Parser: %s' % self.__parser)
        self.debug('-> Charset: %s' % self.__charset)

        # get input vars (scripts) list
        scripts = [
            entry for entry in os.listdir(self.__fs['input'])
            if os.path.isfile(os.path.join(self.__fs['input'], entry)) and entry[-3:] == '.py'
        ]

        self.debug('-> Scripts found: %s' % str([f.split('.')[0] for f in scripts]))
        counter = 0

        # loop through all input var scripts
        for filename in scripts:
            if filename[:2] != '__':  # and filename[-3:] == '.py':  # redundant
                script = os.path.splitext(filename)[0]  # file name without extension
                counter += 1

                self.log('==> Executing input var script: "%s"' % script)
                script_time = datetime.datetime.now()

                # import input var script as a module
                module = importlib.import_module(script)

                # check if the input var script has a (trigger) method named after its file
                if hasattr(module, script):

                    # get the input var script trigger method
                    trigger = getattr(module, script)

                    # instantiate the scraping (facade) api
                    api = API(script, self.__fs, self.__charset, self.__parser, self.__drivers,
                              self.__timestamp, self.__verbose, self.__debug)

                    try:
                        # call the input var script trigger injecting the API instance
                        trigger(api)

                    except Exception as e:
                        # catch generic exceptions from the input var script
                        self.log('The "%s" script raised the following exception: %s'
                                 % (script, str(e)), 'error')

                    # logging results
                    delta_time = datetime.datetime.now() - script_time
                    elapsed_time = str(math.ceil(delta_time.total_seconds()))
                    self.log('==> Script "%s" executed in %s second(s)' % (script, elapsed_time))

                else:
                    self.log('Script "%s" must have the "%s(api)" method' % (script, script), 'error')
            else:
                self.debug('Ignoring file "%s" (reason: begins with "__")' % filename)

        # catch no input var scripts case
        if counter == 0:
            self.log('No input var scripts found in %s' % self.__fs['input'], 'warning')

        # just the end
        delta_time = datetime.datetime.now() - start_time
        elapsed_time = str(math.ceil(delta_time.total_seconds()))
        self.log('***** Scraping finished in %s second(s) *****' % elapsed_time)

        if self.__verbose:
            print('\t-> Check the logs in path: %s' % self.__fs['logs'])
            print('\t-> Find the output in path: %s' % self.__fs['output'])

        return self
