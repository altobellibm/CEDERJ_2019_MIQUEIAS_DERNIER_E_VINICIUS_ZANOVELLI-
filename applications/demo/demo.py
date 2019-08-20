from scraping import engine as microframework

scrap = microframework.Bot(dict(
    charset='utf-8',
    parser='html5lib',  # html5lib | lxml | html.parser
    filesystem=dict(
        input='./input/',
        output='./output/',
        logs='./logs/',
        drivers=dict(
            geckodriver='../../vendor/geckodriver/0.24.0/',  # Firefox 65+
            chromedriver='../../vendor/chromedriver/76.0.3809.68/',  # Chrome 76
            # chromedriver='../../vendor/chromedriver/77.0.3865.10/',   # Chrome 77
            # safaridriver='',  # no support for Safari at this time
            # msdriver='',      # no support for Edge at this time
        ),
    ),
    verbose=True,
    debug=False,
))

if __name__ == "__main__":
    scrap \
        .log('=======================================================') \
        .run() \
        .log('=======================================================')
