from djitellopy import tello
from time import sleep
import cv2
import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400,400))

def getKey(keyname):
        ans = False
        for eve in pygame.event.get(): pass
        keyInput = pygame.key.get_pressed()
        mykey = getattr(pygame, 'K_{}'.format(keyname))
        if keyInput[mykey]:
            ans= True
            pygame.display.update()

        return ans

def main():
    if getKey("LEFT"):
        print("YOU PRESSED LEFT KEY")

if __name__ == '__main__':
    init()
    while True:
     main()

