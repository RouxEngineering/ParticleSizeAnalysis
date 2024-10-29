from flask import Flask, request, redirect, url_for, render_template
import os


#initialize application 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Call your Python image processing function here
        process_image(filepath)
        return 'File uploaded and processed successfully.'

def process_image(filepath):
    # Your image processing code here
    print(f'Processing file: {filepath}')

if __name__ == '__main__':
    app.run(debug=True)