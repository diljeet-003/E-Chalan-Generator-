import os
import uuid
from reportlab.pdfgen import canvas

def generate_challan(vehicle_number, owner_name, violation, fine_amount):

    # 1. Create folder if not exists
    folder = "static/challans"
    os.makedirs(folder, exist_ok=True)

    # 2. SAFE filename (NEVER empty)
    file_name = f"challan_{uuid.uuid4().hex}.pdf"
    file_path = os.path.join(folder, file_name)

    # 🔍 DEBUG (optional but useful)
    print("Generated file path:", file_path)

    # 3. Create PDF canvas
    pdf = canvas.Canvas(file_path)

    # 4. Write content
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "🚔 E-CHALLAN REPORT")
    pdf.drawString(100, 770, f"Vehicle Number: {vehicle_number}")
    pdf.drawString(100, 750, f"Owner Name: {owner_name}")
    pdf.drawString(100, 730, f"Violation: {violation}")
    pdf.drawString(100, 710, f"Fine Amount: ₹{fine_amount}")

    # 5. Save PDF
    pdf.save()

    return file_path