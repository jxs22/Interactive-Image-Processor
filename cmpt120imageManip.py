# CMPT 120 Yet Another Image Processer
# Starter code for cmpt120imageManip.py
# Author(s): Jagjot Sidhu
# Date:
# Description:

import cmpt120imageProjHelper
import numpy
import copy
import math
import pygame

img = cmpt120imageProjHelper.getImage('project-photo.jpg')
height = len(img)
width = len(img[0])

def redFilter(pixels):
    for i in range(height):
        for j in range(width):
            pixel = pixels[i][j]
            pixel[1]=0
            pixel[2]=0
    return pixels

def blueFilter(pixels):
    for i in range(height):
        for j in range(width):
            pixel = pixels[i][j]
            pixel[0]=0
            pixel[1]=0       
    return pixels

def greenFilter(pixels):
    for i in range(height):
        for j in range(width):
            pixel = pixels[i][j]
            pixel[0]=0
            pixel[2]=0
    return pixels

def sepia_filter(pixels):
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            r = pixels[i][j][0]
            g = pixels[i][j][1]
            b = pixels[i][j][2]
            sepiaRed = int((r * 0.393) + (g * 0.769) + (b * 0.189))
            sepiaGreen = int((r * 0.349) + (g * 0.686) + (b * 0.168))
            sepiaBlue  = int((r * 0.272) + (g *0.534) + (b * 0.131))
            sepiaRed = min(sepiaRed, 255)
            sepiaGreen = min(sepiaGreen, 255)
            sepiaBlue = min(sepiaBlue, 255)
            pixels[i][j] = [sepiaRed,sepiaGreen,sepiaBlue]
    return pixels

def warm_filter(pixels):
    for i in range(height):
        for j in range(width):
            r = pixels[i][j][0]
            g = pixels[i][j][1]
            b = pixels[i][j][2]

            if r < 64:
                r = int(r/64*80)
            elif r >= 64 and r < 128:
                r = int((r-64)/(128-64) * (160-80) + 80)
            else: 
                r = int((r-128)/(255-128) * (255-160) + 160)
            
            if b < 64:
                b = int(b/64*50)
            elif b >= 64 and b < 128:
                b = int((b-64)/(128-64) * (100-50) + 50)
            else:
                int((b-128)/(255-128) * (255-100) + 100)
            r = min(r,255)
            g = min(g, 255)
            b = min(b, 255)
            pixels[i][j] = [r,g,b]
    return pixels

def cold_filter(pixels):
    for i in range(height):
        for j in range(width):
            r = pixels[i][j][0]
            g = pixels[i][j][1]
            b = pixels[i][j][2]
            if b < 64:
                b = int(b/64*80)
            elif b >= 64 and b < 128:
                b = int((b-64)/(128-64) * (160-80) + 80)
            else: 
                b = int((b-128)/(255-128) * (255-160) + 160)
            
            if r < 64:
                r = int(r/64*50)
            elif r >= 64 and r < 128:
                r = int((r-64)/(128-64) * (100-50) + 50)
            else:
                int((r-128)/(255-128) * (255-100) + 100)
            r = min(r,255)
            g = min(g, 255)
            b = min(b, 255)
            pixels[i][j] = [r,g,b]
    return pixels

def rotate_left(pixels):
    o = []
    for i in range(width):
        a=[]
        for j in range(height):
            a.append(pixels[j][i])
        o.insert(0,a)
    return o
    
def rotate_right(pixels):
    o=[]
    for i in range(width):
        a=[]
        for j in range(height-1,-1,-1):
            a.append(pixels[j][i])
        o.append(a)
    return o
    
def double_size(pixels):
    a=[[[]]*2*width for _ in range(2*height)]
    for i in range(height):
        for j in range(width):
            a[((i+1)*2)-1][((j+1)*2)-1] = pixels[i][j]
            a[(((i+1)*2)-1)-1][((j+1)*2)-1] = pixels[i][j]
            a[((i+1)*2)-1][(((j+1)*2)-1)-1] = pixels[i][j]
            a[(((i+1)*2)-1)-1][(((j+1)*2)-1)-1] = pixels[i][j]
    return a

def half_size(pixels):
    newwidth = math.floor(width/2)
    newheight = math.floor(height/2)
    a=[[[]]*(newwidth) for _ in range(newheight)]
    for i in range(newheight):
        for j in range(newwidth):
            r = (pixels[((i+1)*2)-1][((j+1)*2)-1][0] + pixels[(((i+1)*2)-1)-1][((j+1)*2)-1][0]+pixels[((i+1)*2)-1][(((j+1)*2)-1)-1][0]+pixels[(((i+1)*2)-1)-1][(((j+1)*2)-1)-1][0])/4
            g = (pixels[((i+1)*2)-1][((j+1)*2)-1][1] + pixels[(((i+1)*2)-1)-1][((j+1)*2)-1][1]+pixels[((i+1)*2)-1][(((j+1)*2)-1)-1][1]+pixels[(((i+1)*2)-1)-1][(((j+1)*2)-1)-1][1])/4
            b = (pixels[((i+1)*2)-1][((j+1)*2)-1][2] + pixels[(((i+1)*2)-1)-1][((j+1)*2)-1][2]+pixels[((i+1)*2)-1][(((j+1)*2)-1)-1][2]+pixels[(((i+1)*2)-1)-1][(((j+1)*2)-1)-1][2])/4
            newpixels = (round(r),round(g),round(b))
            a[i][j] = newpixels
    return a

def detect(pixels):
  for i in range(height):
    for j in range(width):
      value = cmpt120imageProjHelper.rgb_to_hsv(pixels[i][j][0],pixels[i][j][1],pixels[i][j][2])
      if value[0] == 54.62686567164178:
        return greenbox(pixels,i,j)

def greenbox(pixels,x,y):
    value1=x-20
    value2=x+85
    npixels = copy.deepcopy(pixels)
    for i in range(y,y+60,1):
      if i>= width:
        break
      npixels[value1][i][0]=0
      npixels[value1][i][1]=255
      npixels[value1][i][2]=0

      npixels[value2][i][0]=0
      npixels[value2][i][1]=255
      npixels[value2][i][2]=0
    
    for i in range(y,y-60,-1):
      if i<0:
        break
      npixels[value1][i][0]=0
      npixels[value1][i][1]=255
      npixels[value1][i][2]=0

      npixels[value2][i][0]=0
      npixels[value2][i][1]=255
      npixels[value2][i][2]=0
    
    valuey1 = y+60
    valuey2 = y-60

    for i in range(value1+1,value2):
      npixels[i][valuey1][0]=0
      npixels[i][valuey1][1]=255
      npixels[i][valuey1][2]=0

      npixels[i][valuey2][0]=0
      npixels[i][valuey2][1]=255
      npixels[i][valuey2][2]=0

    return npixels

      