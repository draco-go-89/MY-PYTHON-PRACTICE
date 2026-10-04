# pip install qrcode[pil] 
import qrcode
url = input("Enter: ").strip()
img = qrcode.make(url)
img.save("qr_code.png")
print("QR code Generated!")