import googlemaps
import math
from googlemaps.places import places
import requests

#htmlからのinput
start_point_jp = '東京駅'
input_distance_km = 50

#ここからコピペ
#ここからコピペ

error_pm = input_distance_km * 0.2 * 1000
input_distance_km_def = input_distance_km
input_distance_km = input_distance_km * 0.90
keyword = ["駅"]

#キーの入力（gmapsに保存）
gmaps = googlemaps.Client(key="AIzaSyB-o7p9uyxwxAcSUYtpBzhHS3jaM2JuaBw")

#geocode_resultにstart_point_jp（スタート地点名）を入れることで地点の情報が返ってくる
geocode_result = gmaps.geocode(start_point_jp)
#print(geocode_result)

#周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
#0724編集、htmlに影響あり
if not geocode_result:
    print('スタート地点が見つかりません')
    #return render(request, 'c_error.html')
    exit()


'''
#geocode_resultに入ってる座標データだけ表示
#print(geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'])
'''

#start_point_llに座標データのみ入れる
#start_point_ll[0,1][緯度、経度][lat,lng]
start_point_ll = [ geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'] ]

#0.017453293=2×π÷360（角度からラジアンを求める係数),angle_from_radian
#111.3194908=6378.1366×2×π÷360（地球を半径6378.137kmの球として断面の円周を求める係数）factor_ask_section_circumference
afr = 2 * math.pi / 360
sc = 6378.1366 * 2 * math.pi / 360

#経度1度の距離(km) = cos(緯度×0.017453293) × 111.3194908
#入力された場所の経度1度が何ｋｍか算出
input_place_lng= math.cos(start_point_ll[0]*afr)*sc

#入力された場所の緯度1度が何ｋｍか算出
#円周の長さは2πrで求めらる、Earth_circumference
#2∗π∗6378136.6=40,054,782(m)
#1度は,40054782/360=111,263.283(m)

input_place_lat= 2 * math.pi * 6378136.6 /360 / 1000
print(input_place_lat)

#input_distance_llに入力された距離が緯度経度何度分か計算し入力
input_dis_ll = [input_distance_km / input_place_lat , input_distance_km / input_place_lng]

input_dis_sla = [input_dis_ll[0] / math.sqrt(2),input_dis_ll[1] / math.sqrt(2)]

print('移動する緯度',input_dis_ll[0])
print('移動する経度',input_dis_ll[1])

#移動した8地点
mid_point = [[start_point_ll[0] , start_point_ll[1]+input_dis_ll[1]],
             [start_point_ll[0] + input_dis_ll[0] , start_point_ll[1]],
             [start_point_ll[0] , start_point_ll[1] - input_dis_ll[1]],
             [start_point_ll[0] - input_dis_ll[0] , start_point_ll[1]],
             [start_point_ll[0] + input_dis_sla[0],start_point_ll[1] + input_dis_sla[1]],
             [start_point_ll[0] + input_dis_sla[0],start_point_ll[1] - input_dis_sla[1]],
             [start_point_ll[0] - input_dis_sla[0],start_point_ll[1] - input_dis_sla[1]],
             [start_point_ll[0] - input_dis_sla[0],start_point_ll[1] + input_dis_sla[1]]]

print(mid_point)

mis_point = []

for i in range(0,8,1):
    if (mid_point[i][0]  >= -90 and mid_point[i][0] <= 90):
        pass
    else:
        mid_point[i][0] = (mid_point[i][0]-90) - 90


    if(mid_point[i][1] >= -180 and mid_point[i][1] <= 180):
        pass
    else:
        mid_point[i][1] = (mid_point[i][1]-180) - 180

print(mid_point)

#ゴール候補を入れるリスト
gpn = []
gpll = []
goal_point_name = []
goal_point_ll = []
dis_diff_1 = []
#入力距離との差を入れるリスト
dis_diff = []

#色のリスト
colorlist = ['#FF0000','#FF8000','#40FF00','#00BFFF','#0000FF']

#移動した8地点から周辺を検索
for i in range(0,8,1):

    for k in range(0,len(keyword),1):
        print(i,keyword[k])
        place1 = gmaps.places_nearby(keyword="".join(keyword[k]),location=mid_point[i],radius=5000,language='ja')


#1地点ごとの周辺検索結果を保存
        for j in place1['results']:
            gpn.append(j['name'])
            goal_point_name.append(j['name'])
            gpll.append([j['geometry']['location']['lat'],j['geometry']['location']['lng']])

        place1.clear()

#gpnが空だった場合はループを続ける
    if not gpn:
        continue

#gpnが存在していたらルートを検索する
    else:
    #スタート地点からゴール候補のルート（距離）を検索
        route = gmaps.distance_matrix(origins=start_point_jp,destinations=gpn,mode='driving',language='ja',avoid='highways')

        print(i,route)
        #全ルートの距離と入力距離の差を出す
        count = 0
        for j in route['rows'][0]['elements']:
            if 'distance' not in j:
                continue
            dis_diff.append([abs(input_distance_km_def*1000 - j['distance']['value']),gpn[count],gpll[count],j['distance']['text']])
            count += 1

#ゴール候補地が無い場合は処理をしない
        if not dis_diff:
            continue
        else:
            #差をソートする
            dis_diff_sort = sorted(dis_diff)
            print( i,dis_diff_sort)

            #差が一番小さいものだけ保存
            #差が入力距離の20%を超えるものは保存しない
            if dis_diff_sort[0][0] <= error_pm:
                dis_diff_1.append(dis_diff_sort[0])

#次の地点を検索するので、配列をクリアする
        gpn.clear()
        gpll.clear()
        dis_diff.clear()
        route.clear()


#周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
#0724編集、htmlに影響あり
if not dis_diff_1:
    print('候補地点無し')
    #return render(request, 'c_error.html')
    exit()

print('スタート地点',start_point_ll)

#ソートする
dis_diff_1_sort = sorted(dis_diff_1)

#差の上位5つを抽出
distance_diff_5 = []
route = []
route_altitude_m = []

#候補地点が5ヶ所以上の場合と以下の場合で分岐
if len(dis_diff_1_sort) < 5:
    print(dis_diff_1_sort[0][2])
    for i in range(0,len(dis_diff_1_sort),1):
        distance_diff_5.append(dis_diff_1_sort[i])
        route.append(dis_diff_1_sort[i][2])
        distance_diff_5[i].append(colorlist[i])
        
        route = [start_point_ll,dis_diff_1_sort[i][2]]
        route_altitude = gmaps.elevation_along_path(path = route,samples=512)
        
        for k in range(0,len(route_altitude),1):
            route_altitude_m.append(route_altitude[k]['elevation'])
        max_altitude = int(max(route_altitude_m))
        min_altitude = int(min(route_altitude_m))
        
        distance_diff_5[i].append(max_altitude)
        distance_diff_5[i].append(min_altitude)
        
        route_altitude_m.clear()
        
else:
    for i in range(0,5,1):
        distance_diff_5.append(dis_diff_1_sort[i])
        route.append(dis_diff_1_sort[i][2])
        distance_diff_5[i].append(colorlist[i])
        
        route = [start_point_ll,dis_diff_1_sort[i][2]]
        route_altitude = gmaps.elevation_along_path(path = route,samples=512)
        for k in range(0,len(route_altitude),1):
            route_altitude_m.append(route_altitude[k]['elevation'])
        max_altitude = int(max(route_altitude_m))
        min_altitude = int(min(route_altitude_m))
        
        distance_diff_5[i].append(max_altitude)
        distance_diff_5[i].append(min_altitude)
        
        route_altitude_m.clear()
        
print(distance_diff_5)

#標高関連

   
   
# interval = input_distance_km * 1000 / 512
# 
# gradient = []
# 
# for i in range(0,len(route_altitude)-1,1):
#     gradient.append((route_altitude[i+1]['elevation'] - route_altitude[i]['elevation']) * 100 / interval)
# 
# print(gradient)