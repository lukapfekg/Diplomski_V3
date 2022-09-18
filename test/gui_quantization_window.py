from skimage.io import imread
from tkinterdnd2 import TkinterDnD

from gui.chooseColorSpace import ChooseColorSpace
from gui.gui import SecondScreen
from gui.quantization import QuantizeImage

root = TkinterDnD.Tk()
root.geometry('1500x900')

image = imread("../Examples/miner.jpg")
h, w, _ = image.shape
s = '1200x796;2;0;'

QuantizeImage(root, None, None, None, s)

root.mainloop()
