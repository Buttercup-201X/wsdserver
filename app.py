from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import nanoid
import cv2
app = Flask(__name__)
CORS(app)
 

@app.route('/', methods=['GET', 'POST'])
def root():
    return '<h1>hello, world</h1>'

@app.route('/greet/<name>')
def greet(name):
    return f'hello, {name}!'

@app.route('/v1/photos', methods=['POST'])
def post_photos():
    if 'file' not in request.files:
        abort(400)
    
    file = request.files['file']
    if file.content_type != 'image/jpeg':
        abort(400)
        
    filename = f'{nanoid.generate(size=4)}.jpg'
    file.save(f'static/{filename}')
    img0 = cv2.imread(f'static/{filename}', cv2.IMREAD_GRAYSCALE)
    img1 = cv2.Canny(img0, 100, 200)
    cv2.imwrite(f'static/{filename}', img1)
    
    resp = {'url': f'/static/{filename}'}
    
    # 2つ目の画像の処理
    if 'preset_file' in request.files:
        preset_file = request.files['preset_file']
        if preset_file.content_type == 'image/jpeg':
            preset_filename = f'preset_{nanoid.generate(size=4)}.jpg'
            preset_file.save(f'static/{preset_filename}')
            preset_img0 = cv2.imread(f'static/{preset_filename}', cv2.IMREAD_GRAYSCALE)
            preset_img1 = cv2.Canny(preset_img0, 100, 200)
            cv2.imwrite(f'static/{preset_filename}', preset_img1)
            resp['preset_url'] = f'/static/{preset_filename}'
    
    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
