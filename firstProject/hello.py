from flask import Flask
app=Flask(__name__)

@app.route('/groundAnalysisData')
def hello_world():
    return 'helloWorld'

if __name__ == '__main__':
    app.run()
