from flask import Flask, render_template, request, jsonify, session
import openai
from datetime import datetime
  
  
app = Flask(__name__, template_folder='template', static_folder='static') 
  
# OpenAI API Key 
openai.api_key = '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'
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

def intro(data):
    messages = session.get('messages', [])
    messages.append(
        {"role": "user", "content": data})     
    return messages[1]['content']


def summarize():
    messages = session.get('messages', [])
    messages.append({"role": "user", "content": "Rangkum semua percakapan diatas tentang user, tidak perlu menjawab tentu, hanya rangkum saja seperti biasa"})
    query = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    print(messages)
    session['summary'] = query.choices[0].message.content
    return session['summary']

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
        introduction = "Halo, saya adalah sebuah AI yang memiliki pengetahuan umum tentang berbagai topik, termasuk komputer hardware. siap membantu Anda dengan pertanyaan atau informasi terkait komputer hardware dan berbagai topik lainnya. Silakan beri tahu saya apa yang dapat saya bantu!"
        time = datetime.now().strftime("%I:%M:%S %p")
        session['messages'] = [
            {"role": "system", "content": "kamu adalah kecerdasan buatan yang memiliki pengetahuan luas dalam bidang komputer hardware dan bernama Toshka, jika ada yang ingin membuat atau meracik PC buatkan rincian harganya berdasarkan marketplace."}
        ]

        return render_template('index2.html', introduction=introduction, time=time)

    return render_template('index2.html')



@app.route("/summarize", methods=['POST'])
def summarize_route():
    summarize()
    return jsonify({'summary': session.get('summary', '')})

@app.route("/intro", methods=['POST'])
def intro_route():
    data = request.form['data']
    user_intro = intro(data)
    return jsonify({'data': user_intro})
    

if __name__ == "__main__":
    app.run(debug=True)