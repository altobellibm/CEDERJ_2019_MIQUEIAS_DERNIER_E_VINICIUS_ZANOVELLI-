import os
import sys
import platform
import datetime
import math
import importlib
import json

from .logger import VerboseLogger
from .facade import API

__all__ = ['Bot','trigger']


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
        self.__settings = params['settings']
        self.__sources = dict()
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
                if not os.path.isdir(self.__fs[path]) and not os.path.isfile(self.__fs[path]):
                    os.makedirs(self.__fs[path])

        # add sources directory to system "PATH"
        sys.path.append(self.__fs['sources'])

        self.__logger = VerboseLogger('__scraping', self.__fs['logs'], self.__charset, self.__verbose, self.__debug)
        self.__load_sources(self.__relative_to_absolute_path(self.__settings))
        self.__set_drivers_for_os()

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

    def __load_sources(self, filename):
        with open(filename,encoding="utf-8") as json_file:
            data = json.load(json_file)
            for source in data:
                self.__sources[source] = {}
                for key in data[source]:
                    self.__sources[source][key] = {}
                    self.__sources[source][key] = data[source][key]

    def get_sources(self):
        return self.__sources

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

# QUESTIONS: what's the idea behind double nesting this piece of code out of its scope and what means "dec(f)"?
# SUGGESTION: -> reduce complexity and make the code more cohesive (Closure, SRP, Low Coupling, Encapsulation) 
               # by removing redundant nestings and sticking to more clear names
def trigger(script):
    def dec(f):
        def method(self):
            # start engine (and input var scripts) execution
            start_time = datetime.datetime.now()

            self.log('***** Scraping started - %s *****' % start_time.strftime("%Y-%m-%d %H:%M:%S"))
            self.debug('-> Sources modules path: %s' % self._Bot__fs['sources'])
            self.debug('-> Output path: %s' % self._Bot__fs['output'])
            self.debug('-> Logs path: %s' % self._Bot__fs['logs'])
            self.debug('-> Chromedriver: %s' % self._Bot__drivers['chromedriver'])
            self.debug('-> Geckodriver: %s' % self._Bot__drivers['geckodriver'])
            self.debug('-> Parser: %s' % self._Bot__parser)
            self.debug('-> Charset: %s' % self._Bot__charset)

            self.log('==> Executing source module script: "%s"' % script)
            script_time = datetime.datetime.now()

            ret = None

            # instantiate the scraping (facade) api
            api = API(script, self._Bot__fs, self._Bot__charset, self._Bot__parser, self._Bot__drivers,
                self._Bot__timestamp, self._Bot__verbose, self._Bot__debug)


            try:
                # call the input var script trigger injecting the API instance
                ret = f(self, api)

            except Exception as e:
                # catch generic exceptions from the input var script
                self.log('The "%s" script raised the following exception: %s'
                            % (script, str(e)), 'error')

            # logging results
            delta_time = datetime.datetime.now() - script_time
            elapsed_time = str(math.ceil(delta_time.total_seconds()))
            self.log('==> Script "%s" executed in %s second(s)' % (script, elapsed_time))

            # catch no input var scripts case

            # just the end
            delta_time = datetime.datetime.now() - start_time
            elapsed_time = str(math.ceil(delta_time.total_seconds()))
            self.log('***** Scraping finished in %s second(s) *****' % elapsed_time)

            if self._Bot__verbose:
                print('\t-> Check the logs in path: %s' % self._Bot__fs['logs'])
                print('\t-> Find the output in path: %s' % self._Bot__fs['output'])

            return ret
        return method
    return dec
