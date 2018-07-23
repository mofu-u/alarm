#coding:utf-8
import RPi.GPIO as GPIO
import time
import datetime
import pygame.mixer
import subprocess
import urllib2,sys
import json

def weather_get():
    citycode = '070030'
    res = urllib2.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()

    # 読み込んだJSONデータをディクショナリ型に変換する
    res = json.loads(res)
    #print '**************************'

    a = 'none'
    b = 'none'
    c = u'最高気温のデータがありません。' #初期状態は'最高気温のデータがありません'
    d = u'最低気温のデータがありません。' #初期状態は'最低気温のデータがありません'

    a =  res["location"]["prefecture"]+','+res["location"]["city"]+u'の今日の天気は'
    for forecast in res["forecasts"]:
        b = forecast["telop"]+u'です。'
        break

    for forcast in res["forecasts"]:
        t_max = forecast["temperature"]["max"]
        t_min = forecast["temperature"]["min"]
  
        if t_max is not None:
            c = u'最高気温は、'+t_max["celsius"]+u'℃です。'
  
        if t_min is not None:
            d = u'最低気温は、'+t_max["celsius"]+u'℃です。'
  
        break

    return a+b+c+d

def speak(sp):
    try:
        subprocess.call(sp.split()) #お天気情報
    except:
        print "Error."
        sys.exit(1)

#macro
button=25

#settings
GPIO.setmode(GPIO.BCM) #button->GPIO25
GPIO.setup(button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
now = datetime.datetime.now()
w_day = ["月","火","水","木","金","土","日"]

#mixerモジュールの初期化をおこなう
pygame.mixer.init()
#音楽ファイルの読み込みをおこなう
pygame.mixer.music.load("Clock-Alarm Dig01-1L.mp3");

cmd = '/root/jsay.sh '
info = cmd + 'スイッチを押すとアラームが止まります'
get_up = cmd + 'おはようございます。良い一日を！'

print('スイッチを押すとアラームが止まります')
speak(info)
    
while True:
    btn=GPIO.input(button) #read the statement of button
    #音楽再生、及び再生回数の設定(-1はループ再生)
    pygame.mixer.music.play(-1)
    if btn == True:
        #アラーム再生終了
        pygame.mixer.music.stop()
        print('おはようございます。良い一日を！')
        speak(get_up)
        break
    time.sleep(1)

data = '現在は、%s月%s日%s曜日の%s時%s分です。そして、今日の天気をお伝えします。' % (str(now.month),str(now.day),w_day[now.weekday()],str(now.hour),str(now.minute))
print(data)
data = cmd + data
speak(data)

print(weather_get())
weather = cmd + weather_get()
speak(weather)

GPIO.cleanup()
