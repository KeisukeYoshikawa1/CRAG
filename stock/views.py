from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import InputCrag
#from stock.forms import InputForm
from django.views.generic import FormView
#from stock.forms import ProductForm




def toppage(request):
    return render(request, 'toppage.html')

from stock.forms import InputCrag
def inputpage(request):
    form = InputCrag()
    return render(request, 'inputpage.html',{'form':form})



import googlemaps
import math
from googlemaps.places import places
import requests


def resultpage(request):
    form = InputCrag(request.POST)
    if form.is_valid():
        start_point_jp = form.cleaned_data.get('start_point_jp')
        input_distance_km = float(form.cleaned_data.get('input_distance_km'))

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
        goal_point_name = []
        goal_point_ll = []

        #移動した8地点から周辺を検索
        for i in range(0,8,1):
                place1 = gmaps.places_nearby(keyword="station",location=mid_point[i],radius=1000,language='ja')
                #place2 = gmaps.places_nearby(keyword="museum",location=mid_point[i],radius=10000,language='ja')
                #place3 = gmaps.places_nearby(keyword="airport",location=mid_point[i],radius=30000,language='ja')
                #place4 = gmaps.places_nearby(keyword="コンビニ",location=mid_point[i],radius=1000,language='ja')

                for j in place1['results']:
                    goal_point_name.append(j['name'])
                    goal_point_ll.append([j['geometry']['location']['lat'],j['geometry']['location']['lng']])

        #周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
        if not goal_point_name:
            exit()

        print('スタート地点',start_point_ll)
        print(goal_point_name)
        print(goal_point_ll)


        #スタート地点からゴール候補のルート（距離）を検索
        route = gmaps.distance_matrix(origins=start_point_jp,destinations=goal_point_name,mode='driving',language='ja',avoid='highways')

        #入力距離との差を入れるリスト
        distance_diff = []

        #全ルートの距離と入力距離の差を出す
        count = 0
        for j in route['rows'][0]['elements']:
            if 'distance' not in j:
                continue
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


        d


        c = {
            'distance_diff_5':distance_diff_5,
            'start_point_jp':start_point_jp,
            'start_point_ll': start_point_ll,
            'input_distance_km':input_distance_km,
            }

    return render(request, 'resultpage.html', c)


