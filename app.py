# 経費精算システム - バックエンド (Flask)

from flask import Flask, request, jsonify
import os
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'feedback': 'ファイルが選択されていません。'}), 400

    file = request.files['file']
    category = request.form.get('category', '')

    if file.filename == '':
        return jsonify({'feedback': '有効なファイルを選択してください。'}), 400

    # ファイルの保存
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    feedback_message = ''

    try:
        # 画像ファイルの処理
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = pytesseract.image_to_string(Image.open(save_path))
            feedback_message = f'読み取った内容: {text}'

        # PDFファイルの処理
        elif filename.lower().endswith('.pdf'):
            reader = PdfReader(save_path)
            text = ''.join([page.extract_text() for page in reader.pages])
            feedback_message = f'読み取った内容: {text}'

        else:
            feedback_message = '対応していないファイル形式です。'

    except Exception as e:
        feedback_message = f'エラーが発生しました: {str(e)}'

    return jsonify({'feedback': feedback_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
