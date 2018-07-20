import googlemaps
import math
from googlemaps.places import places
import requests

start_point_jp = '東京駅'
input_distance_km = 40

gmaps = googlemaps.Client(key="AIzaSyB-o7p9uyxwxAcSUYtpBzhHS3jaM2JuaBw")
geocode_result = gmaps.geocode(start_point_jp)
print(geocode_result)



print(geocode_result[0]['geometry']['location']['lat'])
print(geocode_result[0]['geometry']['location']['lng'])

start_point_ll = [ geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'] ]
print(start_point_ll)
#start_point_ll[0,1][緯度、経度][lat,lng]

input_place_lat= math.cos(start_point_ll[0]*0.017)*111
#入力された場所の緯度1度が何ｋｍか算出
print(input_place_lat)

input_distance_ll = [input_distance_km / input_place_lat , input_distance_km / 111]

# input_distance_ll[0] = input_distance_km / input_place_lat
# #入力された距離が緯度何度分か算出
# print('移動する緯度',input_distance_ll_lat)
#
# input_distance_ll[1] = input_distance_km / 111
# #入力された距離が経度何度分か算出
# print('移動する経度',input_distance_ll_lng)

print('移動する緯度',input_distance_ll[0])
print('移動する経度',input_distance_ll[1])

# mid_point_1 = [start_point_ll[0] , start_point_ll[1]+input_distance_ll[1]]
# mid_point_2 = [start_point_ll[0] + input_distance_ll[0] , start_point_ll[1]]
# mid_point_3 = [start_point_ll[0] , start_point_ll[1] - input_distance_ll[1]]
# mid_point_4 = [start_point_ll[0] - input_distance_ll[0] , start_point_ll[1]]
#
# print('point1','point2','point3','point4')
# print(mid_point_1,mid_point_2,mid_point_3,mid_point_4)

#移動した4地点
mid_point = [(start_point_ll[0] , start_point_ll[1]+input_distance_ll[1]),
              [start_point_ll[0] + input_distance_ll[0] , start_point_ll[1]],
              [start_point_ll[0] , start_point_ll[1] - input_distance_ll[1]],
              [start_point_ll[0] - input_distance_ll[0] , start_point_ll[1]]]

print(mid_point)

#移動した4地点から周囲を検索したゴール候補を入力
goal_point_name = []
goal_point_ll = []

#要訂正
for i in range(0,4,1):
    place = gmaps.places(query="空港",location=mid_point[i],radius=1,language='ja')
    for j in place['results']:

        goal_point_name.append(j['name'])        
        goal_point_ll.append([j['geometry']['location']['lat'],j['geometry']['location']['lng']])

        
print(goal_point_name)
print(goal_point_ll)
print(start_point_ll)

distance_diff = []

route = gmaps.distance_matrix(origins=start_point_jp,destinations=goal_point_name,mode='driving',language='ja')
count = 0
for j in route['rows'][0]['elements']:
    print(j['distance']['value'],goal_point_name[count])
    distance_diff.append([abs(input_distance_km*1000 - j['distance']['value']),goal_point_name[count]])
    count += 1

print( distance_diff[0])
# distance_diff_sort = sorted(distance_diff[1][0])
# print( distance_diff_sort)


