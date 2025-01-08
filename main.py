from flask import Flask, request, render_template, redirect, url_for
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# Ana sayfa (Form)
@app.route('/')
def index():
    return render_template('index.html')

# Veriyi işleme ve kaydetme
@app.route('/submit', methods=['POST'])
def submit_data():
    data = {
        "sourceId": request.form['sourceId'],
        "sourceName": request.form['sourceName'],
        "sourceDetails": request.form['sourceDetails'],
        "sourceUrl": request.form['sourceUrl'],
        "timestamp": request.form['timestamp']
    }

    # XML dosyasına yazma
    if not os.path.exists('data.xml'):
        root = ET.Element('sources')
        tree = ET.ElementTree(root)
    else:
        tree = ET.parse('data.xml')
        root = tree.getroot()

    source = ET.SubElement(root, 'source')
    for key, value in data.items():
        ET.SubElement(source, key).text = value

    tree.write('data.xml')

    return redirect(url_for('index'))

# Rapor oluşturma
@app.route('/generate_report', methods=['POST'])
def generate_report():
    tree = ET.parse('data.xml')
    root = tree.getroot()

    report_data = [{
        "sourceId": source.find('id').text,
        "sourceUrl": source.find('url').text,
        "status": source.get('status', 'Unknown')
    } for source in root.findall('source')]

    save_report_to_txt(report_data)  # Bu fonksiyonu ayrıca tanımlamanız gerekebilir
    return "Report generated successfully."

if __name__ == '__main__':
    app.run(debug=True)