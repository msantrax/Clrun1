import logging
import numpy as np

from ScanTail import ScanTail

logger = logging.getLogger(__name__)

class Scan():

    def __init__(self, array, scan_num, scaninit, qlog = None):

        self.configLogger(qlog)

        self.scantype = array[scaninit]
        self.scan_num = scan_num
        self.cursor = scaninit+1

        if self.scantype == 0x07:
            self.cursor +=38

        # First get the header
        headertype = np.dtype([
            ("scantag", np.int32),
            ("blocksize", np.int32),
            ("tk1", 'b'),
            ("pixel_num", np.int32),
        ])
        self.scanheader = np.fromstring(array[self.cursor:self.cursor+headertype.itemsize], dtype=headertype)
        scanbegin = self.cursor

        # print("Scan : {} --> Scaninit @ {} - Scantype is {:x} - ID is {} - {} pixels".format(
        #     scan_num, self.cursor, self.scantype,
        #     self.scanheader['scantag'], self.scanheader['pixel_num'][0]))

        self.cursor += headertype.itemsize;
        self.scantail_init = self.cursor + self.scanheader['blocksize'][0] + 1

        pnum = '(' + str(self.scanheader['pixel_num'][0]) + ', 2)f8'
        pixeltype = np.dtype([("pixelrows", pnum)])
        self.scanrows = np.fromstring(array[self.cursor:self.cursor+pixeltype.itemsize], dtype=pixeltype)

        self.tailsize = np.fromstring(array[self.scantail_init:self.scantail_init+4], dtype=np.int32)
        self.scantail = ScanTail(array, self.scantail_init)

        scanvars = self.scantail.vars
        scanvars['ScanNumber'] = scan_num
        scanvars['ScanType'] = self.scantype
        scanvars['ScanID'] = self.scanheader['scantag']
        scanvars['ScanSize'] = self.scanheader['pixel_num'][0]
        scanvars['ScanBegin'] = scanbegin
        scanvars['PayloadInit'] = self.cursor
        scanvars['PayloadSize'] = self.scanheader['blocksize'][0]
        scanvars['TailDataInit'] = self.scantail_init
        scanvars['TailDataSize'] = self.tailsize

        # print ('Payload init @ {} - Payload size is {} - TailData init @ {} - TailData size is {}'.format(
        #     self.cursor,self.scanheader['blocksize'][0], self.scantail_init, self.tailsize
        # ))

        self.cursor = self.scantail_init+self.tailsize[0]+5
        # print ('Scan end @ {}\n'.format(self.cursor))

        scanvars['ScanEnd'] = self.cursor
        scanvars['ScanRows'] = self.scanrows




    def configLogger(self, qlog):
        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
