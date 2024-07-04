from flask import *
from waitress import serve
from FilterFile import main
import os
app = Flask(__name__)
def clearFiles(path):
    for file in os.listdir(path): 
        os.remove(path+file)

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
        # Deleta arquivos salvos
        clearFiles(path)
        
        # Salva os novos arquivos
        file_initial.save(os.path.join('uploads', file_initial.filename))
        file_final.save(os.path.join('uploads', file_final.filename))
        print(file_initial.filename)
        file_initial_path = path+file_initial.filename
        file_final_path = path+file_final.filename
        # Chama a função main() passando os caminhos dos arquivos
        main(file_initial_path=file_initial_path, file_final_path=file_final_path, name_file= name_result)
        
    return render_template("resultado.html")
if __name__ == "__main__":
    app.run(debug=True)