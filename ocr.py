import cv2
import numpy as np


def find_th(img):
    difference = 10
    th = 255/2
    while(difference > 0.01):
        mean1 = np.mean(img[img < th])
        mean2 = np.mean(img[img >= th])
        th_new = 0.5*(mean2+mean1)
        difference = abs(th - th_new)
        # print("difference: ", difference,"TH: ", th_new)
        th = th_new
    return th_new


def cutting_row(page):
    row_list = []
    flag = False
    for i in range(page.shape[0] - 1):
        if 0 in page[i, :] and not flag:
            row_list.append(i - 1)
            flag = True
        elif 0 not in page[i, :] and flag:
            row_list.append(i + 1)
            flag = False
    return row_list


def cutting_letters(word):
    cuts_list = []
    flag = False
    for i in range(word.shape[1] - 1):
        if 0 in word[:, i] and not flag:
            cuts_list.append(i)
            flag = True
        elif list(word[:, i]).count(0) < 2 and flag:
            cuts_list.append(i)
            flag = False
    return cuts_list


def show_row(page, list):
    row = []
    for i in range(0, len(list), 2):
        # cv2.imshow('word1', page[list[i]:list[i + 1], :])
        # cv2.waitKey(0)
        row.append(page[list[i]:list[i + 1], :])
    return row


def show_letters(word, list):
    letter = []
    for i in range(0, len(list), 2):
        cv2.imshow('word1', word[:, list[i]:list[i + 1]])
        cv2.waitKey(0)
        letter.append(word[:, list[i]:list[i + 1]])
    return letter


image = cv2.imread('page3.png')
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# image = cv2.GaussianBlur(image, (5, 5), 0.5)
th = find_th(image)
image[image <= th*1.1] = 0
image[image > th] = 255
m, n = image.shape

cv2.imshow('word', image)
cv2.waitKey(0)

cut_row = cutting_row(image)
row_list = show_row(image, cut_row)
for i in range(len(row_list)):
    cuts_list = cutting_letters(row_list[i])
    print(cuts_list)
    show_letters(row_list[i], cuts_list)

