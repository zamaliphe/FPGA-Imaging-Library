__author__ = 'Tianyu Dai (dtysky)'

from PIL import Image
import os, json
from ctypes import *
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

FileFormat = ['.jpg', '.bmp']
Conf = json.load(open('../ImageForTest/conf.json', 'r'))['conf']

def show_error(e):
	MessageBox(e)
	exit(0)

def name_format(root, name, ex, conf):
	return '%s-%s-%s-%s' % (name, conf['mode'], conf['th1'], conf['th2'])

def conf_format(im, conf):
	mode = conf['mode']
	th1 = int(conf['th1'])
	th2 = int(conf['th2'])
	if mode == 'Base':
		return '%s\n%s\n%s\n' % ('0', color_format('L', th1), color_format('L', th2))
	return '%s\n%s\n%s\n' % ('1', color_format('L', th1), color_format('L', th2))

def color_format(mode, color):
	res = ''
	color = [color]
	for c in color:
		tmp = bin(c)[2:]
		for i in xrange(10 - len(bin(c))):
			tmp = '0' + tmp
		res += tmp
	return res

def create_dat(im, conf):
	mode = im.mode
	if im.mode not in ['L']:
		show_error('This module just supports Gray-scale images, check your images !')
	if conf['mode'] not in ['Base', 'Contour']:
		show_error('''This module just supports conf "Base" and "Contour", check your conf !''')
	data_src = im.getdata()
	xsize, ysize = im.size
	data_res = ''
	for color in data_src:
		data_res += color_format(mode, color) + '\n'
	return data_res[:-1]

FileAll = []
for root,dirs,files in os.walk('../ImageForTest'):
    for f in files:
    	name, ex=os.path.splitext(f)
        if ex in FileFormat:
        	FileAll.append((root+'/', name, ex))
dat_index = ''
for root, name, ex in FileAll:
	im_src = Image.open(root + name + ex)
	xsize, ysize = im_src.size
	for c in Conf:
		dat_res = open('../FunSimForHDL/%s.dat' \
			% name_format(root, name, ex, c), 'w')
		dat_res.write('%d\n%d\n' % (xsize, ysize))
		dat_res.write('%s' % conf_format(im_src, c))
		dat_res.write(create_dat(im_src, c))
		dat_index += '%s' % name_format(root, name, ex, c)
		dat_index += '\n'
		dat_res.close()
dat_index = dat_index[:-1]
dat_index_f = open('../FunSimForHDL/imgindex.dat','w')
dat_index_f.write(dat_index)
dat_index_f.close()