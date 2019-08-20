def api_save_json(api):
    links = dict(
        cederj='http://cederj.edu.br/fundacao/',
        proderj='http://www.proderj.rj.gov.br/',
    )
    api.save_json(links)
