import sys
from scraping import engine as microframework

# SUGGESTION: -> dependencies could be handled by the package/engine
               # no need to manually import each one (consider managing hundreds of sources)
#   - Allows new sources to be included without requiring changing the code (consider having hundreds of sources)
#   - Follows good principles such as Encapsulation, SRP and Low Coupling
#   - Reduces complexity and lines of codes in main app avoiding code repetition
#   - More maintainable (consider updating hundreds of sources)
from sources.drugbank import drugbank
from sources.merck import merck

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
    @microframework.trigger('merck')
    def merck(self, api):
        return merck(api, scrapper.get_sources())


scrapper = Pharmaceutical(dict(
    charset='utf-8',
    parser='html5lib',  # html5lib | lxml | html.parser
    settings='./sources/settings.json',
    filesystem=dict(
        sources='./sources/',
        output='./output/',
        logs='./logs/',
        drivers=dict(
            geckodriver='../../vendor/geckodriver/0.24.0/',             # Firefox 65+
            chromedriver='../../vendor/chromedriver/78.0.3904.70/',     # Chrome 78
        ),
    ),
    verbose=True,
    debug=False,
))

def run_source_script(source_name, scrapper):
    if hasattr(scrapper, source_name):
        module = getattr(scrapper, source_name)
        scrapper.log('Starting "%s" source module script' % source_name)
        module()
    else:
        scrapper.log('Source "%s" not found or not enabled' % (source_name), 'error')

if __name__ == "__main__":

    params = sys.argv[1:]
    sources = scrapper.get_sources()['sources']

    if len(params) > 0:
        for source in params:               # order matters here (first checking params and then the sources list)
            if source.lower() in sources:   # considering params first so execution order is delegated to command line
                run_source_script(source.lower(), scrapper)
            else:
                scrapper.log('Source script "%s" not found' % (source.lower()), 'warning')
    else:
        for source in sources:              # run all scripts
            run_source_script(source.lower(), scrapper)
