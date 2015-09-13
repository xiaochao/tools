# cities
# 国内所有省、市以及对应的id，以及世界上主要的城市

##数据来源
###在此感谢鹅厂，所有的数据都是从鹅厂注册页面获取到的

### [演示地址](http://tools.bugcode.cn)
### ![截图](http://7xlrq6.com1.z0.glb.clouddn.com/tools.png?attname=&e=1442249233&token=ylQC8EgbJjYVLBChocIRmkrAfslPi9tuwDU33kSF:4sBjITG6j1w8Z9jtlRvSdBB1KLg)
### 使用方法：
* 输入国家名称，获取到国家ID
* 输入省，获取到国家和省ID
* 输入城市，获取到国家、省和市ID

### API

url = 'http://tools.bugcode.cn'
#####根据城市名字获取城市ID

	r = requests.post(url+'/cities/search', {'country': '中国', 'language': 'cn', 'province': '江苏', 'city': '淮安'})
	if r.status_code == 200:
    	print r.text
	else:
    	print r.status_code

#####根据城市ID获取城市名字
* 获取所有国家

		r = requests.post(url+'/cities/search', {'action': 'countries', 'language': 'cn'})
		if r.status_code == 200:
    		print r.text
		else:
    		print r.status_code
* 获取一个国家所有省份

		r = requests.post(url+'/cities/search', {'action': 'provinces', 'language': 'cn', 'c_id': 1})
		if r.status_code == 200:
    		print r.text
		else:
    		print r.status_code
    		
* 获取一个国家一个省所有城市

		r = requests.post(url+'/cities/search', {'action': 'cities', 'language': 'cn', 'c_id': 1, 'p_id': 32})
		if r.status_code == 200:
    		print r.text
		else:
    		print r.status_code

* 获取一个国家一个省一个城市

		r = requests.post(url+'/cities/search', {'action': 'city', 'language': 'cn', 'c_id': 1, 'p_id': 32, 'i_id': 8})
		if r.status_code == 200:
    		print r.text
		else:
    		print r.status_code
