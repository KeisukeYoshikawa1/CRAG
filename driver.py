import googlemaps
import math
from googlemaps.places import places
import requests

#htmlからのinput
start_point_jp = '東京駅'
input_distance_km = 60

#キーの入力（gmapsに保存）
gmaps = googlemaps.Client(key="AIzaSyB-o7p9uyxwxAcSUYtpBzhHS3jaM2JuaBw")

#geocode_resultにstart_point_jp（スタート地点名）を入れることで地点の情報が返ってくる
geocode_result = gmaps.geocode(start_point_jp)
#print(geocode_result)

'''
#geocode_resultに入ってる座標データだけ表示
#print(geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'])
'''

#start_point_llに座標データのみ入れる
#start_point_ll[0,1][緯度、経度][lat,lng]
start_point_ll = [ geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'] ]
print(start_point_ll)

#入力された場所の緯度1度が何ｋｍか算出
input_place_lat= math.cos(start_point_ll[0]*0.017)*111
print(input_place_lat)

#input_distance_llに入力された距離が緯度経度何度分か計算し入力
input_distance_ll = [input_distance_km / input_place_lat , input_distance_km / 111]

'''
input_distance_ll[0] = input_distance_km / input_place_lat
#入力された距離が緯度何度分か算出
print('移動する緯度',input_distance_ll_lat)

input_distance_ll[1] = input_distance_km / 111
#入力された距離が経度何度分か算出
print('移動する経度',input_distance_ll_lng)
'''

print('移動する緯度',input_distance_ll[0])
print('移動する経度',input_distance_ll[1])

#移動した4地点
mid_point = [[start_point_ll[0] , start_point_ll[1]+input_distance_ll[1]],
              [start_point_ll[0] + input_distance_ll[0] , start_point_ll[1]],
              [start_point_ll[0] , start_point_ll[1] - input_distance_ll[1]],
              [start_point_ll[0] - input_distance_ll[0] , start_point_ll[1]]]

print(mid_point)

mis_point = []

for i in range(0,4,1):
    print(mid_point[i][0],mid_point[i][1])
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
goal_point_name = []
goal_point_ll = []

#移動した4地点から周辺を検索
for i in range(0,4,1):
        place1 = gmaps.places_nearby(keyword="station",location=mid_point[i],radius=1000,language='ja')
        place2 = gmaps.places_nearby(keyword="museum",location=mid_point[i],radius=10000,language='ja')
        place3 = gmaps.places_nearby(keyword="airport",location=mid_point[i],radius=30000,language='ja')
        place4 = gmaps.places_nearby(keyword="コンビニ",location=mid_point[i],radius=1000,language='ja')
    
        for j in place1['results']:
            goal_point_name.append(j['name'])
            goal_point_ll.append([j['geometry']['location']['lat'],j['geometry']['location']['lng']])

#周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
if not goal_point_name:
    exit()
 
print(goal_point_name)
print(goal_point_ll)
print(start_point_ll)

#スタート地点からゴール候補のルート（距離）を検索
route = gmaps.distance_matrix(origins=start_point_jp,destinations=goal_point_name,mode='driving',language='ja',avoid='highways')
#print(route['rows'][0]['elements'][0]['distance']['value'])

#入力距離との差を入れるリスト
distance_diff = []

#全ルートの距離と入力距離の差を出す
count = 0
for j in route['rows'][0]['elements']:
    if 'distance' not in j:
        continue
    #print(j['distance']['value'],goal_point_name[count])
    distance_diff.append([abs(input_distance_km*1000 - j['distance']['value']),goal_point_name[count],goal_point_ll[count]])
    count += 1

#差をソートする
distance_diff_sort = sorted(distance_diff)
print( distance_diff_sort)

#差の上位5つを抽出
distance_diff_5 = []
print(len(distance_diff_sort))

#候補地点が5ヶ所以上の場合と以下の場合で分岐
if len(distance_diff_sort) < 5:
    for i in range(0,len(distance_diff_sort),1):
        distance_diff_5.append(distance_diff_sort[i])
        
else:
    for i in range(0,5,1):
        distance_diff_5.append(distance_diff_sort[i])
    

print(distance_diff_5)


