from PIL import Image, ImageDraw

img = Image.new("RGB", (800, 400), "white")
draw = ImageDraw.Draw(img)
text = (
    "MOCK STORE\n"
    "Invoice: INV-001\n"
    "2x Widget @ 3.50\n"
    "Subtotal: 7.00\n"
    "Tax: 0.63\n"
    "Total: 7.63\n"
    "Paid: VISA ****1111"
)
draw.text((40, 40), text, fill="black")
img.save("sample.png")
print("Wrote sample.png")
