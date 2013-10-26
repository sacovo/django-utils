
class NavigationPoint(object):
    name = ''
    link = ''
    subsites = []

    def __init__(self, name, link='', subsites=[]):
        self.name = name
        self.link = link
        self.subsites = subsites


