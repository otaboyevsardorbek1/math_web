from flask import Flask, request, render_template, redirect, send_file, jsonify
from base_func import (newton_raphson,iterate_values,file_path)
import json
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/math/<url>', methods=['GET', 'POST'])
def base_urls(url):
    data = request.base_url
    results = []
    if request.method == 'POST': 
        try:
            func1 = request.form.get('func1')  
            func2 = request.form.get('func2')  
            start_x = float(request.form.get('start_x'))
            start_y = float(request.form.get('start_y'))
            epsilon = float(request.form.get('Epslon'))
            if str(url) ==str('itaratsiya'):
                results = iterate_values(func1, func2, start_x, start_y, epsilon)
                json_path = file_path('itaratsiya.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({'iterations': results}, f, indent=4)
                return render_template(
                'itaratsiya.html',results=results,data=data,error=None)
            elif str(url)==str('nyuton_itaratsiya'):
                results = newton_raphson(func1, func2, start_x, start_y, epsilon)
                json_path = file_path('nyuton_itaratsiya.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({'iterations': results}, f, indent=4)
                return render_template('nuyuton_itaratsiya.html',results=results,data=data,error=None)
            else:
                return redirect('/')
  
        except Exception as e:
            return render_template('input.html', error=str(e),data=data, results=[])

    return render_template('input.html', results=[],data=data,error=None)


@app.route('/developer')
def developer():
    return render_template('developer.html')
# JSON yuklab olish
@app.route('/download/<file_name>')
def download_file(file_name):
    try:
        json_path = file_path(f'{file_name}.json')
        return send_file(json_path, as_attachment=True, download_name=f'{file_name}.json', mimetype='application/json')
    except Exception:
        return redirect('/')

# API orqali natijalarni olish
@app.route('/api/<data_name>')
def get_results(data_name):
    try:
        json_path = file_path(f'{data_name}.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run()
