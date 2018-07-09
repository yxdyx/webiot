# 当传参格式要求为json串时
import requests

url = 'http://127.0.0.1:8000/1'
data = {"username": "admin", "password": 123456}
res = requests.get(url)
# res = requests.post(url, json=data)  # 只需要在这里指定data为json即可
# res = requests.post(url, data)
# res = res.text# text方法是获取到响应为一个str，也不需要对res进行转换等处理
# res = res.json()  # 当返回的数据是json串的时候直接用.json即可将res转换成字典
print(res.text)
