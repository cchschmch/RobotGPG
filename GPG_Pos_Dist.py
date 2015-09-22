

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
		cosval = math.cos(self.alpha+self.beta)
		sinval = math.sin(self.alpha+self.beta)
		pointx = offsetx+scale*(self.x+self.usd*cosval)
		pointy = offsety+scale*(self.y+self.usd*sinval)
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


