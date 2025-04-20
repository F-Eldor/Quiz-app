from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'maxfiy_kalit'

def init_db():
    ulanish = sqlite3.connect('english.db')
    kursor = ulanish.cursor()
    
    kursor.execute('''
        CREATE TABLE IF NOT EXISTS foydalanuvchilar (
            foydalanuvchi_id INTEGER PRIMARY KEY AUTOINCREMENT,
            foydalanuvchi_nomi TEXT NOT NULL,
            parol TEXT NOT NULL
        )
    ''')

    kursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            answer_1 TEXT NOT NULL,
            answer_2 TEXT NOT NULL, 
            answer_3 TEXT NOT NULL, 
            answer_4 TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            percent INTEGER NOT NULL    
        )
    ''')

    kursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            foydalanuvchi_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (foydalanuvchi_id) REFERENCES foydalanuvchilar(foydalanuvchi_id)
        )
    ''')

    ulanish.commit()
    ulanish.close()

init_db()

def insert_questions():
    savollar = [
        ("What time ___ the train leave?", "do", "does", "did", "doing", "do", 100),
        ("I ___ to the gym twice a week.", "go", "going", "went", "goes", "go", 100),
        ("She ___ never been to Paris.", "has", "have", "is", "was", "has", 100),
        ("If I ___ rich, I would travel the world.", "am", "was", "were", "will be", "were", 100),
        ("Can you tell me ___ the station is?", "where", "when", "what", "why", "where", 100),
        ("I’ve lived here ___ 2018.", "since", "for", "from", "during", "since", 100),
        ("This is the man ___ car was stolen.", "who's", "which", "whose", "whom", "whose", 100),
        ("She said she ___ busy yesterday.", "is", "was", "has been", "will be", "was", 100),
        ("You ___ smoke in here. It’s forbidden.", "must", "mustn’t", "don’t have to", "should", "mustn’t", 100),
        ("How long ___ you been studying English?", "do", "did", "have", "had", "have", 100),
        ("It was ___ interesting movie.", "an", "a", "the", "some", "an", 100),
        ("I don't have ___ money left.", "many", "a", "much", "several", "much", 100),
        ("My brother is ___ than me.", "tall", "taller", "tallest", "more tall", "taller", 100),
        ("That book is ___ boring.", "such", "so", "too", "very", "so", 100),
        ("Let's go for a walk, ___?", "shall we", "will we", "don’t we", "won’t we", "shall we", 100),
        ("I enjoy ___ to music when I study.", "listen", "listening", "to listen", "listened", "listening", 100),
        ("He works as a teacher, ___ he?", "isn’t", "doesn’t", "wasn’t", "didn’t", "doesn’t", 100),
        ("If I had known, I ___ have told you.", "will", "would", "would have", "had", "would have", 100),
        ("I wish I ___ speak Japanese.", "can", "will", "could", "must", "could", 100),
        ("By the time we arrived, the movie ___.", "started", "had started", "has started", "starts", "had started", 100),
        ("They ___ to the party if they finish their work.", "come", "will come", "came", "would come", "will come", 100),
        ("This is ___ book I’ve ever read.", "best", "the best", "better", "good", "the best", 100),
        ("She asked me ___ I was going.", "where", "when", "why", "what", "where", 100),
        ("I ___ my homework before dinner.", "finished", "finish", "finishing", "have finished", "have finished", 100),
        ("You should ___ earlier to avoid traffic.", "leave", "leaving", "left", "to leave", "leave", 100),
        ("The movie was so ___ that I cried.", "sad", "sadder", "saddest", "sadly", "sad", 100),
        ("He ___ speak English fluently when he was ten.", "can", "could", "will", "would", "could", 100),
        ("I don’t mind ___ late to finish this.", "work", "working", "to work", "worked", "working", 100),
        ("If it ___ tomorrow, we’ll stay home.", "rains", "rain", "rained", "will rain", "rains", 100),
        ("The teacher told us ___ quiet.", "be", "to be", "being", "been", "to be", 100),
    ]

    ulanish = sqlite3.connect('english.db')
    kursor = ulanish.cursor()

    # Clear existing questions to avoid duplicates (remove in production)
    kursor.execute('DELETE FROM questions')
    
    kursor.executemany('''
        INSERT INTO questions (question_text, answer_1, answer_2, answer_3, answer_4, correct_answer, percent)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', savollar)
    
    ulanish.commit()
    ulanish.close()

insert_questions()

@app.route('/')
def bosh_sahifa():
    if 'foydalanuvchi' in session:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        foydalanuvchi_nomi = request.form['foydalanuvchi_nomi']
        parol = request.form['parol']

        ulanish = sqlite3.connect('english.db')
        kursor = ulanish.cursor()
        kursor.execute("SELECT * FROM foydalanuvchilar WHERE foydalanuvchi_nomi = ?", (foydalanuvchi_nomi,))
        mavjud = kursor.fetchone()

        if mavjud:
            ulanish.close()
            return render_template('log.html', xabar="Bu foydalanuvchi nomi allaqachon mavjud", form_type="register")

        kursor.execute('INSERT INTO foydalanuvchilar (foydalanuvchi_nomi, parol) VALUES (?, ?)', 
                       (foydalanuvchi_nomi, parol))
        ulanish.commit()
        ulanish.close()

        session['foydalanuvchi'] = foydalanuvchi_nomi
        return redirect(url_for('bosh_sahifa'))

    return render_template('log.html', form_type="register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        foydalanuvchi_nomi = request.form['foydalanuvchi_nomi']
        parol = request.form['parol']

        ulanish = sqlite3.connect('english.db')
        kursor = ulanish.cursor()
        kursor.execute("SELECT * FROM foydalanuvchilar WHERE foydalanuvchi_nomi = ?", (foydalanuvchi_nomi,))
        foydalanuvchi = kursor.fetchone()
        ulanish.close()

        if foydalanuvchi and foydalanuvchi[2] == parol:
            session['foydalanuvchi'] = foydalanuvchi_nomi
            session['foydalanuvchi_id'] = foydalanuvchi[0]
            return redirect(url_for('bosh_sahifa'))
        else:
            return render_template('log.html', xabar='Foydalanuvchi nomi yoki parol xato', form_type="login")

    return render_template('log.html', form_type="login")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('bosh_sahifa'))

@app.route("/quiz")
def quiz():
    ulanish = sqlite3.connect("english.db")
    cursor = ulanish.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 25")
    all_questions = cursor.fetchall()
    ulanish.close()

    return render_template("quiz.html", savollar=all_questions)

@app.route('/submit', methods=['POST'])
def submit():
    if 'foydalanuvchi_id' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    togrilar = data.get("togrilar", 0)
    umumiy = data.get("umumiy", 1)

    # Validate inputs
    if not isinstance(togrilar, int) or not isinstance(umumiy, int):
        return jsonify({"error": "Invalid input: togrilar and umumiy must be integers"}), 400
    if togrilar < 0 or umumiy <= 0 or togrilar > umumiy:
        return jsonify({"error": "Invalid score data: togrilar must be between 0 and umumiy"}), 400
    if umumiy != 25:
        return jsonify({"error": "Invalid total questions: umumiy must be 25"}), 400

    foiz = (togrilar / umumiy) * 100
    session["foiz"] = round(foiz, 2)

    if foiz < 40:
        daraja = 'A1'
    elif foiz < 60:
        daraja = 'A2'
    elif foiz < 75:
        daraja = 'B1'
    elif foiz < 90:
        daraja = 'B2'
    else:
        daraja = 'C1'

    session["daraja"] = daraja

    # Save result to database
    ulanish = sqlite3.connect('english.db')
    kursor = ulanish.cursor()
    foydalanuvchi_id = session['foydalanuvchi_id']
    kursor.execute('INSERT INTO results (foydalanuvchi_id, score) VALUES (?, ?)', (foydalanuvchi_id, int(foiz)))
    ulanish.commit()
    ulanish.close()

    return jsonify({"foiz": round(foiz, 2), "daraja": daraja})

@app.route('/result')
def result():
    foiz = session.get('foiz')
    daraja = session.get('daraja')

    return render_template('result.html', foiz=foiz, daraja=daraja)

if __name__ == '__main__':
    app.run(debug=True)