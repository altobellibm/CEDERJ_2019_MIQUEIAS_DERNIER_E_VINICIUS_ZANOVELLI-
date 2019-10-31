from scraping import engine as microframework

# SUGGESTION: -> dependencies could be handled by the package/engine
               # no need to manually import each one (consider managing hundreds of sources)
#   - Allows new sources to be included without requiring changing the code (consider having hundreds of sources)
#   - Follows good principles such as Encapsulation, SRP and Low Coupling
#   - Reduces complexity and lines of codes in main app avoiding code repetition
#   - More maintainable (consider updating hundreds of sources)
from sources.drugbank import drugbank
from sources.merckmillipore import merckmillipore

class Pharmaceutical(microframework.Bot):

    @microframework.trigger('drugbank')
    def drugbank(self, api):
        return drugbank(api, scrapper.get_sources())

# SUGGESTION: -> sources could be valid when both exist, a module file and a record in JSON settings
               # no need to explicitly define each trigger (consider managing hundreds of sources)
#   - Allows new sources to be included without requiring changing the code (consider having hundreds of sources)
#   - Follows good principles such as Encapsulation, SRP, and DRY
#   - Reduces complexity and lines of codes in main app avoiding code repetition
#   - More maintainable (consider updating hundreds of sources)
    @microframework.trigger('merckmillipore')
    def merckmillipore(self, api):
        return merckmillipore(api, scrapper.get_sources())


scrapper = Pharmaceutical(dict(
    charset='utf-8',
    parser='html5lib',  # html5lib | lxml | html.parser
    settings='./settings.json',
    filesystem=dict(
        sources='./sources/',
        output='./output/',
        logs='./logs/',
        drivers=dict(
            geckodriver='../../vendor/geckodriver/0.24.0/',             # Firefox 65+
            chromedriver='../../vendor/chromedriver/76.0.3809.68/',     # Chrome 76
            # chromedriver='../../vendor/chromedriver/77.0.3865.10/',   # Chrome 77
            # safaridriver='',  # no support for Safari at this time
            # msdriver='',      # no support for Edge at this time
        ),
    ),
    verbose=True,
    debug=False,
))

if __name__ == "__main__":

# SUGGESTION: -> sources triggers should be automatic based on a loop through all sources with settings
            # no need to manually trigger each one (consider managing hundreds of sources)
#   - Allows new sources to be included without requiring changing the code (consider having hundreds of sources)
#   - Follows good principles such as Encapsulation and DRY
#   - Reduces complexity and lines of codes in main app avoiding code repetition
#   - More maintainable (consider updating hundreds of sources)
    try:
        scrapper.drugbank()
    except:
        scrapper.log('Source module "%s" not found' % ("drugbank"), 'error')
    try:
        scrapper.merckmillipore()
    except:
        scrapper.log('Source module "%s" not found' % ("merckmillipore"), 'error')
