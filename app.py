import os
import markdown
from flask import Flask, render_template, abort

app = Flask(__name__)

PROJECTS_FOLDER = 'projects'

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', active_page='about')

@app.route('/contacts')
def contacts():
    """Страница контактов"""
    return render_template('contacts.html', active_page='contacts')

@app.route('/projects')
def projects_list():
    """Список проектов из папки .md файлов"""
    if not os.path.exists(PROJECTS_FOLDER):
        os.makedirs(PROJECTS_FOLDER)
        
    files = os.listdir(PROJECTS_FOLDER)
    md_files = [f for f in files if f.endswith('.md')]
    
    projects = []
    for filename in sorted(md_files, reverse=True):  # Новые сверху
        filepath = os.path.join(PROJECTS_FOLDER, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Парсим заголовок из первой строки (# Заголовок)
        lines = content.split('\n')
        title = lines[0].lstrip('#').strip() if lines and lines[0].startswith('#') else filename
        
        projects.append({
            'filename': filename,
            'title': title
        })
    
    return render_template('projects.html', projects=projects, active_page='projects')

@app.route('/projects/<filename>')
def project_detail(filename):
    """Просмотр конкретного проекта"""
    filepath = os.path.join(PROJECTS_FOLDER, filename)
    
    if not os.path.exists(filepath) or not filename.endswith('.md'):
        abort(404)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Парсим заголовок
    lines = content.split('\n')
    title = lines[0].lstrip('#').strip() if lines and lines[0].startswith('#') else filename
    
    # Конвертируем Markdown в HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    return render_template('projects.html', 
                         projects=[], 
                         current_project={'title': title, 'content': html_content},
                         active_page='projects')

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('woz_cert.pem', 'woz_pk.pem'))
    app.run()