# pip install qrcode[pil] 
import qrcode
url = input("Enter: ").strip()
img = qrcode.make(url)
img.save("qr_code.png")
print("\n--- QR code Generated! Saved in file ---")