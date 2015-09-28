

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

        cosvalb = math.cos(self.beta)
        sinvalb = math.sin(self.beta)
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
    def __init__(self):
        pass

    def add_element(self,elem_to_add):
        elem = GPG_Pos_Dist_Element()
        elem.set_copy(elem_to_add)
        self.Elements.append(elem)
        self.numelem = self.numelem+1

    def release_element(self):
        self.Elements = []
        self.numelem = 0

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

    def FromFile(self,gpg_pos_dist,workfile):
        gpg_pos_dist.release_element()
        with open(workfile, 'r') as f:
            io = GPG_Pos_Dist_Element_IO()
            s = f.readline()
            num_elem = int(s)
            num_read=0
            elem = GPG_Pos_Dist_Element()
            while num_read<num_elem:
                num_read=num_read+1
                io.ToRead(f,elem)
                gpg_pos_dist.add_element(elem)
        f.closed

    def ToFile(self,gpg_pos_dist,workfile):
        with open(workfile, 'w') as f:
            io = GPG_Pos_Dist_Element_IO()
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
    def __init__(self,cell_x,cell_y):
        self.num_cell_x = cell_x
        self.num_cell_y = cell_y

    def get_cell_num(self):
        return (self.num_cell_x,self.num_cell_y)
    def set_cell_value(self,val):
        self.value = val
    def get_cell_value(self):
        return self.value

class GPG_Map:
    size_cell_x = 20
    size_cell_y = 20
    cells =[]

    def CalculateCell(self,point):
        cellx = (int(point.x) + size_cell_x/2)/size_cell_x
        celly = (int(point.y) + size_cell_y/2)/size_cell_y
        return (cellx,celly)



    def AddToMap(self,elem):
        points = element.get_frame(scale,offsetx,offsety)
        pos_zero = element.get_pos()
        last_cell = (None,None)
        num_point = 0
        for point in points:

            cell = self.CalculateCell(point)
            num_point = num_point+1





