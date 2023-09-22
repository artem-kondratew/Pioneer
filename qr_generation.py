import qrcode

data = "test generation for opencv"
filename = "qrcode.png"
img = qrcode.make(data)
img.save(filename)
