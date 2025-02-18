from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import shutil
from werkzeug.utils import secure_filename
from image_operations import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS_TEXT = {'txt', 'md', 'py'}
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/enimg', exist_ok=True)  # Create static directory for encrypted images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename, file_type):
    if file_type == 'text':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_TEXT
    elif file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE
    return False

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Dummy login (replace with real authentication)
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename, 'text'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file (encrypt)
            encrypted_image = encrypt_file(filepath)
            
            # Move the image to the static folder
            static_image_path = 'static/' + encrypted_image
            if not os.path.exists(static_image_path):
                shutil.copy(encrypted_image, static_image_path)
            
            # Return success page with image path
            return render_template('encrypt_success.html', 
                                   filename=os.path.basename(encrypted_image),
                                   image_path=encrypted_image)
    
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename, 'image'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file (decrypt)
            decrypted_file = decrypt_file(filepath)
            
            # Read the content of the decrypted file
            with open(decrypted_file, 'r', encoding='utf-8') as f:
                decrypted_content = f.read()
            
            # Return success page with decrypted content
            return render_template('decrypt_success.html', 
                                   content=decrypted_content,
                                   filename=os.path.basename(decrypted_file))
    
    return render_template('decrypt.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)