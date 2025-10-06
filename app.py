from flask import Flask, render_template, jsonify, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
from flask_cors import CORS
from config import UPLOAD_FOLDER   # make sure config.py exists with UPLOAD_FOLDER path

app = Flask(__name__)
CORS(app)

# ========== File Upload ==========
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Empty filename'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(filepath)
    return jsonify({'status': 'success', 'filename': file.filename})

# ========== Load Data Helper ==========
def load_data():
    df = pd.read_csv("calculated_metrics.csv")
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    return df

# ========== Frontend ==========
@app.route('/')
def home():
    return render_template('index.html')  # templates/index.html must exist

# ========== API: Full Metrics ==========
@app.route('/api/metrics')
def get_metrics():
    df = load_data()
    return jsonify(df.to_dict(orient='records'))

# ========== API: Summary ==========
@app.route('/api/summary')
def get_summary():
    df = load_data()
    summary = {
        'total_sales': float(df['Sales'].sum()),
        'avg_profit': float(df['Profit'].mean()),
        'max_profit': float(df['Profit'].max()),
        'min_profit': float(df['Profit'].min()),
    }
    return jsonify(summary)

# ========== API: Chart ==========
@app.route('/api/chart', methods=['POST'])
def generate_chart():
    data = request.json
    chart_type = data.get('type', 'line')
    metric = data.get('metric', 'Sales')
    df = load_data()

    plt.figure(figsize=(10, 5))
    if chart_type == 'line':
        plt.plot(df["Date"], df[metric], marker='o', color='#1E90FF')
    elif chart_type == 'bar':
        plt.bar(df["Date"], df[metric], color='#1E90FF')

    plt.title(f"{metric} Over Time")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()

    return jsonify({'image': f'data:image/png;base64,{image_base64}'})

# ========== API: Trigger Metrics Calculation ==========
@app.route('/api/calculate-metrics')
def calculate_metrics():
    from metrics_calculator import main
    main()
    return jsonify({'status': 'success', 'message': 'Metrics calculated successfully'})

# ========== Run App ==========
if __name__ == '__main__':
    app.run(debug=True, port=5000)
