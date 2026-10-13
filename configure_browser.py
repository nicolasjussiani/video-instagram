from obs_control import request, ws
import json

scene = 'Reels - Rosto e jogo'
items = request('GetInputPropertiesListPropertyItems', {'inputName':'Jogo no navegador','propertyName':'window'})['propertyItems']
edge = next(x for x in items if x['itemEnabled'] and x['itemValue'].endswith(':msedge.exe'))
request('SetInputSettings', {'inputName':'Jogo no navegador','inputSettings':{'window':edge['itemValue'],'priority':2,'method':2,'client_area':True,'cursor':True}})
request('SetSceneItemEnabled',{'sceneName':scene,'sceneItemId':1,'sceneItemEnabled':False})
request('SetSceneItemIndex',{'sceneName':scene,'sceneItemId':5,'sceneItemIndex':0})
request('SetSceneItemTransform',{'sceneName':scene,'sceneItemId':5,'sceneItemTransform':{'positionX':0,'positionY':0,'boundsType':'OBS_BOUNDS_SCALE_OUTER','boundsWidth':1080,'boundsHeight':1920,'boundsAlignment':0,'cropToBounds':True}})
request('SetSceneItemTransform',{'sceneName':scene,'sceneItemId':2,'sceneItemTransform':{'positionX':100,'positionY':1160,'boundsType':'OBS_BOUNDS_SCALE_INNER','boundsWidth':620,'boundsHeight':500,'boundsAlignment':0}})
for i in (1,2,5):
    request('SetSceneItemLocked',{'sceneName':scene,'sceneItemId':i,'sceneItemLocked':True})
print(json.dumps({'browser':edge['itemName'],'layout':'1080x1920'},ensure_ascii=False))
ws.close(timeout=1)
