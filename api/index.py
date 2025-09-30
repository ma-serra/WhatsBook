#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask API for WhatsBook - WhatsApp chat parser for Vercel deployment
"""
from flask import Flask, request, jsonify, render_template, send_file
import os
import sys
import tempfile
import zipfile
from werkzeug.utils import secure_filename

# Add parent directory to path to import whatsBook module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

ALLOWED_EXTENSIONS = {'zip', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsBook - WhatsApp Chat Parser</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 0.95em;
            }
            .upload-area {
                border: 2px dashed #667eea;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                background: #f8f9ff;
                margin: 20px 0;
                cursor: pointer;
                transition: all 0.3s;
            }
            .upload-area:hover {
                border-color: #764ba2;
                background: #f0f1ff;
            }
            .upload-area.dragover {
                border-color: #764ba2;
                background: #e8e9ff;
            }
            input[type="file"] {
                display: none;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
                width: 100%;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .status.processing {
                background: #fff3cd;
                color: #856404;
                border: 1px solid #ffeaa7;
            }
            .info-box {
                background: #e8f4f8;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
                border-left: 4px solid #667eea;
            }
            .info-box h3 {
                margin-top: 0;
                color: #333;
            }
            .info-box ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            .info-box li {
                margin: 5px 0;
                color: #555;
            }
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 10px auto;
                display: none;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .file-info {
                margin-top: 15px;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 5px;
                display: none;
            }
            code {
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 WhatsBook</h1>
            <p class="subtitle">WhatsApp Chat Parser for LaTeX</p>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="upload-area" id="uploadArea">
                    <p>📁 Drop your WhatsApp chat export here or click to browse</p>
                    <p style="font-size: 0.9em; color: #666;">Accepts .zip files or _chat.txt files</p>
                    <input type="file" id="fileInput" name="file" accept=".zip,.txt">
                </div>
                
                <div class="file-info" id="fileInfo"></div>
                
                <button type="submit" class="btn" id="submitBtn">Convert to LaTeX</button>
            </form>
            
            <div class="loader" id="loader"></div>
            <div class="status" id="status"></div>
            
            <div class="info-box">
                <h3>ℹ️ How to use:</h3>
                <ul>
                    <li>Open WhatsApp on your phone</li>
                    <li>Go to the chat you want to export</li>
                    <li>Tap the menu (⋮) → More → Export chat</li>
                    <li>Choose "Without Media" or "With Media"</li>
                    <li>Save the file and upload it here</li>
                    <li>Download the generated LaTeX file</li>
                    <li>Use pdfLaTeX to compile it into a PDF</li>
                </ul>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('fileInput');
            const form = document.getElementById('uploadForm');
            const status = document.getElementById('status');
            const loader = document.getElementById('loader');
            const submitBtn = document.getElementById('submitBtn');
            const fileInfo = document.getElementById('fileInfo');

            // Click to upload
            uploadArea.addEventListener('click', () => fileInput.click());

            // Drag and drop
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    showFileInfo(files[0]);
                }
            });

            // Show file info when selected
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    showFileInfo(e.target.files[0]);
                }
            });

            function showFileInfo(file) {
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                fileInfo.innerHTML = `<strong>Selected file:</strong> ${file.name} (${sizeMB} MB)`;
                fileInfo.style.display = 'block';
            }

            function showStatus(message, type) {
                status.textContent = message;
                status.className = 'status ' + type;
                status.style.display = 'block';
            }

            // Form submission
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const file = fileInput.files[0];
                if (!file) {
                    showStatus('Please select a file first', 'error');
                    return;
                }

                const formData = new FormData();
                formData.append('file', file);

                // Show loading state
                submitBtn.disabled = true;
                loader.style.display = 'block';
                status.style.display = 'none';
                showStatus('Processing your chat... This may take a few minutes.', 'processing');

                try {
                    const response = await fetch('/api/convert', {
                        method: 'POST',
                        body: formData
                    });

                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'whatsbook_content.tex';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                        
                        showStatus('✅ Success! Your LaTeX file has been downloaded.', 'success');
                    } else {
                        const error = await response.json();
                        showStatus('❌ Error: ' + (error.error || 'Failed to process file'), 'error');
                    }
                } catch (error) {
                    showStatus('❌ Error: ' + error.message, 'error');
                } finally {
                    submitBtn.disabled = false;
                    loader.style.display = 'none';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/convert', methods=['POST'])
def convert():
    """Convert WhatsApp chat to LaTeX"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .zip or .txt file'}), 400
    
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(temp_dir, filename)
            file.save(file_path)
            
            # If it's a zip file, extract it
            if filename.endswith('.zip'):
                extract_dir = os.path.join(temp_dir, 'extracted')
                os.makedirs(extract_dir, exist_ok=True)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                chat_dir = extract_dir
            else:
                # If it's a txt file, use the temp directory
                chat_dir = temp_dir
            
            # Import and use the whatsBook parser
            try:
                import whatsBook as wb
                import argparse
                
                # Create arguments namespace
                arguments = argparse.Namespace()
                arguments.chatDir = chat_dir
                arguments.output = None  # Output to stdout
                arguments.cloud = False  # Don't generate word clouds for web
                
                # Parse the chat
                parsed_lines = list(wb.parseChat(arguments))
                
                # Create output file
                output_path = os.path.join(temp_dir, 'content.tex')
                with open(output_path, 'w', encoding='utf-8') as f:
                    for line in parsed_lines:
                        f.write(line + '\n')
                
                # Return the file
                return send_file(
                    output_path,
                    mimetype='text/plain',
                    as_attachment=True,
                    download_name='whatsbook_content.tex'
                )
                
            except Exception as e:
                return jsonify({'error': f'Error parsing chat: {str(e)}'}), 500
                
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'WhatsBook API'})

# Vercel serverless function handler
def handler(request):
    return app(request)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
