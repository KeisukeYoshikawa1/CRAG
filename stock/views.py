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

        #ここからコピペ
        #ここからコピペ

        error_pm = input_distance_km * 0.2 * 1000
        input_distance_km = input_distance_km * 0.90
        keyword = ["station","コンビニ"]

        #キーの入力（gmapsに保存）
        gmaps = googlemaps.Client(key="AIzaSyB-o7p9uyxwxAcSUYtpBzhHS3jaM2JuaBw")

        #geocode_resultにstart_point_jp（スタート地点名）を入れることで地点の情報が返ってくる
        geocode_result = gmaps.geocode(start_point_jp)
        #print(geocode_result)

        #周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
        #0724編集、htmlに影響あり
        if not geocode_result:
            print('スタート地点が見つかりません')
            return render(request, 'c_error.html')
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
                place1 = gmaps.places_nearby(keyword="".join(keyword[k]),location=mid_point[i],radius=1000,language='ja')
                #place2 = gmaps.places_nearby(keyword="museum",location=mid_point[i],radius=10000,language='ja')
                #place3 = gmaps.places_nearby(keyword="airport",location=mid_point[i],radius=30000,language='ja')
                #place4 = gmaps.places_nearby(keyword="コンビニ",location=mid_point[i],radius=1000,language='ja')

        #1地点ごとの周辺検索結果を保存
                for j in place1['results']:
                    gpn.append(j['name'])
                    gpll.append([j['geometry']['location']['lat'],j['geometry']['location']['lng']])

                place1.clear()

        #gpnが空だった場合はループを続ける
            if not gpn:
                continue

        #gpnが存在していたらルートを検索する
<<<<<<< HEAD
            else:
            #スタート地点からゴール候補のルート（距離）を検索
                route = gmaps.distance_matrix(origins=start_point_jp,destinations=gpn,mode='driving',language='ja',avoid='highways')

                print(i,route)
                #全ルートの距離と入力距離の差を出す
                count = 0
                for j in route['rows'][0]['elements']:
                    if 'distance' not in j:
                        continue
                    dis_diff.append([abs(input_distance_km*1000 - j['distance']['value']),gpn[count],gpll[count],j['distance']['text']])
                    count += 1

        #ゴール候補地が無い場合は処理をしない
                if not dis_diff:
                    continue
                else:
=======
                else:
                #スタート地点からゴール候補のルート（距離）を検索
                    route = gmaps.distance_matrix(origins=start_point_jp,destinations=gpn,mode='driving',language='ja',avoid='highways')

                    #全ルートの距離と入力距離の差を出す
                    count = 0
                    for j in route['rows'][0]['elements']:
                        if 'distance' not in j:
                            continue
                        dis_diff.append([abs(input_distance_km*1000 - j['distance']['value']),gpn[count],gpll[count],j['distance']['text']])
                        count += 1

>>>>>>> eaa0f9b9dcc86f3bb470ecff362e906d16d3c7bf
                    #差をソートする
                    dis_diff_sort = sorted(dis_diff)
                    print( i,dis_diff_sort)

                    #差が一番小さいものだけ保存
<<<<<<< HEAD
                    #差が入力距離の20%を超えるものは保存しない
                    if dis_diff_sort[0][0] <= error_pm:
                        dis_diff_1.append(dis_diff_sort[0])
=======
                    dis_diff_1.append(dis_diff_sort[0])
>>>>>>> eaa0f9b9dcc86f3bb470ecff362e906d16d3c7bf

        #次の地点を検索するので、配列をクリアする
                gpn.clear()
                gpll.clear()
                dis_diff.clear()
                route.clear()


<<<<<<< HEAD
        #周辺に施設がなかった場合にはプログラム終了（後日、入力ページに戻るように、エラーメッセが表示されるように）
        #0724編集、htmlに影響あり
        if not dis_diff_1:
            print('候補地点無し')
            return render(request, 'c_error.html')
            exit()

=======
>>>>>>> eaa0f9b9dcc86f3bb470ecff362e906d16d3c7bf
        print('スタート地点',start_point_ll)

        #ソートする
        dis_diff_1_sort = sorted(dis_diff_1)

        #差の上位5つを抽出
        distance_diff_5 = []

        #候補地点が5ヶ所以上の場合と以下の場合で分岐
        if len(dis_diff_1_sort) == 0:
            return render(request, 'c_error.html')

        elif len(dis_diff_1_sort) < 5:
            for i in range(0,len(dis_diff_1_sort),1):
                distance_diff_5.append(dis_diff_1_sort[i])

        else:
            for i in range(0,5,1):
                distance_diff_5.append(dis_diff_1_sort[i])

        #colorコード追加
        for i in range(0,len(distance_diff_5),1):
            distance_diff_5[i].append(colorlist[i])


        print(distance_diff_5)


        c={
            'distance_diff_5':distance_diff_5,
            'start_point_jp':start_point_jp,
            'start_point_ll': start_point_ll,
            'input_distance_km':input_distance_km,
            }


        return render(request, 'resultpage.html', c)


