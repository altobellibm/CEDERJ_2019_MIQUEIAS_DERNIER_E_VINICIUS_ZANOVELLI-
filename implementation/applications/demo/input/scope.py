HELLO_WORLD = 'Hello World'


class HelloWorld(object):
    def __init__(self):
        self.message = 'Hello World'
        pass

    def hello_world(self):
        return self.message


def hello_world():
    return 'Hello World'


# @trigger
def scope(api):
    instance = HelloWorld()
    api.log('There are no scoping limitations')
    api.log('"%s" from outer scope variable' % HELLO_WORLD)
    api.log('"%s" from outer scope function' % hello_world())
    api.log('"%s" from outer scope class instance' % instance.hello_world())
