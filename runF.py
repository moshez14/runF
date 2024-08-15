from flask import Flask, request, render_template_string, redirect, url_for
import subprocess
import re

app = Flask(__name__)

# Define the path to the script file
file_path = '/home/ubuntu/livestream/exec_ffmpeg.sh'

# Function to extract RTMP codes from the script file
def get_rtmp_codes():
    rtmp_codes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        match = re.search(r'rtmp://localhost:1935/live_hls/(\S+)', line)
        if match:
            rtmp_codes.append(match.group(1))
    return rtmp_codes

# Function to execute the corresponding command for the selected RTMP code
def run_ffmpeg_for_camera(camera_rtmp):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if camera_rtmp in line:
            print(f"Executing in background: {line.strip()}")
            # Run the command in the background
            subprocess.Popen(line.strip(), shell=True)
            return f"Started: {line.strip()}"
    return f"No matching RTMP stream found for: {camera_rtmp}"

@app.route('/', methods=['GET'])
def index():
    rtmp_codes = get_rtmp_codes()
    return render_template_string(open('index.html').read(), rtmp_codes=rtmp_codes)

@app.route('/run_ffmpeg', methods=['POST'])
def run_ffmpeg():
    message=request.json
    camera_rtmp = message['camera_rtmp']
    #camera_rtmp = request.form['camera_rtmp']
    print(f"camera_rtmp={camera_rtmp}")
    result = run_ffmpeg_for_camera(camera_rtmp)
    print(result)
    return redirect(url_for('index'))

@app.route('/run_camera', methods=['POST'])
def run_camera():
    camera_rtmp = request.form['camera_rtmp']
    print(f"camera_rtmp={camera_rtmp}")
    result = run_ffmpeg_for_camera(camera_rtmp)
    print(result)
    return redirect(url_for('index'))

if __name__ == "__main__":
    cert_file = "/home/ubuntu/certs/8907a39044534c57.crt"
    key_file = "/home/ubuntu/certs/8907a39044534c57.pem"
    ca_bundle = "/home/ubuntu/certs/gd_bundle-g2-g1.crt"
    app.run(host="0.0.0.0", port=5900)

