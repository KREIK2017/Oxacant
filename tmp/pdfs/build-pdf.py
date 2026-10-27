from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas


ROOT = Path(r"D:\Рабочий стол\projeckts\!AlpenPharma\Oxacant")
source = ROOT / "tmp" / "pdfs" / "oxacant-fullpage.png"
target = ROOT / "output" / "pdf" / "Oxacant-Advertorial-Fullpage.pdf"

with Image.open(source) as image:
    width_px, height_px = image.size

# Browser pixels are 96 dpi; PDF points are 72 dpi.
width_pt = width_px * 72 / 96
height_pt = height_px * 72 / 96

pdf = canvas.Canvas(str(target), pagesize=(width_pt, height_pt), pageCompression=1)
pdf.setTitle("Oxacant Advertorial – Full-page capture")
pdf.setAuthor("Oxacant project")
pdf.setSubject("Full-page visual export of the Oxacant advertorial")
pdf.drawImage(str(source), 0, 0, width=width_pt, height=height_pt, preserveAspectRatio=True)
pdf.showPage()
pdf.save()

print(target)
print(f"{width_px}x{height_px}px -> {width_pt:.2f}x{height_pt:.2f}pt")
