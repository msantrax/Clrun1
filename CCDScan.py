import logging
import numpy as np
import pandas as pd

from Scan import Scan


logger = logging.getLogger(__name__)

class CCDScan():

    def __init__(self, scanfile, payload, config, qlog = None):

        self.configLogger(qlog)

        self.cursor = 0
        self.df = None



        if payload is None :
            self.scanpath = config['scanpath'] + scanfile
            with open(self.scanpath, 'r+b') as f:
                s = f.read()
                self.scanfile = scanfile
                print("Processing File [{}] --> loaded {} bytes".format(scanfile, len(s)))

        elif scanfile is not None:
            s = payload
            self.scanfile = scanfile
            self.scanpath = config['scanpath'] + self.scanfile

            print("Processing File [{}] --> loaded {} bytes".format(scanfile, len(s)))

        else:
            print ("Not suitable data to parse, aborting ..")
            return



        self.entrypoint = s.find(b'BQ.CCD.Data.Scan2D[]')

        if self.entrypoint > -1:
            # print("Scans entry point found @ {}".format(self.entrypoint))
            self.marker = s[self.entrypoint+27]
            self.recsize = self.findRecordSize(s,self.marker,self.entrypoint+28)
            if self.recsize != 0:

                self.recnum, scaninit = self.findRecosdNum(s, self.marker, self.recsize, self.entrypoint+27)
                # print("MARKER IS [{}] -- Found {} dir_entries of Recsize {}\n".format(self.marker, self.recnum, self.recsize))
                self.cursor = scaninit

                self.scans = list()

                for scan_num in range (0,self.recnum):
                    scan = Scan(s, scan_num, self.cursor)
                    tempvars = scan.scantail.vars
                    tempvars['FilePath'] = scanfile
                    tempvars['FileSize'] = len(s)
                    tempvars['RecNumber'] = self.recnum
                    tempvars['RecSize'] = self.recsize
                    tempvars['EntryPoint'] = self.entrypoint

                    self.scans.append(scan)
                    self.cursor = scan.cursor

            else:
                print("Could not find Recsize")
        else:
            print("Could not find Entrypoint")


    def getDataframe(self):

        scanframes = list()
        for scan in self.scans:
            scanframes.append(scan.scantail.vars)

        self.df = pd.DataFrame(scanframes)

        return self.df

    def getScanRows(self, chipnum, integration):

        for scan in self.scans:
            if scan.scantail.vars['ChipNo'] != chipnum: continue
            if scan.scantail.vars["IntegrationTime"] == integration :
                return scan.scanrows[0][0]

        return None





    def getIntegrations(self, chip):
        scanint = list()
        default = -1
        for scan in self.scans:
            chipnr = scan.scantail.vars["ChipNo"]
            if chipnr == chip:
                time = scan.scantail.vars["IntegrationTime"]
                if default == -1 : default = time
                entry = {'label': time, 'value': time}
                scanint.append(entry)

        return scanint, default


    def getChipNums(self):
        scanint = list()
        chips = set()
        for scan in self.scans:
            schip = "{}".format(scan.scantail.vars["ChipNo"])
            if not schip in chips:
                chips.add(schip)
                entry = {'label': schip, 'value': scan.scantail.vars["ChipNo"]}
                scanint.append(entry)

        return scanint



    def listScan(self, id):

        scanvars = self.scans[id].scantail.vars

        print ('Listing scan[{}/{}] of file [{}] EntryPoint @{} '.format(
            id, scanvars['ScanNumber'], scanvars['FilePath'],  scanvars['PayloadInit']
        ))
        for key in scanvars.keys():
            if key != 'ScanRows':
                print ('\tInfodir key [{}] is [{}]'.format(key, scanvars[key]))


    def findRecordSize(self,sarray, marker, ptr):

        for nexttk in range(ptr , ptr+60):
            if sarray[nexttk] == marker:
                return (nexttk - ptr) + 1
        return 0

    def findRecosdNum(self, sarray, marker, recsize, ptr):

        recnum = 0

        while sarray[ptr] == marker :
            recnum +=1
            ptr += recsize

        return recnum, (ptr-recsize)+12

















    def configLogger(self, qlog):
        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
