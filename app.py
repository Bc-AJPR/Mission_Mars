from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#make an app instance
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

'''Define the Routes'''

#index
@app.route('/')
def index():
    info_mars = mongo.db.info_mars.find_one()
    return render_template('index.html', info_mars=info_mars)

@app.route('/scrape')
def scraper():
    info_mars = mongo.db.info_mars
    info_mars_data = scrape_mars.scrape()
    info_mars.update_one({}, {'$set': info_mars_data}, upsert=True)
    return redirect("/", code=302)

#run the app
if __name__ == '__main__':
    app.run(debug=True)