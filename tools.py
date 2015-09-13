#coding=utf-8

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import simplejson as json
import logging
import os

app = Flask(__name__)
app.debug = True

#get cities from file
cities = open(os.path.split(os.path.realpath(__file__))[0]+'/cities.json').read()
cities = json.loads(cities)

#init logger
logger = logging.getLogger("city")
fh = logging.FileHandler('city.run.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

#init mysql connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/tools'
db = SQLAlchemy(app)

#define a table
class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_id = db.Column(db.String(16))
    country = db.Column(db.String(64))
    p_id = db.Column(db.String(16))
    province = db.Column(db.String(64))
    i_id = db.Column(db.String(16))
    city = db.Column(db.String(64))

    def __init__(self, c_id, country, p_id, province, i_id, city):
        self.c_id = c_id
        self.country = country
        self.p_id = p_id
        self.province = province
        self.i_id = i_id
        self.city = city
        pass

    def __repr__(self):
        return '<country %r province %r city %r>' % self.country, self.province, self.city


@app.route('/tools', methods=['GET', 'POST'])
@app.route('/tools/cities', methods=['GET', 'POST'])
def hello_world():
    logger.debug(request.remote_addr)
    if request.method == 'GET':
        return render_template('cities.html')
    province = request.form.get('province', '')
    country = request.form.get('country', '')
    city = request.form.get('city', '')
    print type(country)
    if city:
        #myvar = dict(city=city)
        #result = db.select('cities', myvar, where='city="'+city+'"', what='c_id, p_id, i_id')
        result = Cities.query.filter_by(city=city)
    if province:
        #myvar = dict(province=province)
        #result = db.select('cities', myvar, where='province="'+province+'"', what='c_id, p_id')
        result = Cities.query.filter_by(province=province)
    if country:
        #myvar = dict(country=country)
        #result = db.select('cities', myvar, where='country="'+country+'"', what='c_id')
        result = Cities.query.filter_by(country=country)

    find_or_not = False
    now_list = list()
    if result:
        for i in result:
            return_result = dict()
            if not country or country == i.country:
                if not province and not city:
                    return_result['country'] = i.country
                    return_result['c_id'] = i.c_id
                    return_result['province'] = ''
                    return_result['p_id'] = ''
                    return_result['city'] = ''
                    return_result['i_id'] = ''
                    now_list.append(return_result)
                    find_or_not = True
                    break
                if not province or province == i.province:
                    if not city:
                        return_result['country'] = i.country
                        return_result['c_id'] = i.c_id
                        return_result['province'] = i.province
                        return_result['p_id'] = i.p_id
                        return_result['city'] = ''
                        return_result['i_id'] = ''
                        now_list.append(return_result)
                        find_or_not = True
                        break
                    if not city or city == i.city:
                        return_result['country'] = i.country
                        return_result['c_id'] = i.c_id
                        return_result['province'] = i.province
                        return_result['p_id'] = i.p_id
                        return_result['city'] = i.city
                        return_result['i_id'] = i.i_id
                        find_or_not = True
            now_list.append(return_result)
        now_result = dict(flag=0, result=now_list)
        if not find_or_not:
            logger.warn('miss:'+str(request.form))
        return json.dumps(now_result)
    if not province and not city and not country:
        return json.dumps({'flag': 1, 'message': '请至少输入一个'})
    return json.dumps({'flag': 0, 'message': 'success'})

if __name__ == '__main__':
    app.run()
