from flask import *
import os
from FilterFile import main
app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/resultado", methods=['POST', 'GET'])
def result_join():
    if request.method == 'POST':
        path = 'uploads/'
        # Obtém arquivos
        file_initial = request.files['file-initial']
        file_final = request.files['file-final']
        name_result = request.form['name-file']
        
        # # Salva os novos arquivos
        # file_initial.save(os.path.join('uploads', file_initial.filename))
        # file_final.save(os.path.join('uploads', file_final.filename))
        
        # file_initial_path = path+file_initial.filename
        # file_final_path = path+file_final.filename
        # Chama a função main() passando os caminhos dos arquivos
        result_file = main(file_initial_obj=file_initial, file_final_obj=file_final, name_file= name_result)
        result_filename = name_result+".csv"
        # return render_template("resultado.html", result_filename=result_filename)
        return send_file(result_file, as_attachment=True, download_name=result_filename, mimetype='text/csv')
    
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join("downloads", filename)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)