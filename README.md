🚦 E-Challan Generator (AI-Based Number Plate Detection System)
📌 Project Overview

The E-Challan Generator is an AI-powered web application designed to automate the process of traffic challan generation using Automatic Number Plate Recognition (ANPR) and Optical Character Recognition (OCR). The system detects vehicle number plates from uploaded images, extracts the registration number, identifies violations, and generates a digital challan instantly.

This project helps traffic authorities reduce manual workload, improve accuracy, and speed up challan issuance using automation and AI technology.

🚀 Features
🚗 Automatic Number Plate Detection (ANPR)
🔍 OCR-based Number Extraction
🧠 AI-based Text Recognition
📄 Auto Challan Generation
🧾 PDF Challan Download
💾 Database Storage (Violation Records)
👤 Owner & Vehicle Details Management
📊 Simple Admin Dashboard
📷 Image Upload & Processing
⚡ Fast & Automated Processing
🛠 Technologies Used
Technology	Purpose
Python	Backend Logic
Streamlit	Web UI
OpenCV	Image Processing
EasyOCR / Tesseract	Text Extraction (OCR)
YOLO (Optional)	Number Plate Detection
SQLite / MySQL	Database Management
ReportLab	PDF Generation
Pandas	Data Handling
🧠 Working Process
User uploads vehicle image
System detects number plate region (ANPR)
OCR extracts vehicle number
System checks violation rules
Challan details are generated automatically
Data is stored in database
PDF challan is created and downloaded
📂 Project Structure
E-Challan-Generator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── ocr_reader.py
│   ├── plate_detector.py
│
├── utils/
│   ├── database.py
│   ├── challan_generator.py
│
├── data/
│   ├── sample_images/
│
├── output/
│   ├── challans/
│
└── venv/
⚙️ Installation
Step 1: Clone Repository
git clone https://github.com/your-username/e-challan-generator.git
Step 2: Move into Project Folder
cd e-challan-generator
Step 3: Create Virtual Environment
python -m venv venv
Step 4: Activate Environment

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate
Step 5: Install Dependencies
pip install -r requirements.txt
▶️ Run the Project
streamlit run app.py
📄 Supported Inputs
Vehicle Images (JPG, PNG)
Clear number plate photos
📊 Output Features
Detected Vehicle Number
Owner Details
Violation Type
Fine Amount
Generated PDF Challan
📈 Future Enhancements
📹 Real-time CCTV integration
🚓 Automatic traffic monitoring system
☁ Cloud database support
📱 Mobile app version
🤖 Deep learning-based YOLOv8 detection
🧾 Smart challan payment gateway integration
🎯 Applications
Traffic Police Departments
Smart City Projects
Highway Monitoring Systems
Automated Law Enforcement
Parking Violation Systems
🔐 Advantages
Reduces manual work
Increases accuracy
Faster challan generation
Paperless system
Easy record management
⚠️ Limitations
Requires clear images for OCR accuracy
Depends on lighting conditions
Needs proper dataset for better detection
👨‍💻 Author

Developed by: Diljeet Kaur
