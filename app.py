from flask import Flask, render_template, url_for, request
from logger_class import log
from time import time, strftime
from mongoDBOperations import MongoDBManagement
from wikiscrapper import wikiScrapper

# If script failed Log handlers need removing before starting again
try:
    log.close_log()
except:
    pass

log = log("Wikipedia")
log.logger.info(f"Starting Processing at : {strftime('%H:%M:%S').format(time())}")

collection_name = None

free_status = True
db_name = 'Wikipedia-Scrapper'

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home_page():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString = request.form['content'] # obtaining the search string entered in the form
        try:
            scrapper_object = wikiScrapper(searchString=searchString)
            mongoClient = MongoDBManagement(username='mongodb', password='mongodb')
            log.logger.info(f"Data creation begins for {searchString}")
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                summary =[ i for i in response]
                new_summary = {}
                for i in summary:
                    new_summary.update(i)
                #return render_template('summary.html', result= [a_dict['summary'] for a_dict in summary])  # show the results to user
                return render_template('summary.html', result = new_summary, title = 'Details Page')
            else:
                #summary = scrapper_object.WikiSummary()
                summary = scrapper_object.getSummaryToDisplay(username='mongodb', password='mangodb', )
            return render_template('summary.html',result = summary)
        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))
    else:
        return render_template('home.html', title = 'Home Page')

#Work in Progress to show details in different pages

posts = [
    {
        'images' : 'Work In Progress. As of now everything is rendered in home page.',
        'references' : 'Work In Progress. As of now everything is rendered in home page.'

    }
]

@app.route("/summary")
def summary():
     return render_template('references.html', posts = posts, title = 'Wikipedia Summary' )

@app.route("/references")
def references():
    return render_template('references.html', posts = posts, title = 'Wikipedia References')

@app.route("/images")
def images():
    return render_template('images.html', posts = posts, title = 'Wikipedia Images')

if __name__ == '__main__':
    app.run(debug=True)