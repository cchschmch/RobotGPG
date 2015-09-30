
from geometry import *
import math

class GPG_Bbox:
    x = 0
    y = 0
    w = 0
    h = 0
    def __init__(self):
        pass
    def set(self,xx,yy,ww,hh):
        self.x = xx
        self.y = yy
        self.w = ww
        self.h = hh

class GPG_Pos_Dist_Element:
    x=0
    y=0
    alpha=0
    beta=0
    usd=0
    def __init__(self):
        pass

    def set_pos(self, xx,yy):
        self.x = xx
        self.y = yy

    def get_pos(self):
        return (self.x,self.y)

    def set_alpha(self, aa):
        self.alpha = aa*2*math.pi/360

    def set_beta(self, bb):
        self.beta = bb*2*math.pi/360

    def set_usd(self,uu):
        self.usd = uu

    def set_all(self, xx,yy,aa,bb,uu):
        self.set_pos(xx,yy)
        self.set_alpha(aa)
        self.set_beta(bb)
        self.set_usd(uu)
    def set_copy(self,elem_to_copy):
        self.x =elem_to_copy.x
        self.y = elem_to_copy.y
        self.alpha = elem_to_copy.alpha
        self.beta = elem_to_copy.beta
        self.usd = elem_to_copy.usd

    def get_frame(self, scale,offsetx,offsety):
        points = []
        points.append((offsetx+scale*self.x,offsety+scale*self.y))
        cosvala = math.cos(self.alpha)
        sinvala = math.sin(self.alpha)
        pointx = offsetx+scale*(self.x+8*cosvala)
        pointy = offsety+scale*(self.y+8*sinvala)
        points.append((pointx,pointy))

        cosvalb = math.cos(self.alpha+self.beta)
        sinvalb = math.sin(self.alpha+self.beta)
        pointx = offsetx+scale*(self.x+8*cosvala)+scale*(self.x+(self.usd+4)*cosvalb)
        pointy = offsety+scale*(self.y+8*sinvala)+scale*(self.y+(self.usd+4)*sinvalb)
        points.append((pointx,pointy))
        return points

    def get_bbox(self, scale):
        bbox = GPG_Bbox()
        points = self.get_frame(scale,0,0)
        xmin = +10000000
        xmax = -10000000
        ymin = +10000000
        ymax = -10000000

        width = 0
        height = 0
        for (x_test,y_test) in points:
            if x_test<xmin:
                xmin =x_test
            if x_test>xmax:
                xmax = x_test
            if y_test<ymin:
                ymin =y_test
            if y_test>ymax:
                ymax = y_test
        width = xmax-xmin;
        height = ymax-ymin
        bbox.set(xmin,xmax,width,height)
        return bbox

class GPG_Pos_Dist_Element_IO:
    num_version=0
    def __init__(self,num_version):
        self.num_version=num_version

    def ToFile(self,f,gpg_Pos_Dist_Element):
        if f:
            s = str(gpg_Pos_Dist_Element.x)+'\n'
            f.write(s)
            s = str(gpg_Pos_Dist_Element.y)+'\n'
            f.write(s)
            s = str(gpg_Pos_Dist_Element.alpha)+'\n'
            f.write(s)
            s = str(gpg_Pos_Dist_Element.beta)+'\n'
            f.write(s)
            s = str(gpg_Pos_Dist_Element.usd)+'\n'
            f.write(s)

    def ToRead(self,f,gpg_Pos_Dist_Element):
        if f:
            s=f.readline()
            gpg_Pos_Dist_Element.x = float(s)
            s=f.readline()
            gpg_Pos_Dist_Element.y = float(s)
            s=f.readline()
            gpg_Pos_Dist_Element.alpha = float(s)
            s=f.readline()
            gpg_Pos_Dist_Element.beta = float(s)
            s=f.readline()
            gpg_Pos_Dist_Element.usd = float(s)

