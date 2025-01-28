from flask import Flask, request, send_from_directory, render_template
import os
import qrcode

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".glb"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Use the local IP address instead of localhost
            ip_address = request.host.split(':')[0]
            viewer_url = f"http://{ip_address}:5000/view/{file.filename}"

            # Generate QR Code pointing directly to the 3D viewer
            qr = qrcode.make(viewer_url)
            qr_path = os.path.join("static", "qr_code.png")
            qr.save(qr_path)

            return render_template("index.html", qr_code=qr_path, viewer_url=viewer_url)
    return render_template("index.html")


@app.route("/view/<filename>")
def view_3d_model(filename):
    file_url = f"{request.host_url}uploads/{filename}"
    return render_template("view_3d.html", file_url=file_url)


@app.route("/uploads/<path:filename>")
def serve_file(filename):
    # Serve GLB files with the correct MIME type
    if filename.endswith(".glb"):
        return send_from_directory(UPLOAD_FOLDER, filename, mimetype="model/gltf-binary")
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
