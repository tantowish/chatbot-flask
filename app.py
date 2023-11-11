from flask import Flask, render_template, request, jsonify ,g 
import openai
from datetime import datetime
  
  
app = Flask(__name__, template_folder='template', static_folder='static') 
  
# OpenAI API Key 
openai.api_key = 'key'

def introduce():
    g.messages = [
        {"role": "system", "content": "kamu adalah kecerdasan buatan yang memiliki pengetahuan luas dalam bidang komputer hardware dan bernama Toshka"},
        {"role": "user", "content": "Perkenalkan diri anda dengan singkat dan bagaimana cara anda membantu saya"}
    ]
    query = openai.chat.completions.create( 
        model="gpt-3.5-turbo-1106", 
        messages=g.messages
    ) 
    response = query.choices[0].message.content
    g.messages.append({"role": "assistant", "content":response})
    return response

def get_completion(prompt): 
    g.messages.append(
        {"role": "user", "content": prompt}
    )
    
    query = openai.chat.completions.create( 
        model="gpt-3.5-turbo-1106", 
        messages=g.messages
    ) 

    response = query.choices[0].message.content
    g.messages.append({"role": "assistant", "content":response})
    return response 
  
@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
    g.messages =[{"role": "assistant","content":introduce()}]
    if request.method == 'POST': 
        prompt = request.form['prompt'] 
        response = get_completion(prompt) 
        print(g.messages) 
        return jsonify({'response': response})

    elif request.method == 'GET':
        introduction = g.messages[0]['content']
        time = datetime.now().strftime("%I:%M:%S %p")

        return render_template('index.html', introduction=introduction, time=time) 
    return render_template('index.html') 

@app.route("/index", methods=['POST', 'GET'])
def index():
    g.messages =[{"role": "assistant","content":introduce()}]
    if request.method == 'POST': 
        prompt = request.form['prompt'] 
        response = get_completion(prompt) 
        print(g.messages) 
        return jsonify({'response': response})

    elif request.method == 'GET':
        introduction = g.messages[0]['content']
        time = datetime.now().strftime("%I:%M:%S %p")

        return render_template('index2.html', introduction=introduction, time=time) 
    return render_template('index2.html') 
  
if __name__ == "__main__": 
    app.run(debug=True) 