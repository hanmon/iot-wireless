from processing_py import *
app=App(320,240)
def setup():
    global img
  # Make a new instance of a PImage by loading an image file
  # Declaring a variable of type PImage
    img = app.loadImage("mysummervacation.jpg")

def draw():
    global img
    app.background(0)
    # Draw the image to the screen at coordinate (0,0)
    app.image(img,0,0)

setup()
draw()