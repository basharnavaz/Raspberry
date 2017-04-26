# Python 2.7 code to test the speed of operation of
# different commands. This need arose when the speed
# of compressing and decompressing data came.

import zlib
import cv2
import numpy as np
import time
from cPickle import dumps, loads


# =========GRAY 640x480=========
print "=========GRAY 640x480========="
img = cv2.imread('capt_640_gray.png', 0)
'''
start = time.time()
img_d = dumps(img)
print "Dumping Time: ", (time.time()-start)

start = time.time()
img_d_c = zlib.compress(img_d, 1)
print "Compression Time: ", (time.time()-start)
'''
start = time.time()
img_cm = zlib.compress(img, 1)
print "Matrix Compression Time: ", (time.time()-start)
'''
start = time.time()
img_d_c_d = zlib.decompress(img_d_c)
print "Decompression Time: ", (time.time()-start)

print "Compression Ratio with Dumps: ", (len(img_d)/len(img_d_c))
print "Compression Ratio of Matrix: ", (len(img_d)/len(img_cm))
'''
print 'Length of Compressed Matrix String: ', len(img_cm)
img_cm_re = np.fromstring(zlib.decompress(img_cm), img.dtype)
img_cm_re = np.reshape(img_cm_re,(480,640))
cv2.imwrite('reconstruct_G640.png', img_cm_re)
print ""
print ""






# =========COLOR 640x480=========
print "=========COLOR 640x480========="
img = cv2.imread('capt_640_colo.png', 1)
'''
start = time.time()
img_d = dumps(img)
print "Dumping Time: ", (time.time()-start)

start = time.time()
img_d_c = zlib.compress(img_d, 1)
print "Compression Time: ", (time.time()-start)
'''
start = time.time()
img_cm = zlib.compress(img, 1)
print "Matrix Compression Time: ", (time.time()-start)
'''
start = time.time()
img_d_c_d = zlib.decompress(img_d_c)
print "Decompression Time: ", (time.time()-start)

print "Compression Ratio with Dumps: ", (len(img_d)/len(img_d_c))
print "Compression Ratio of Matrix: ", (len(img_d)/len(img_cm))
'''
print 'Length of Compressed Matrix String: ', len(img_cm)
img_cm_re = np.fromstring(zlib.decompress(img_cm), img.dtype)
img_cm_re = np.reshape(img_cm_re,(480,640,3))
cv2.imwrite('reconstruct_C640.png', img_cm_re)

print ""
print ""

# =========GRAY 320x240=========
print "=========GRAY 320x240========="
img = cv2.imread('capt_320_gray.png', 0)
'''
start = time.time()
img_d = dumps(img)
print "Dumping Time: ", (time.time()-start)

start = time.time()
img_d_c = zlib.compress(img_d, 1)
print "Compression Time: ", (time.time()-start)
'''
start = time.time()
img_cm = zlib.compress(img, 1)
print "Matrix Compression Time: ", (time.time()-start)
'''
start = time.time()
img_d_c_d = zlib.decompress(img_d_c)
print "Decompression Time: ", (time.time()-start)

print "Compression Ratio with Dumps: ", (len(img_d)/len(img_d_c))
print "Compression Ratio of Matrix: ", (len(img_d)/len(img_cm))
'''
print 'Length of Compressed Matrix String: ', len(img_cm)
img_cm_re = np.fromstring(zlib.decompress(img_cm), img.dtype)
img_cm_re = np.reshape(img_cm_re,(240, 320))
cv2.imwrite('reconstruct_G320.png', img_cm_re)

print ""
print ""


# =========COLOUR 320x240=========
print "=========COLOR 320x240========="
img = cv2.imread('capt_320_colo.png', 1)

'''
start = time.time()
img_d = dumps(img)
print "Dumping Time: ", (time.time()-start)

start = time.time()
img_d_c = zlib.compress(img_d, 1)
print "Compression Time: ", (time.time()-start)
'''
start = time.time()
img_cm = zlib.compress(img, 1)
print "Matrix Compression Time: ", (time.time()-start)
'''
start = time.time()
img_d_c_d = zlib.decompress(img_d_c)
print "Decompression Time: ", (time.time()-start)

print "Compression Ratio with Dumps: ", (len(img_d)/len(img_d_c))
print "Compression Ratio of Matrix: ", (len(img_d)/len(img_cm))
'''
print 'Length of Compressed Matrix String: ', len(img_cm)
img_cm_re = np.fromstring(zlib.decompress(img_cm), img.dtype)
img_cm_re = np.reshape(img_cm_re,(240, 320,3))
cv2.imwrite('reconstruct_C320.png', img_cm_re)

print ""
print ""
