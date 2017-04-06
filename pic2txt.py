from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

file = "/home/jc/Downloads/1.jpeg"
img = np.array((Image.open(file).resize((100,100), Image.ANTIALIAS)).convert('L'))
count = 0
rows, cols = img.shape
for i in range(rows):
	for j in range(cols):
		count += img[i,j]
edge = count / (rows*cols)
a = np.array([[0 for i in range(cols)] for i in range(rows)])
for i in range(rows):
	for j in range(cols):
		if img[i, j] > edge:
			a[i, j] = 1
		else:
			a[i, j] = 0
plt.imshow(a, cmap="gray")
plt.show()
print a