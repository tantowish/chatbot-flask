from flask import Flask, render_template, request, jsonify, session
import openai
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

  
  
app = Flask(__name__, template_folder='template', static_folder='static') 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chatbot'
db = SQLAlchemy(app)

class chatbot_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    umur = db.Column(db.Integer, nullable=False)
    jenis_kelamin = db.Column(Enum('P', 'L', name='jenis_kelamin_enum'), nullable=False)
    rangkuman = db.Column(db.Text, nullable=True)

# Buat database dan tabel
with app.app_context():
    db.create_all()  
# OpenAI API Key 
openai.api_key = 'sk-API-key'
app.secret_key = '123'

# def introduce():
#     g.messages = [
#         {"role": "system", "content": "kamu adalah kecerdasan buatan yang memiliki pengetahuan luas dalam bidang komputer hardware dan bernama Toshka"},
#         {"role": "user", "content": "Perkenalkan diri anda dengan singkat dan bagaimana cara anda membantu saya"}
#     ]
#     query = openai.chat.completions.create( 
#         model="gpt-3.5-turbo-1106", 
#         messages=g.messages
#     ) 
#     response = query.choices[0].message.content
#     g.messages.append({"role": "assistant", "content":response})
#     return response

# def intro(data):
#     messages = session.get('messages', [])
#     messages.append(
#         {"role": "user", "content": data})     
#     return messages[1]['content']


# def summarize():
#     messages = session.get('messages', [])
#     messages.append({"role": "user", "content": "Rangkum semua percakapan diatas tentang user, tidak perlu menjawab tentu, hanya rangkum saja seperti biasa"})
#     query = openai.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=messages
#     )
#     session['summary'] = query.choices[0].message.content
#     return session['summary']

def get_completion(prompt):
    messages = session.get('messages', [])
    messages.append({"role": "user", "content": prompt})

    query = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )

    response = query.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    session['messages'] = messages

    return response

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = get_completion(prompt)
        print(session['messages'])
        return jsonify({'response': response})

    elif request.method == 'GET':
        introduction = "Halo, saya adalah AI yang memiliki pengetahuan tentang gigi dan mulut, silahkan tanya apapun terkait permasalahan anda"
        session['messages'] = [
            {"role": "system", "content": "Kamu adalah kecerdasan buatan yang berperan dan Memiliki pengetahuan sebagai seorang dokter gigi yang berpengalaman dan berwawasan luas, berbahasa Indonesia namun juga mampu menggunakan bahasa lainnya, baik hati dan ramah, serta memberikan diagnosis sesuai dengan ICD 10 dan memberikan rekomendasi tindakan medis sesuai ICD 9 CM, selalu kaitkan komplikasi dari user ke ICD 10 dan rekomendasikan tindakan medis sesuai ICD 9 CM"}
        ]

        return render_template('index2.html', introduction=introduction)

    return render_template('index2.html')



@app.route("/summarize", methods=['POST'])
def summarize_route():
    messages = session.get('messages', [])
    messages.append({"role": "user", "content": "Rangkum semua percakapan diatas, termasuk ICD 9, dan ICD 10"})
    query = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    session['summary'] = query.choices[0].message.content


    nama = request.form['nama']
    umur = request.form['umur']
    jenis_kelamin = request.form['jenis_kelamin']
    # Menyimpan data ke dalam database
    history = {
        "nama": nama,
        "umur": umur,  
        "jenis_kelamin": jenis_kelamin, 
        "rangkuman": session['summary']
    }

    new_user = chatbot_history(**history)
    db.session.add(new_user)
    db.session.commit()

    # messages.append({"role": "assistant", "content": session['summary']})
    # session['messages'] = messages

    return jsonify({'data': 'data', 'message': 'History Saved!'})
    
@app.route("/intro", methods=['POST'])
def intro_route():
    data = request.form['userInfo']
    messages = session.get('messages', [])
    messages.append({"role": "user", "content": data})
    query = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages = messages
    )
    messages.append({"role": "assistant", "content": query.choices[0].message.content})
    session['messages'] = messages
 
    return jsonify({'data': messages[1]})
    

if __name__ == "__main__":
    app.run(debug=True)