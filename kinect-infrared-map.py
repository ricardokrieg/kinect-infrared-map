#!/usr/bin/python

import pygame
from pygame.locals import *
from pygame.color import THECOLORS
from openni import *
import numpy
import cv
import sys

XML_FILE = 'config.xml'
MAX_DEPTH_SIZE = 10000

context = Context()
context.init_from_xml_file(XML_FILE)

ir_generator = IRGenerator()
ir_generator.create(context)

context.start_generating_all()

pygame.init()
screen = pygame.display.set_mode((640, 480))
ir_frame = pygame.Surface((640, 480))
pygame.display.set_caption('Kinect Infrared Map')

running = True

MIN_8_BIT = 0
MAX_8_BIT = 255

while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
	# for

	screen.fill(THECOLORS['white'])
	context.wait_any_update_all()
	cv.WaitKey(10)

	ir_map = numpy.asarray(ir_generator.get_tuple_ir_map())
	min_ir = ir_map.min()
	max_ir = ir_map.max()

	display_ratio = float((MAX_8_BIT-MIN_8_BIT)/(max_ir-min_ir))

	depth_frame = numpy.arange(640*480, dtype=numpy.uint32)

	depth_frame = ir_map[depth_frame]

	depth_frame = depth_frame.reshape(ir_generator.metadata.res[1], ir_generator.metadata.res[0])

	frame_surface = pygame.transform.rotate(pygame.transform.flip(pygame.surfarray.make_surface(depth_frame), True, False), 90)
	frame_surface.set_palette(tuple([(i, i, i) for i in range(256)]))
	ir_frame.blit(frame_surface, (0, 0))

	screen.blit(ir_frame, (0, 0))

	pygame.display.flip()
# while

context.stop_generating_all()
sys.exit(0)