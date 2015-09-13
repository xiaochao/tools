#coding=utf-8

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
#from flaskext.sqlalchemy import SQLAlchemy 
import simplejson as json
import logging
import os

app = Flask(__name__)
app.debug = False

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

#define a table
class Cities_en(db.Model):
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/cities', methods=['GET', 'POST'])
def cities():
    logger.debug(request.remote_addr)
    if request.method == 'GET':
        return render_template('cities.html')
    language = request.form.get('language', 'cn')
    province = request.form.get('province', '')
    country = request.form.get('country', '')
    city = request.form.get('city', '')
    if city:
        #myvar = dict(city=city)
        #result = db.select('cities', myvar, where='city="'+city+'"', what='c_id, p_id, i_id')
        if language == 'cn':
            result = Cities.query.filter_by(city=city)
        else:
            result = Cities_en.query.filter_by(city=city)
    if province:
        #myvar = dict(province=province)
        #result = db.select('cities', myvar, where='province="'+province+'"', what='c_id, p_id')
        if language == 'cn':
            result = Cities.query.filter_by(province=province)
        else:
            result = Cities_en.query.filter_by(province=province)
    if country:
        #myvar = dict(country=country)
        #result = db.select('cities', myvar, where='country="'+country+'"', what='c_id')
        if language == 'cn':
            result = Cities.query.filter_by(country=country)
        else:
            result = Cities_en.query.filter_by(country=country)

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

@app.route('/cities/search', methods=['POST'])
def cities_api():
    language = request.form.get('language', 'cn')
    action = request.form.get('action', None)
    return_result = list()
    if not action:
        return json.dumps({'flag': 1, 'message': '请选择你要获取的数据'})
    if action == 'countries':
        if language == 'en':
            result = Cities_en.query.group_by('country')
        else:
            result = Cities.query.group_by('country')
        for r in result:
            return_result.append({'c_id': r.c_id, 'country': r.country})
    if action == 'provinces':
        c_id = request.form.get('c_id', None)
        if not c_id:
            return json.dumps({'flag': 1, 'message': '请选择要获取省份所属的国家'})
        if language == 'en':
            result = Cities_en.query.filter_by(c_id=c_id).group_by('province')
        else:
            result = Cities.query.filter_by(c_id=c_id).group_by('province')
        for r in result:
            return_result.append({'p_id': r.p_id, 'province': r.province})
    if action == 'cities':
        p_id = request.form.get('p_id', None)
        c_id = request.form.get('c_id', None)
        if not p_id or not c_id:
            return json.dumps({'flag': 1, 'message': '缺少省id或者国家id'})
        if language == 'en':
            result = Cities_en.query.filter_by(c_id=c_id, p_id=p_id).group_by('city')
        else:
            result = Cities.query.filter_by(c_id=c_id, p_id=p_id).group_by('city')
        for r in result:
            return_result.append({'i_id': r.i_id, 'city': r.city})

    if action == 'city':
        p_id = request.form.get('p_id', None)
        c_id = request.form.get('c_id', None)
        i_id = request.form.get('i_id', None)
        if not p_id or not c_id or not i_id:
            return json.dumps({'flag': 1, 'message': '缺少省id或者国家id'})
        if language == 'en':
            result = Cities_en.query.filter_by(c_id=c_id, p_id=p_id, i_id=i_id).first()
        else:
            result = Cities.query.filter_by(c_id=c_id, p_id=p_id, i_id=i_id).first()
        return_result.append({'c_id': result.c_id, 'country': result.country, 'p_id': result.p_id,
                              'province': result.province, 'i_id': result.i_id, 'city': result.city})
    return json.dumps({'flag': 0, 'result': return_result})

if __name__ == '__main__':
    app.run()
