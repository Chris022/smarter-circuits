# Smarter Circuits #
import imagePreprocessing as ip
import utils

image = utils.loadImage(path="./../src/testImages",name="raf1.png")

preprocessedImage = ip.preprocessImage(image)

utils.saveImage(name="preprocessed.png", image=preprocessedImage)