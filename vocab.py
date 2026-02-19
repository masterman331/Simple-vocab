import os
import json
import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from jinja2 import DictLoader

app = Flask(__name__)
app.secret_key = 'duolingo-replica-secret-key-change-me'

# -------------------------------------------------------------------
# Helper to load data
# -------------------------------------------------------------------
def load_vocabs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'vocabs.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# -------------------------------------------------------------------
# HTML / CSS / JS Templates (Embedded cleanly via DictLoader)
# -------------------------------------------------------------------
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DuoVocab Practice</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
        
        :root {
            --primary: #58cc02;
            --primary-shadow: #58a700;
            --secondary: #e5e5e5;
            --secondary-shadow: #cccccc;
            --text-main: #4b4b4b;
            --text-muted: #afafaf;
            --danger: #ff4b4b;
            --danger-shadow: #ea2b2b;
            --blue: #1cb0f6;
            --blue-shadow: #1899d6;
        }

        body {
            font-family: 'Nunito', sans-serif;
            background-color: #ffffff;
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            border-bottom: 2px solid var(--secondary);
        }

        .navbar h1 { margin: 0; font-size: 24px; color: var(--primary); font-weight: 800; cursor: pointer;}
        
        .nav-links a {
            text-decoration: none;
            color: var(--text-muted);
            font-weight: 700;
            margin-left: 20px;
            text-transform: uppercase;
            font-size: 14px;
            transition: color 0.2s;
        }

        .nav-links a:hover, .nav-links a.active { color: var(--blue); }

        .container {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            width: 100%;
            box-sizing: border-box;
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 0 var(--primary-shadow);
            text-transform: uppercase;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            transition: transform 0.1s, box-shadow 0.1s;
        }

        .btn:active {
            transform: translateY(4px);
            box-shadow: 0 0 0 transparent;
        }

        .btn-outline {
            background: white;
            color: var(--text-muted);
            border: 2px solid var(--secondary);
            box-shadow: 0 4px 0 var(--secondary);
        }

        .btn-outline:active { transform: translateY(4px); box-shadow: 0 0 0 transparent; }
        
        .btn-blue { background: var(--blue); box-shadow: 0 4px 0 var(--blue-shadow); }
        .btn-danger { background: var(--danger); box-shadow: 0 4px 0 var(--danger-shadow); }

        .title { text-align: center; margin-bottom: 30px; font-size: 28px; font-weight: 800;}
        
        /* Badges */
        .badge {
            font-size: 12px; padding: 4px 8px; border-radius: 8px; font-weight: bold; text-transform: uppercase;
            background: #eee; color: #888;
        }
        .badge.phrase { background: #dceefc; color: #1cb0f6; }
        .badge.noun { background: #fce4e4; color: #ff4b4b; }
        .badge.verb { background: #e4fce4; color: #58cc02; }
        .badge.adjective { background: #fcf4e4; color: #ffc800; }
        
        /* Dictionary elements */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px;}
        .stat-card { border: 2px solid var(--secondary); border-radius: 16px; padding: 20px; text-align: center; }
        .stat-card h3 { margin: 0 0 10px 0; font-size: 32px; color: var(--blue); }
        .stat-card p { margin: 0; color: var(--text-muted); font-weight: bold; text-transform: uppercase; font-size: 12px;}
        
        .search-box { width: 100%; padding: 15px; border: 2px solid var(--secondary); border-radius: 16px; font-size: 16px; margin-bottom: 20px; box-sizing: border-box; font-family: inherit;}
        .search-box:focus { outline: none; border-color: var(--blue); }

        table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
        th { text-align: left; padding: 10px 15px; color: var(--text-muted); text-transform: uppercase; font-size: 14px;}
        td { padding: 15px; background: white; border-top: 2px solid var(--secondary); border-bottom: 2px solid var(--secondary); }
        td:first-child { border-left: 2px solid var(--secondary); border-top-left-radius: 16px; border-bottom-left-radius: 16px; font-weight: bold;}
        td:last-child { border-right: 2px solid var(--secondary); border-top-right-radius: 16px; border-bottom-right-radius: 16px; }

    </style>
</head>
<body>
    <div class="navbar">
        <h1 onclick="window.location.href='/'">DuoVocab</h1>
        <div class="nav-links">
            <a href="/">Learn</a>
            <a href="/dictionary">Dictionary</a>
            <a href="/custom">Custom Training</a>
        </div>
    </div>
    
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
{% extends "base.html" %}
{% block content %}
<style>
    .lesson-card {
        border: 2px solid var(--secondary);
        border-radius: 20px;
        padding: 20px 25px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
    }
    .lesson-info h2 { margin: 0 0 5px 0; font-size: 20px; }
    .lesson-info p { margin: 0; color: var(--text-muted); font-size: 14px; font-weight: bold;}
    .lesson-actions { display: flex; gap: 10px; }
    .completed { background-color: #f7f7f7; border-color: #eee; }
    .completed .lesson-info h2 { color: var(--text-muted); text-decoration: line-through; }
</style>

<div style="display: flex; justify-content: space-between; align-items: center;">
    <h2 class="title" style="margin: 0;">Syllabus</h2>
    <form method="POST" action="/reset" style="margin:0;">
        <button type="submit" class="btn btn-outline" style="padding: 8px 15px; font-size: 12px;">Reset Progress</button>
    </form>
</div>
<br>

{% if not lessons %}
    <div style="text-align:center; padding: 50px; border: 2px dashed var(--secondary); border-radius: 20px;">
        <h3 style="color: var(--danger);">vocabs.txt not found!</h3>
        <p>Please place the <b>vocabs.txt</b> file in the same directory as this script and refresh.</p>
    </div>
{% endif %}

{% for i, lesson in lessons %}
    <div class="lesson-card {% if str(i) in completed %}completed{% endif %}">
        <div class="lesson-info">
            <h2>{{ lesson.lesson_name }}</h2>
            <p>{{ lesson.words|length }} Words / Phrases</p>
        </div>
        <div class="lesson-actions">
            {% if str(i) not in completed %}
                <form method="POST" action="/skip/{{ i }}"><button class="btn btn-outline" type="submit">Skip</button></form>
            {% else %}
                <form method="POST" action="/unskip/{{ i }}"><button class="btn btn-outline" type="submit">Undo</button></form>
            {% endif %}
            <a href="/practice?lesson_id={{ i }}" class="btn">Start</a>
        </div>
    </div>
{% endfor %}
{% endblock %}
"""

DICTIONARY_TEMPLATE = """
{% extends "base.html" %}
{% block content %}
<h2 class="title">Dictionary & Glossary</h2>

<div class="stats-grid">
    <div class="stat-card">
        <h3>{{ total_words }}</h3>
        <p>Total Items</p>
    </div>
    <div class="stat-card">
        <h3>{{ stats.Phrase | default(0) }}</h3>
        <p>Phrases</p>
    </div>
    <div class="stat-card">
        <h3>{{ stats.Noun | default(0) }}</h3>
        <p>Nouns</p>
    </div>
    <div class="stat-card">
        <h3>{{ stats.Verb | default(0) }}</h3>
        <p>Verbs</p>
    </div>
</div>

<input type="text" id="searchInput" class="search-box" placeholder="Search in Spanish, Czech, or Notes..." onkeyup="filterTable()">

<table id="vocabTable">
    <thead>
        <tr>
            <th>Spanish</th>
            <th>Czech</th>
            <th>Type</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        {% for word in all_words %}
        <tr>
            <td>{{ word.spanish }}</td>
            <td>{{ word.czech }}</td>
            <td><span class="badge {{ word.type.lower() }}">{{ word.type }}</span></td>
            <td style="color: var(--text-muted); font-size: 14px;">{{ word.notes }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<script>
function filterTable() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let rows = document.getElementById("vocabTable").getElementsByTagName("tr");
    
    for (let i = 1; i < rows.length; i++) {
        let text = rows[i].innerText.toLowerCase();
        rows[i].style.display = text.includes(input) ? "" : "none";
    }
}
</script>
{% endblock %}
"""

CUSTOM_TRAINING_TEMPLATE = """
{% extends "base.html" %}
{% block content %}
<style>
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-bottom: 30px;}
    .custom-label {
        display: block; border: 2px solid var(--secondary); border-radius: 16px; padding: 15px; 
        cursor: pointer; font-weight: bold; transition: all 0.2s;
    }
    .custom-label:hover { border-color: var(--blue); }
    .custom-label input { margin-right: 10px; transform: scale(1.2); }
</style>

<h2 class="title">Custom Training</h2>
<p style="text-align:center; color: var(--text-muted); margin-bottom: 30px;">Select specific lessons to combine into one ultimate practice session.</p>

<form action="/practice" method="GET">
    <div class="grid">
        {% for i, lesson in lessons %}
        <label class="custom-label">
            <input type="checkbox" name="custom_lessons" value="{{ i }}">
            {{ lesson.lesson_name.split(':')[0] }}
        </label>
        {% endfor %}
    </div>
    <div style="text-align: center;">
        <button type="submit" class="btn btn-blue" style="width: 100%; max-width: 300px;">Start Custom Practice</button>
    </div>
</form>
{% endblock %}
"""

PRACTICE_TEMPLATE = """
{% extends "base.html" %}
{% block content %}
<style>
    .progress-bar-bg { width: 100%; height: 16px; background: var(--secondary); border-radius: 8px; margin-bottom: 40px; overflow: hidden;}
    .progress-bar-fill { height: 100%; background: var(--primary); width: 0%; transition: width 0.3s ease; }
    
    .question-box { text-align: center; margin-bottom: 40px; }
    .question-title { font-size: 20px; color: var(--text-muted); font-weight: bold; text-transform: uppercase; margin-bottom: 10px;}
    .question-word { font-size: 32px; font-weight: 800; }
    
    .options-grid { display: flex; flex-direction: column; gap: 15px; }
    .option-btn {
        background: white; border: 2px solid var(--secondary); border-radius: 16px; padding: 15px 20px;
        font-size: 18px; font-weight: bold; color: var(--text-main); cursor: pointer; text-align: left;
        box-shadow: 0 4px 0 var(--secondary); transition: all 0.1s;
    }
    .option-btn:hover { background: #f7f7f7; }
    .option-btn:active { transform: translateY(4px); box-shadow: 0 0 0 transparent; }
    
    .option-btn.correct { border-color: var(--primary); background: #eaffd0; color: #58a700; box-shadow: 0 4px 0 var(--primary-shadow); }
    .option-btn.wrong { border-color: var(--danger); background: #ffebeb; color: #ea2b2b; box-shadow: 0 4px 0 var(--danger-shadow); }
    .option-btn:disabled { cursor: not-allowed; }

    .bottom-bar {
        position: fixed; bottom: 0; left: 0; width: 100%; padding: 20px; background: white;
        border-top: 2px solid var(--secondary); display: flex; justify-content: space-between; align-items: center;
        box-sizing: border-box; display: none;
    }
    .bottom-bar.active { display: flex; }
    .bottom-bar.correct-bar { background: #d7ffb8; border-color: #c0f296; color: #58a700;}
    .bottom-bar.wrong-bar { background: #ffdfe0; border-color: #ffc4c5; color: #ea2b2b;}
    
    .bottom-msg { font-size: 24px; font-weight: 800; display: flex; align-items: center; gap: 10px; margin-left: 20px;}
    .bottom-btn { max-width: 200px; width: 100%; }

    .end-screen { text-align: center; display: none; padding: 40px 0;}
    .end-screen h2 { font-size: 36px; color: var(--primary); }
    
    #quiz-area { display: block; }
</style>

<div class="progress-bar-bg" id="progress-container">
    <div class="progress-bar-fill" id="progress-fill"></div>
</div>

<div id="quiz-area">
    <div class="question-box">
        <div class="question-title" id="q-title">Translate this</div>
        <div class="question-word" id="q-word">Word</div>
    </div>
    <div class="options-grid" id="options-grid">
        <!-- Buttons injected by JS -->
    </div>
</div>

<div id="end-screen" class="end-screen">
    <h2>Lesson Complete! 🎉</h2>
    <p>Great job! You have completed this practice session.</p>
    <br>
    <a href="/" class="btn">Continue</a>
</div>

<div class="bottom-bar" id="bottom-bar">
    <div class="bottom-msg" id="bottom-msg"></div>
    <button class="btn bottom-btn" id="next-btn" onclick="nextQuestion()">Continue</button>
</div>

<!-- JS Data Injection -->
<script>
    const sessionData = {{ practice_data | tojson | safe }};
    const allDict = {{ all_dict | tojson | safe }};
    
    let currentIndex = 0;
    let currentOptions = [];
    let correctAnswer = "";
    
    // Shuffle helper
    function shuffle(array) {
        let currentIndex = array.length, randomIndex;
        while (currentIndex !== 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
        }
        return array;
    }

    // Initialize Quiz
    sessionData.words = shuffle(sessionData.words);

    function loadQuestion() {
        if (currentIndex >= sessionData.words.length) {
            showEndScreen();
            return;
        }

        let wordObj = sessionData.words[currentIndex];
        
        let direction = Math.random() > 0.5 ? 'es-cz' : 'cz-es';
        
        let questionWord = direction === 'es-cz' ? wordObj.spanish : wordObj.czech;
        correctAnswer = direction === 'es-cz' ? wordObj.czech : wordObj.spanish;
        
        document.getElementById('q-title').innerText = direction === 'es-cz' ? 'Translate to Czech' : 'Translate to Spanish';
        document.getElementById('q-word').innerText = questionWord;
        
        let distractorPool = direction === 'es-cz' ? allDict.czech : allDict.spanish;
        let filteredPool = distractorPool.filter(w => w !== correctAnswer);
        
        let options = [correctAnswer];
        shuffle(filteredPool);
        
        for (let i = 0; i < 3; i++) {
            if (filteredPool[i]) options.push(filteredPool[i]);
        }
        
        currentOptions = shuffle(options);
        
        renderOptions();
        updateProgress();
        hideBottomBar();
    }

    function renderOptions() {
        const grid = document.getElementById('options-grid');
        grid.innerHTML = '';
        currentOptions.forEach((opt, index) => {
            let btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.innerText = opt;
            btn.onclick = () => checkAnswer(opt, btn);
            grid.appendChild(btn);
        });
    }

    function checkAnswer(selected, btnElement) {
        const btns = document.querySelectorAll('.option-btn');
        btns.forEach(b => b.disabled = true);
        
        const isCorrect = (selected === correctAnswer);
        
        if (isCorrect) {
            btnElement.classList.add('correct');
            showBottomBar(true);
        } else {
            btnElement.classList.add('wrong');
            btns.forEach(b => {
                if (b.innerText === correctAnswer) b.classList.add('correct');
            });
            showBottomBar(false);
            sessionData.words.push(sessionData.words[currentIndex]); 
        }
    }

    function showBottomBar(isCorrect) {
        const bar = document.getElementById('bottom-bar');
        const msg = document.getElementById('bottom-msg');
        
        bar.className = 'bottom-bar active';
        if (isCorrect) {
            bar.classList.add('correct-bar');
            msg.innerHTML = '✔ Excellent!';
        } else {
            bar.classList.add('wrong-bar');
            msg.innerHTML = '✘ Correct answer: ' + correctAnswer;
        }
    }

    function hideBottomBar() {
        document.getElementById('bottom-bar').className = 'bottom-bar';
    }

    function nextQuestion() {
        currentIndex++;
        loadQuestion();
    }

    function updateProgress() {
        const fill = document.getElementById('progress-fill');
        const percentage = (currentIndex / sessionData.words.length) * 100;
        fill.style.width = percentage + '%';
    }

    function showEndScreen() {
        document.getElementById('quiz-area').style.display = 'none';
        document.getElementById('progress-container').style.display = 'none';
        document.getElementById('end-screen').style.display = 'block';
        hideBottomBar();
        
        if (sessionData.is_single_lesson) {
            fetch('/mark_complete/' + sessionData.lesson_id, { method: 'POST' });
        }
    }

    loadQuestion();
</script>
{% endblock %}
"""

# Register all templates cleanly inside Jinja2's DictLoader
app.jinja_loader = DictLoader({
    "base.html": BASE_TEMPLATE,
    "index.html": INDEX_TEMPLATE,
    "dictionary.html": DICTIONARY_TEMPLATE,
    "custom.html": CUSTOM_TRAINING_TEMPLATE,
    "practice.html": PRACTICE_TEMPLATE
})

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route('/')
def index():
    data = load_vocabs()
    if 'completed' not in session:
        session['completed'] = []
    
    lessons_enum = list(enumerate(data))
    return render_template('index.html', lessons=lessons_enum, completed=session['completed'], str=str)

@app.route('/skip/<int:lesson_id>', methods=['POST'])
def skip_lesson(lesson_id):
    if 'completed' not in session:
        session['completed'] = []
    
    comp = session['completed']
    if str(lesson_id) not in comp:
        comp.append(str(lesson_id))
        session['completed'] = comp
    return redirect(url_for('index'))

@app.route('/unskip/<int:lesson_id>', methods=['POST'])
def unskip_lesson(lesson_id):
    if 'completed' in session:
        comp = session['completed']
        if str(lesson_id) in comp:
            comp.remove(str(lesson_id))
            session['completed'] = comp
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_progress():
    session['completed'] = []
    return redirect(url_for('index'))

@app.route('/mark_complete/<int:lesson_id>', methods=['POST'])
def mark_complete(lesson_id):
    if 'completed' not in session:
        session['completed'] = []
    comp = session['completed']
    if str(lesson_id) not in comp:
        comp.append(str(lesson_id))
        session['completed'] = comp
    return jsonify({"status": "success"})

@app.route('/dictionary')
def dictionary():
    data = load_vocabs()
    all_words = []
    stats = {}
    
    for lesson in data:
        for w in lesson.get('words', []):
            all_words.append(w)
            wt = w.get('type', 'Other')
            stats[wt] = stats.get(wt, 0) + 1

    return render_template('dictionary.html', all_words=all_words, total_words=len(all_words), stats=stats)

@app.route('/custom')
def custom_training():
    data = load_vocabs()
    lessons_enum = list(enumerate(data))
    return render_template('custom.html', lessons=lessons_enum)

@app.route('/practice')
def practice():
    data = load_vocabs()
    lesson_id = request.args.get('lesson_id')
    custom_lessons = request.args.getlist('custom_lessons')
    
    practice_words = []
    is_single = False
    l_id = -1
    
    if lesson_id is not None:
        idx = int(lesson_id)
        if 0 <= idx < len(data):
            practice_words = data[idx]['words']
            is_single = True
            l_id = idx
    elif custom_lessons:
        for cl in custom_lessons:
            idx = int(cl)
            if 0 <= idx < len(data):
                practice_words.extend(data[idx]['words'])
                
    if not practice_words:
        return redirect(url_for('index'))
        
    # Build dictionaries for random distractors
    all_spanish = []
    all_czech = []
    for lesson in data:
        for w in lesson.get('words', []):
            if w['spanish'] not in all_spanish: all_spanish.append(w['spanish'])
            if w['czech'] not in all_czech: all_czech.append(w['czech'])
            
    practice_data = {
        "words": practice_words,
        "is_single_lesson": is_single,
        "lesson_id": l_id
    }
    
    all_dict = {
        "spanish": all_spanish,
        "czech": all_czech
    }
    
    return render_template('practice.html', practice_data=practice_data, all_dict=all_dict)


if __name__ == '__main__':
    print("==================================================")
    print("🟩 DuoVocab Replica is starting!")
    print("🟩 Make sure 'vocabs.txt' is in:", os.path.dirname(os.path.abspath(__file__)))
    print("🟩 Open http://127.0.0.1:5000/ in your browser")
    print("==================================================")
    
    app.run(debug=True, port=5000)