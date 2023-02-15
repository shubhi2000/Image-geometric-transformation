import cv2
from PIL import Image
from numpy import asarray
import numpy as np
import math
import ast

"""T1=[[math.cos(45*math.pi/180),math.sin(45*math.pi/180),0],[-1*math.sin(45*math.pi/180),math.cos(45*math.pi/180),0],[0,0,1]]
T2=[[2,0,0],[0,2,0],[0,0,1]]
T3=[[1,0,0],[0,1,0],[30,30,1]]
T=np.dot(np.array(T1),np.dot(np.array(T2),np.array(T3)))
print(T)"""
print("Input the image name")
img_name=input()
print("Input the transformation matrix")
T=ast.literal_eval(input())

image=Image.open("./"+img_name)
M0,N0=image.size
image_array=asarray(image)

x_min="*"
x_max="*"
y_min="*"
y_max="*"
for i in range(M0):
	for j in range(N0):
		M=np.dot(np.array([i,j,1]),np.array(T))
		x=M[0]
		y=M[1]
		if x_min=="*":
			x_min=x
		else:
			x_min=min(x_min,x)
		if x_max=="*":
			x_max=x
		else:
			x_max=max(x_max,x)
		if y_min=="*":
			y_min=y
		else:
			y_min=min(y_min,y)
		if y_max=="*":
			y_max=y
		else:
			y_max=max(y_max,y)
x_min=math.floor(x_min)
y_min=math.floor(y_min)
x_max=math.ceil(x_max)
y_max=math.ceil(y_max)
M1,N1=x_max-x_min+1,y_max-y_min+1
new_array=np.ones((M1,N1))*(-1)
for i in range(x_min,x_max+1):
	for j in range(y_min,y_max+1):
		M=np.dot(np.array([i,j,1]),np.linalg.inv(np.array(T)))
		x=M[0]
		y=M[1]
		if x>=M0-2 or y>=N0-2:
			continue
		if x<=0 or y<=0:
			continue
		x1,y1=math.floor(x),math.floor(y)
		x2,y2=x1+1,y1
		x3,y3=x1,y1+1
		x4,y4=x1+1,y1+1

		X=[[x1,y1,x1*y1,1],[x2,y2,x2*y2,1],[x3,y3,x3*y3,1],[x4,y4,x4*y4,1]]
		V=[[image_array[x1][y1]],[image_array[x2][y2]],[image_array[x3][y3]],[image_array[x4][y4]]]
		A=np.dot(np.linalg.inv(X),V)
		new_array[i-x_min][j-y_min]=np.dot(np.array([x,y,x*y,1]),A)

print("Input Image is:")
img=Image.fromarray(image_array)
img.show()
print("Transformation matrix is:")
print(T)
print("Output Image is:")
img=Image.fromarray(new_array)
img.show()
cv2.imwrite("q4_out.jpg",new_array)