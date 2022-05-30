import logging
import untangle
import uuid

from itertree import iTree

logger = logging.getLogger(__name__)

class CCDProj():

    def __init__(self, projfile, config = None, qlog = None):

        self.configLogger(qlog)

        # self.projpath = config['scanpath'] + projfile
        with open(projfile, 'r+b') as f:
            # s = f.read()
            # self.projfile = projfile
            elm = untangle.parse(f)
            print("Processing File [{}] --> loaded {} bytes".format(projfile, 30))

        t2 = elm.NewDataSet

        count = 0

        self.items = dict()
        self.paths = dict()

        # Mount a linear sequence of items by marshaling the xml
        for item in t2.tblCCDItems:
            # print ('Item = {}'.format(item))
            ccditem = CCDItem(item)
            self.items[ccditem.id] = ccditem
            count +=1;

        # Now build a directory of paths by building from a leaf (integrator) up to lightsource
        vlas = list(self.items.values())
        klas = list(self.items.keys())

        # First determine who is leaf (shold be anintegrator channel by now)
        for key in klas:
            for item in vlas:
                if item.parent is not None:
                    if item.parent == key:
                        # print ('Normal found @ '+ self.printNode(item))
                        cit:CCDItem = self.items[key]
                        cit.leaf = False
                        break

        # Now build a path list walking up from leaf to root
        for item2 in vlas:
            if item2.leaf :
                temppath = list()
                itemp = item2
                if itemp.name == 'Channel':
                    name = itemp.itdict['IntegrSymbol']
                else :
                    name = itemp.name
                while itemp.id != uuid.UUID('00000000-0000-0000-0000-000000000000'):
                    temppath.append(itemp)
                    seg = itemp.name
                    itemp = self.items[itemp.parent]

                name = name + ':' + seg
                self.paths[name] = temppath

                # print ('leaf path of {} done'.format(name))
                self.printPath(temppath, name)



    def printPath(self, path, name):

        print ('\nResults for path {}'.format(name) )
        for idx in range(len(path)):
            ident = "  " * idx
            ccdit = path[idx]
            print("{}[{}] / ID=[{}]  parent = [{}]  -- seq = [{}]".format(ident, ccdit.name, ccdit.id, ccdit.parent, ccdit.seq))
            print ('{}dict = {}'.format(ident, ccdit.itdict))





    def printNode (self, ccdit) :
       return "Item : '[{}] / ID=[{}]  parent = [{}]  -- seq = [{}] \n\thas dict = {}".format (ccdit.name, ccdit.id, ccdit.parent, ccdit.seq, ccdit.itdict)


    def addChildren(self, itlevel, parentuid, items, itree):

        for localit in items:
            if localit.parent == parentuid :
                itree.append(iTree(tag=localit.id, data = self.items[localit.id]))
                itlevel +=1
                self.addChildren(itlevel, localit.id, items, itree[itlevel])
            # else :
            #     itlevel -=1


    def configLogger(self, qlog):
        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)





class CCDItem :

    def __init__(self, item):


        self.leaf = True
        self.referenced = False

        self.id = uuid.UUID(item.ID.cdata)
        if item.ID.cdata == '00000000-0000-0000-0000-000000000000':
            self.parent= None
        else:
            self.parent = uuid.UUID(item.ParentID.cdata)
        self.seq = item.Seq.cdata
        self.name = item.Name.cdata
        self.typename = item.CCDItemTypeName.cdata
        self.props = item.CCDItemProps.cdata
        self.itdict = dict()

        if self.props is not None:
            cdic = untangle.parse(self.props)
            for cdit in cdic.dictionary:
                if len(cdit) == 0 : break
                for cditem in cdit.item:
                    key = cditem.key.string.cdata
                    value = cditem.value.anyType.cdata
                    self.itdict[key] = value

            # print ('Item name {} has')











        # itid = uuid.UUID('00000000-0000-0000-0000-000000000000')
        # self.itroot = iTree(tag=itid, data = self.items[itid])
        # self.itlevel = -1;
        # self.addChildren(self.itlevel, itid, list(self.items.values()), self.itroot)
        # self.itroot.render();






# t2 = elm.svg.defs.linearGradient.stop
#
# for stop in t2:
#     print ('Stop = {}'.format(stop))
#     print ('\tData is : offset = {}'.format(stop['offset']))












