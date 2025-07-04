from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
# from werkzeug.urls import quote as url_quote
import os
from compare_files import compare_files

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保uploads目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件
        if 'file1' not in request.files or 'file2' not in request.files:
            return render_template('upload.html', error='没有选择文件')
        file1 = request.files['file1']
        file2 = request.files['file2']
        # 如果用户没有选择文件,浏览器也会提交一个没有文件名的空文件
        if file1.filename == '' or file2.filename == '':
            return render_template('upload.html', error='没有选择文件')
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file1_path = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
            file2_path = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
            file1.save(file1_path)
            file2.save(file2_path)
            
            try:
                # 比较文件
                result, output_path = compare_files(file1_path, file2_path)
                if output_path:
                    return send_file(output_path, as_attachment=True, download_name='comparison_result.xlsx')
                else:
                    return render_template('upload.html', message=result)
            except Exception as e:
                return render_template('upload.html', error=f"比较文件时发生错误: {str(e)}")
            finally:
                # 删除上传的文件
                os.remove(file1_path)
                os.remove(file2_path)
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
