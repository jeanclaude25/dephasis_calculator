import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api

def grab_screen(window_title):
    hwin = win32gui.FindWindow(None, window_title)
    if hwin:
        left, top, right, bot = win32gui.GetClientRect(hwin)
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, right - left, bot - top)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (right - left, bot - top), srcdc, (0, 0), win32con.SRCCOPY)
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (bot - top, right - left, 4)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def find_offset(frame1, frame2):
    difference = cv2.absdiff(frame1, frame2)
    difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    result = cv2.matchTemplate(difference, difference, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    offset_x = max_loc[0]
    offset_y = max_loc[1]
    return offset_x, offset_y

if __name__ == "__main__":
    frame1 = grab_screen("Window Title")
    frame2 = grab_screen("Window Title")
    offset_x, offset_y = find_offset(frame1, frame2)
    print("Offset X:", offset_x)
    print("Offset Y:", offset_y)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