class GPG_Pos_Dist:
    Elements = []
    numelem = 0
    num_version = 0
    def __init__(self):
        pass
    def get_version(self):
        return self.num_version
    def add_element(self,elem_to_add):
        elem = GPG_Pos_Dist_Element()
        elem.set_copy(elem_to_add)
        self.Elements.append(elem)
        self.numelem = self.numelem+1

    def release_element(self):
        self.Elements = []
        self.numelem = 0


        
    def get_element(self,num):
        if num<self.numelem:
            return self.Elements[num]
        else:
            return None
    def get_num_element(self):
        return self.numelem        
    def get_frame(self,scale,offsetx,offsety,num):
        if num<self.numelem:
            element = self.Elements[num]
            return element.get_frame(scale,offsetx,offsety)

    def get_bbox(self, scale):
        bbox = GPG_Bbox()
        xmin = +10000000
        xmax = -10000000
        ymin = +10000000
        ymax = -10000000

        width = 0
        height = 0
        for element in self.Elements:
            one_bbox = element.get_bbox(scale)
            x_test = one_bbox.x
            y_test = one_bbox.y
            x_test_w = one_bbox.w
            y_test_h = one_bbox.h
            if x_test<xmin:
                xmin = x_test
            if x_test>xmax:
                xmax = x_test
            if y_test<ymin:
                ymin = y_test
            if y_test>ymax:
                ymax = y_test
            x_test = x_test + x_test_w
            y_test = y_test + y_test_h
            if x_test<xmin:
                xmin = x_test
            if x_test>xmax:
                xmax = x_test
            if y_test<ymin:
                ymin = y_test
            if y_test>ymax:
                ymax = y_test

        width = xmax-xmin;
        height = ymax-ymin
        bbox.set(xmin,xmax,width,height)
        return bbox

class GPG_Pos_Dist_IO:
    num_version = 0
    def __init__(self,num_version):
        self.num_version = num_version

    def FromFile(self,gpg_pos_dist,workfile,info):
        gpg_pos_dist.release_element()
        with open(workfile, 'r') as f:

            info = f.readline()
            s = f.readline()
            self.num_version = int(s)
            io = GPG_Pos_Dist_Element_IO(self.num_version)
            s = f.readline()
            num_elem = int(s)
            num_read=0
            elem = GPG_Pos_Dist_Element()
            while num_read<num_elem:
                num_read=num_read+1
                io.ToRead(f,elem)
                gpg_pos_dist.add_element(elem)
        f.closed

    def ToFile(self,gpg_pos_dist,workfile,info):
        with open(workfile, 'w') as f:
            s=info+'\n'
            f.write(s)
            s=str(self.num_version)+'\n'
            f.write(s)
            io = GPG_Pos_Dist_Element_IO(self.num_version)
            num_elem = gpg_pos_dist.get_num_element()
            s = str(num_elem)+'\n'
            f.write(s)
            for element in gpg_pos_dist.Elements:
                io.ToFile(f,element)
        f.closed

class GPG_Map_Cell:
    value = 0 # -1 / 0 / 1
    num_cell_x = 0
    num_cell_y = 0
    def __init__(self,cellGrid):
        self.num_cell_x = cellGrid[0]
        self.num_cell_y = cellGrid[1]

    def get_cell_num(self):
        return (self.num_cell_x,self.num_cell_y)
    def set_cell_value(self,val):
        self.value = val
    def get_cell_value(self):
        return self.value
    def get_cell_pos(self):
        return (self.num_cell_x,self.num_cell_y )

    def get_frame(self, scale,size_cell_x,size_cell_y,offsetx,offsety):
        points = []
        localoffsetx = -scale*size_cell_x/2
        localoffsety = -scale*size_cell_y/2
        points.append((localoffsetx+offsetx+scale*self.num_cell_x*size_cell_x,localoffsety+offsety+scale*self.num_cell_y*size_cell_y))
        points.append((localoffsetx+offsetx+scale*(self.num_cell_x+1)*size_cell_x,localoffsety+offsety+scale*self.num_cell_y*size_cell_y))
        points.append((localoffsetx+offsetx+scale*(self.num_cell_x+1)*size_cell_x,localoffsety+offsety+scale*(self.num_cell_y+1)*size_cell_y))
        points.append((localoffsetx+offsetx+scale*self.num_cell_x*size_cell_x,localoffsety+offsety+scale*(self.num_cell_y+1)*size_cell_y))
        points.append((localoffsetx+offsetx+scale*self.num_cell_x*size_cell_x,localoffsety+offsety+scale*self.num_cell_y*size_cell_y))
        return points

    def get_rect(self,size_cell_x,size_cell_y):
        localoffsetx = -size_cell_x/2
        localoffsety = -size_cell_y/2
        r1 = Rect((localoffsetx+self.num_cell_x*size_cell_x,localoffsety+self.num_cell_y*size_cell_y), (size_cell_x , size_cell_x))
        r1.normalize()
        return r1

