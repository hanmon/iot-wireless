import cv2
import sys
import numpy as np
filepath1 = sys.argv[1]
filepath2 = sys.argv[2]
image1 = cv2.imread(filepath1)
image2 = cv2.imread(filepath2)
max_height = max(image1.shape[0], image2.shape[0])
resized_image1 = cv2.resize(image1, (int(image1.shape[1] * max_height / image1.shape[0]), max_height))
resized_image2 = cv2.resize(image2, (int(image2.shape[1] * max_height / image2.shape[0]), max_height))
numpy_horizontal = np.hstack((resized_image1, resized_image2))
cv2.imshow("preview", numpy_horizontal)
cv2.waitKey(0)
cv2.destroyAllWindows()