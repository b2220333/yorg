'''This module provides functionalities for font managing.'''


class FontMgr(object):
    '''This class models the font manager.'''

    def __init__(self, eng):
        self.__fonts = {}
        self.__eng = eng

    def load_font(self, path):
        '''Loads a font.'''
        if path not in self.__fonts:
            self.__fonts[path] = self.__eng.loader.loadFont(path)
            self.__fonts[path].setPixelsPerUnit(60)
            self.__fonts[path].setOutline((0, 0, 0, 1), .8, .2)
        return self.__fonts[path]
