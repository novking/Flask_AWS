from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template('user.html', user=user)

@app.route('/awesome/<int:ok>')
def awesome(ok):
    if ok<3:
        return "this is amazing"
    else:
        return "this is awesome"

@app.route('/method', methods=['POST','GET'])
def method():
    if request.method=='POST':
        return "you are posting!"
    else:
        return "you are getting!"

@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html", name=name)

@app.route('/shopping')
def shopping():
    food = ["chesscake", "beef", "indian buffet", "Chinese!"]
    return render_template('shopping.html', food= food)
if __name__ == '__main__':
    app.run(debug=True)
