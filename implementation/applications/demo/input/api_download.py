def api_download(api):
    name = 'LearningWithPython.pdf'
    link = 'https://wiki.python.org.br/DocumentacaoPython?action=AttachFile&do=get&target=thinkcspy.pdf'
    api.download(link, name)
