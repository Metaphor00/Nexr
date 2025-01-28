from flask import Flask, render_template, request, redirect, url_for
import os
import qrcode
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/3d_models/'  # Save models in static directory
app.config['ALLOWED_EXTENSIONS'] = {'glb'}
CORS(app)
# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload 3D model
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Generate QR code
            viewer_url = request.url_root + f"view-model/{filename}"
            qr = qrcode.make(viewer_url)
            qr_path = os.path.join(app.config['UPLOAD_FOLDER'], "qrcode.png")
            qr.save(qr_path)
            return render_template('index.html', qr_code_path="static/3d_models/qrcode.png")
    return render_template('index.html')

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    return app.send_static_file(f'js/{filename}')


# Route to view 3D model
@app.route('/view-model/<filename>')
def view_model(filename):
    return render_template('viewer.html', model_file=f"static/3d_models/{filename}")
   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
