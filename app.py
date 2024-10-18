# from flask import Flask, request, render_template, redirect, url_for
# import os
# from src.main import rank_resumes
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# # Configuration for file uploads
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}

# # Check file extension
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Read file and handle encoding
# def read_file_as_text(file_path):
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         with open(file_path, 'r', encoding='latin-1') as f:
#             return f.read()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_files():
#     # Check if the form has files for resume and job description
#     if 'resume' not in request.files or 'job_description' not in request.files:
#         return redirect(url_for('index'))

#     resume_file = request.files['resume']
#     jd_file = request.files['job_description']

#     # Validate file extensions
#     if (resume_file and allowed_file(resume_file.filename) and 
#         jd_file and allowed_file(jd_file.filename)):
        
#         resume_filename = secure_filename(resume_file.filename)
#         jd_filename = secure_filename(jd_file.filename)
        
#         resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#         jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        
#         # Save files to the server
#         resume_file.save(resume_path)
#         jd_file.save(jd_path)
        
#         # Rank resumes based on the JD
#         score = rank_resumes(resume_path, jd_path)
        
#         # Render the result
#         return render_template('result.html', resume_filename=resume_filename,score=score)

#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)











# from flask import Flask, request, render_template, redirect, url_for
# import os
# from werkzeug.utils import secure_filename
# from src.main import rank_multiple_resumes  # Adjust the import path based on your project structure

# app = Flask(__name__)

# # Configuration for file uploads
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}

# # Helper function to check file extension
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Route for the homepage
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route to handle the upload and processing of files
# @app.route('/upload', methods=['POST'])
# def upload_files():
#     # Check if the form has files for resumes and job description
#     if 'resumes' not in request.files or 'job_description' not in request.files:
#         return redirect(url_for('index'))

#     jd_file = request.files['job_description']
#     resume_files = request.files.getlist('resumes')  # Get multiple resume files

#     # Validate file extensions
#     if jd_file and allowed_file(jd_file.filename):
#         jd_filename = secure_filename(jd_file.filename)
#         jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
#         jd_file.save(jd_path)  # Save the job description file

#         resume_paths = []
#         for resume_file in resume_files:
#             if resume_file and allowed_file(resume_file.filename):
#                 resume_filename = secure_filename(resume_file.filename)
#                 resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
#                 resume_file.save(resume_path)  # Save each resume file
#                 resume_paths.append(resume_path)

#         # Call the ranking function for multiple resumes
#         scores = rank_multiple_resumes(resume_paths, jd_path)

#         # Render the results in result.html
#         return render_template('result.html', scores=scores)

#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)








from flask import Flask, request, render_template, redirect, url_for
import os
import csv
from werkzeug.utils import secure_filename
from src.main import rank_multiple_resumes  # Assuming this function handles ranking
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_CSV = 'result.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}

# Utility to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to display the upload page
@app.route('/')
def index():
    return render_template('index.html')

# Handle file uploads
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'resumes' not in request.files or 'job_description' not in request.files:
        return redirect(url_for('index'))

    # Job Description file
    jd_file = request.files['job_description']

    # List of CV files
    resume_files = request.files.getlist('resumes')

    if jd_file and allowed_file(jd_file.filename):
        jd_filename = secure_filename(jd_file.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        jd_file.save(jd_path)

        resume_paths = []
        for resume_file in resume_files:
            if resume_file and allowed_file(resume_file.filename):
                resume_filename = secure_filename(resume_file.filename)
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
                resume_file.save(resume_path)
                resume_paths.append(resume_path)

        # Rank the resumes
        scores = rank_multiple_resumes(resume_paths, jd_path)

        # Save the result to CSV
        with open(RESULT_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['CV File Name', 'Score'])
            for resume, score in scores:
                writer.writerow([resume, score])

        # Render the result page and pass the scores
        return render_template('result.html', scores=scores)

    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
