import logging
import numpy as np

logger = logging.getLogger(__name__)

class ScanTail():

    def __init__(self, array, init, qlog = None):

        self.configLogger(qlog)

        self.cursor = init

        self.tailsize = np.fromstring(array[self.cursor:self.cursor+4], dtype=np.int32)
        self.cursor += 281
        # lmark = array[self.cursor]
        # self.cursor +=1
        dirsize = np.fromstring(array[self.cursor:self.cursor+4], dtype=np.int32)
        self.cursor +=5

        self.vars = dict()

        for infodir in range(0, dirsize[0]):
            key, value = self.getDirEntry(array)
            self.vars[key] = value
            # print ('\tInfodir key [{}] is [{}]'.format(key, value))


    def getDirEntry(self, array):

        lsize = array[self.cursor] # np.fromstring(array[cursor:cursor+4], dtype=np.int32)
        self.cursor +=1
        key = str(array[self.cursor:self.cursor+lsize], "utf-8")
        self.cursor +=lsize
        rmark = array[self.cursor]
        self.cursor +=1
        rsize = array[self.cursor]
        self.cursor +=1

        if key =='ChipNo' or key=='IntegrationTime' or key=='LightPath':
            value = int(str(array[self.cursor:self.cursor+rsize], "utf-8"))
        elif key =='ChipOrientationReversed':
            temp = str(array[self.cursor:self.cursor+rsize], "utf-8")
            value = False if temp=="False" else True
        else:
            value = str(array[self.cursor:self.cursor+rsize], "utf-8")

        self.cursor +=rsize+1



        return key, value




    def configLogger(self, qlog):
        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)





