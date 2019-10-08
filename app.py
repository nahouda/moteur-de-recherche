from flask import Flask, render_template
from elasticsearch import Elasticsearch
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    search = SubmitField('Search')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
es = Elasticsearch([{u'host': u'127.0.0.1', u'port': b'9200'}])


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    form = SearchForm()
    keyword = form.keyword.data
    if keyword == 'None':
        return render_template('index.html', title='elasticsearch', form=form)
    res = es.search(index='flickrphotos', body={'query': {'fuzzy': {'tags': str(keyword)}}})
    photoNumber = len(res['hits']['hits'])
    urls=[]
    for i in res['hits']['hits']:
        sourceDict = i['_source']
        urls.append("http://farm"+sourceDict['flickr_farm']+".staticflickr.com/"
            +sourceDict['flickr_server']+"/"+sourceDict['id']+"_"+sourceDict['flickr_secret']+".jpg")
    return render_template('index.html', title='elasticsearch', form=form,
                           keyword=keyword, photoNumber=photoNumber, urls=urls)


@app.route('/search', methods=['POST'])
def search():
    res = es.search(index='flk23', body={'query': {'match': {'tags': 'moon'}}})
    return res['hits']['hits']


if __name__ == '__main__':
    app.run()
