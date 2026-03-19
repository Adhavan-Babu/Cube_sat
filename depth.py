import cv2
import numpy as np

# Load images
imgL = cv2.imread('/home/nikhil/Cube_sat/images/test1.jpg', 0)  # Left image (grayscale)
imgR = cv2.imread('/home/nikhil/Cube_sat/images/test2.jpg', 0)

# Raspberry Pi Optimized Settings
# minDisparity: smallest shift to look for
# numDisparities: must be divisible by 16 (how many layers of height)
# blockSize: size of the window (usually 3, 5, or 7)
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=64, 
    blockSize=5,
    P1=8 * 3 * 5**2,
    P2=32 * 3 * 5**2
)

# Calculate the 'difference'
disparity = stereo.compute(imgL, imgR)

# Normalize for viewing (makes it a pretty grayscale image)

# 1. Normalize the disparity to the 0-255 range
disp_vis = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 2. Apply a colorful scheme
# COLORMAP_JET: Blue is low/far, Red is high/close
# COLORMAP_VIRIDIS: Purple is low, Yellow is high (very popular for scientific data)
color_disparity = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)

# 3. Save or Show
cv2.imwrite('height_map_color.jpg', color_disparity)
print("Height map saved as height_map.jpg")