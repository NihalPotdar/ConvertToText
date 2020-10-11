import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Process the images for better results')
parser.add_argument('--image_path', type=str, help='the path of the image on the local filesystem', required=True)
args = parser.parse_args()

def rotation(img): # returns matrix
    rows,cols = img.shape

    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    dst = cv2.warpAffine(img,M,(cols,rows))

    return dst

def show_image(dst):
    cv2.imshow(args.image_path, dst)

def save_image(dst):
    cv2.imwrite(args.image_path, dst)

def sharpen(img):
    kernel = np.array([[9,9,9], [9,9,9], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)

    return img

def crop_image(img, h=0, w= 0):
    img = img[0:1000, 0:2150]

    return img

if __name__ == "__main__":
    img = cv2.imread(args.image_path,0)

    save_image(crop_image(img))

    #img = rotation(img)