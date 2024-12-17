class Image:
    def __init__(self, height, width, pixels):
        self.height = height
        self.width = width
        self.pixels = pixels
    
    def getPixel(self, x, y):
        return self.pixels[y*self.width + x]
    
    def setPixel(self, x, y, val):
        self.pixels[y*self.width + x] = val
