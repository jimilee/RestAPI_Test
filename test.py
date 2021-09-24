import requests
import json
import random

url_s_1_D1 = 'https://grepp-cloudfront.s3.ap-northeast-2.amazonaws.com/programmers_imgs/competition-imgs/2021kakao/problem1_day-1.json'
url_s_1_D2 = 'https://grepp-cloudfront.s3.ap-northeast-2.amazonaws.com/programmers_imgs/competition-imgs/2021kakao/problem1_day-2.json'
url_s_1_D3 = 'https://grepp-cloudfront.s3.ap-northeast-2.amazonaws.com/programmers_imgs/competition-imgs/2021kakao/problem1_day-3.json'

def post_Start(url, token, problem): # POST | Start API 로 key 발급.
    data = {'problem':str(problem)}
    header = {'X-Auth-Token':token}
    res = requests.post(url+'/start', data=data, headers = header)
    return cvt_json_2_dict(res.text)

def get_Locations(url, auth_key): # GET | 서비스 시각에 자전거 대여소가 보유한 자전거 수 반환
    header = {'Authorization':auth_key,'Content-Type':'application/json; chearset=utf-8'}
    res = requests.get(url+'/locations', headers = header)
    return cvt_json_2_dict(res.text)

def get_Trucks(url, auth_key): # GET | 서비스 시각에 자전거 대여소가 보유한 자전거 수 반환
    header = {'Authorization':auth_key,'Content-Type':'application/json; chearset=utf-8'}
    res = requests.get(url + '/trucks', headers= header)
    return cvt_json_2_dict(res.text)

def make_randact():
    list = []
    for i in range(10):
        list.append(random.randint(1,6))
    return list
def put_Simulate(url, auth_key): # PUT | 각 트럭이 행할 명령을 담아 서버에 전달
    header = {'Authorization':auth_key,'Content-Type':'application/json; chearset=utf-8'}
    dict = {'commands':[{"truck_id": 0, "command": make_randact()},
                        {"truck_id": 1, "command": make_randact()},
                        {"truck_id": 2, "command": make_randact()},
                        {"truck_id": 3, "command": make_randact()},
                        {"truck_id": 4, "command": make_randact()}]}
    data = cvt_dict_2_json(dict)
    res = requests.put(url + '/simulate',data=data, headers= header)
    return cvt_json_2_dict(res.text)

def get_Score(url, auth_key): # GET | 해당 Auth key로 획득한 점수를 반환
    header = {'Authorization':auth_key,'Content-Type':'application/json; chearset=utf-8'}
    res = requests.get(url+'/score', headers = header)
    return cvt_json_2_dict(res.text)

def cvt_json_2_dict(jsontxt):
    return json.loads(jsontxt)

def cvt_dict_2_json(dict):
    return json.dumps(dict)

def get_dict(url): #get dict data from url(JSON)
    data = {'key':'value'}
    res = requests.get(url)
    return cvt_json_2_dict(res.text)

def post_json(url, dict, tocken): # tocken = X-Auth-Token : 문제에서 발급되는 응시자 식별 토큰 값
    ## Start API : 문제를 풀기위한 key를 발급.
    # POST /start
    # X-Auth-Token: {X-Auth-Token}
    # Content-Type: application/json
    headers = {tocken : 'application/json; chearset=utf-8'}
    res = requests.post(url, data=json.dumps(dict), headers=headers)
    print(str(res.status_code) + " | " + res.text)



token = 'a61bfb1e9b126bdd61f7b2dd3d1fa989'
baseurl ='https://kox947ka1a.execute-api.ap-northeast-2.amazonaws.com/prod/users'
problems = [1, 2]

for p in problems:
    # Start API
    auth_key, problem, time = post_Start(baseurl, token, p).values()
    print(auth_key, problem, time)

    # Locations API
    data = get_Locations(baseurl, auth_key)
    print(data)

    # Trucks API
    data = get_Trucks(baseurl, auth_key)
    print(data)

    # Simulate API
    while True:
        data = put_Simulate(baseurl, auth_key)
        if data['status'] == 'finished': break # 처리가 완료되면 탈출.

    # Score API
    data = get_Score(baseurl, auth_key)
    print(data)

