from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

data=list()
data.append({'id':0, 'name':'Entry one', 'secret':'secret'})
data.append({'id':1, 'name':'Entry two', 'secret':'password'})
data.append({'id':2, 'name':'Entry three', 'secret':'yay'})

@app.route('/')
def index():
    return render_template('index.html',data=data)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/test',methods=('GET',))
def test():
    if request.method=='GET' and 'id' in request.args:
        id=int(request.args['id'])
        return render_template('test.html',id=id,data=data[id])
    else:
        return redirect(error)



if __name__=='__main__':
    app.debug = True
    app.run(port=8080, host='0.0.0.0')
