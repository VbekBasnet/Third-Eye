import cv2 as cv



def rescaleFrame(frame, scale= 0.2):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)

img = cv.imread("Photos/Isle.jpg")
cv.imshow("FilmImage", img)

resized_image = rescaleFrame(img)
cv.imshow("resized Image", resized_image)

#Videos:

capture = cv.VideoCapture("Photos/meme.mp4")

while True:
    isTrue, frame = capture.read()
    resized_video = rescaleFrame(frame)

    cv.imshow("video", frame)
    cv.imshow("resized video", resized_video)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()


cv.waitKey(0)
