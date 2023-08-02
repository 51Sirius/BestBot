import cv2
import requests
import PIL


def save_img_with_url(image, name):
    try:
        resp = requests.get(image, stream=True).raw
    except requests.exceptions.RequestException:
        print('Error')
    try:
        img = PIL.Image.open(resp)
    except IOError:
        print("Unable to open image")
    img.save(name, 'JPEG')


def convert_to_multi(image, name):
    save_img_with_url(image, name)
    img = cv2.imread(name)
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayimg = cv2.medianBlur(grayimg, 5)

    edges = cv2.Laplacian(grayimg, cv2.CV_8U, ksize=5)
    r, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    img2 = cv2.bitwise_and(img, img, mask=mask)
    img2 = cv2.medianBlur(img2, 5)
    cv2.imwrite(name, mask)