class GPG_Map:
    size_cell_x = 20
    size_cell_y = 20
    cells =[]
    numelem = 0
    def __init__(self,cell_x,cell_y):
        self.size_cell_x = cell_x
        self.size_cell_y = cell_y

    def CalculateCell(self,point):
        cellx = (int(point[0]) + self.size_cell_x/2)/self.size_cell_x
        celly = (int(point[1]) + self.size_cell_y/2)/self.size_cell_y
        return (cellx,celly)

    def AddInterToMap(self,first_cell,last_cell,first_point, last_point):
        cel_minx = min (first_cell.num_cell_x,last_cell.num_cell_x)
        cel_miny = min (first_cell.num_cell_y,last_cell.num_cell_y)
        cel_maxx = max (first_cell.num_cell_x,last_cell.num_cell_x)
        cel_maxy = max (first_cell.num_cell_y,last_cell.num_cell_y)
        for cell_x in range (cel_minx,cel_maxx+1):
            for cell_y in range (cel_miny,cel_maxy+1):
               found_intercell = False
               for interCell in self.cells:
                    if interCell.get_cell_pos() == (cell_x,cell_y):
                        found_intercell = True
                        if interCell is not first_cell:
                            if interCell is not last_cell:

                                rect_points = interCell.get_frame(1,self.size_cell_x,self.size_cell_y,0,0)
                                last_rect_point = None
                                intersect_rect = False
                                for first_rect_point in rect_points:
                                    if last_rect_point is not None:
                                        intersect_point = calculateIntersectPoint(first_point, last_point, first_rect_point, last_rect_point)
                                        if intersect_point is not None:
                                            if interCell.get_cell_value()<1:
                                                interCell.set_cell_value(0)
                                    last_rect_point = first_rect_point
               if not found_intercell:
                    interCell = GPG_Map_Cell((cell_x,cell_y))
                    rect_points = interCell.get_frame(1,self.size_cell_x,self.size_cell_y,0,0)
                    last_rect_point = None
                    intersect_rect = False
                    already_add = False
                    for first_rect_point in rect_points:
                        if not already_add:
                            if last_rect_point is not None:
                                intersect_point = calculateIntersectPoint(first_point, last_point, first_rect_point, last_rect_point)
                                if intersect_point is not None:
                                    already_add = True
                                    self.cells.append(interCell)
                                    self.numelem = self.numelem+1
                                    interCell.set_cell_value(0)
                        last_rect_point = first_rect_point

    def AddToMap(self,elem,inter):
        scale = 1
        offsetx = 0
        offsety = 0
        points = elem.get_frame(scale,offsetx,offsety)
        pos_zero = elem.get_pos()
        last_cell = None
        num_point = 0
        last_point = None
        for first_point in points:
            cellGrid = self.CalculateCell(first_point)
            found = False
            first_cell = None
            for OneCell in self.cells:
                if OneCell.get_cell_value() == cellGrid:
                    found = True
                    first_cell = OneCell
                    if num_point<2:
                        OneCell.set_cell_value(-1)
                    else:
                        OneCell.set_cell_value(1)
            if not found:
                OneCell = GPG_Map_Cell(cellGrid)
                first_cell = OneCell
                if num_point<2:
                    OneCell.set_cell_value(-1)
                else:
                    OneCell.set_cell_value(1)
                self.cells.append(OneCell)
                self.numelem = self.numelem+1
            if inter:
                if num_point>=2:
                    if last_cell is not None:
                        if last_point is not None:
                            self.AddInterToMap(first_cell,last_cell,first_point,last_point)

            num_point = num_point+1
            last_cell = first_cell
            last_point = first_point
            
    def AddAllToMap(self,gpg_Pos_Dist):
        num_element = gpg_Pos_Dist.get_num_element()
        num = 0
        while num < num_element:
            self.AddToMap(gpg_Pos_Dist.get_element(num),True)
            num = num +1
            
    def get_num_element(self):
        return self.numelem        
        
    def get_level(self,num):
        if num<self.numelem:
            element = self.cells[num]
            return element.get_cell_value()
        else:
            return -1
            
    def get_frame(self,scale,offsetx,offsety,num):
        if num<self.numelem:
            element = self.cells[num]
            return element.get_frame(scale,self.size_cell_x,self.size_cell_y,offsetx,offsety)





