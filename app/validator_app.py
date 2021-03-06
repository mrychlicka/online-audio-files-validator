import os

import helper
from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "%s" % (os.path.dirname(os.path.abspath(__file__)) + '/uploads')
ALLOWED_EXTENSIONS = 'wav'

validator_app = Flask(__name__)
validator_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@validator_app.route('/', methods=['GET', 'POST'])
def upload_site():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return render_template('no_file_added_site.html')
        if file and is_file_allowed(file.filename):
            sth = helper.valid_audio("%s/%s" % (UPLOAD_FOLDER, file.filename))
            filename = secure_filename(file.filename)
            file.save(os.path.join(validator_app.config['UPLOAD_FOLDER'], filename))
            sth_return = sth.split(" ")
            is_valid = sth_return[0]
            sample_number = " " if len(sth_return) == 1 else sth_return[1]
            return render_template('validation.html', filename=filename, is_valid=is_valid, sample_number=sample_number)
    return render_template('upload_site.html')


if __name__ == '__main__':
    validator_app.run(debug=True)
