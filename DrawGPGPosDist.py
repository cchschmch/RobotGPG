import pygame
from pygame.locals import *

from GPG_Pos_Dist import*

import os
import time

class App:
	def __init__(self, width=640, height=400, fps=30):
		self._running = True
		self._display_surf = None
		self.width	= width
		self.height = height
		self.height_screen = 0
		self.width_screen = 0
		self.fps = fps
		self.playtime = 0.0

	def on_init(self):
		pygame.init()
		infoObject = pygame.display.Info()
		self.width_screen = infoObject.current_w
		self.height_screen = infoObject.current_h
		self.clock = pygame.time.Clock()
		self.size = self.width, self.height
		self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self._running = True
		self.sample = GPG_Pos_Dist();

		self.offsetx = self.width/2
		self.offsety = self.height/2
			
	def generate_sample(self,sample, usd):
		one_sample = GPG_Pos_Dist_Element()
		istep = 5
		icurrent = 0
		while icurrent<360:
			one_sample.set_all(0,0,icurrent,0,usd)
			sample.add_element(one_sample)
			icurrent = icurrent+ istep
			
	def get_scale(self,sample):
		scale = 1
		bbox = sample.get_bbox(scale)
		scalex = self.width/bbox.w
		scaley = self.height/bbox.h
		if scalex<scale:
			scale=scalex
		if scaley<scale:
			scale=scaley
		scalex = self.width/bbox.h
		scaley = self.height/bbox.w
		if scalex<scale:
			scale=scalex
		if scaley<scale:
			scale=scaley
		return scale

	def on_event_key(self,event):
		if event.key == pygame.K_ESCAPE:
			self._running = False

	def on_event_mouse(self,down,event):
		pass
	
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == pygame.KEYDOWN:
			self.on_event_key(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.on_event_mouse(True,event)
		elif event.type == pygame.MOUSEBUTTONUP:
			self.on_event_mouse(False,event)

	



	def on_loop(self):
		self.miliseconds = self.clock.tick(self.fps)
		self.playtime+=self.miliseconds / 1000.0
		self.sample.release_element()
		self.generate_sample(self.sample, self.playtime*50)
		self.scale = self.get_scale(self.sample)
	
	def on_render(self):
		self.screen.blit(self.background, (0,0)) 
		num_element = self.sample.get_num_element()
		num = 0
		while num < num_element:
			num = num +1
			points = self.sample.get_frame(self.scale,self.offsetx,self.offsety,num)
			if points:
				pygame.draw.lines(self.screen,(255,255,255),False,points,1)
			
		pygame.display.flip()
		
	def on_cleanup(self):
		pygame.quit()
		
 
	def on_execute(self):
		if self.on_init() == False:
			self._running = False
 
		while( self._running ):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

 
if __name__ == "__main__" :
	theApp = App(600,480,30)
	theApp.on_execute()