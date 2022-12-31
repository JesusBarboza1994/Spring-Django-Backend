from django.http import JsonResponse

from django.forms.models import model_to_dict

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from spring.models import Spring
from points.models import Points
from forces.models import Forces

import time
import json

# def api_home(request, *args, **kwargs):
#   return JsonResponse({"messagge": "Aqui estaraán los datos"})

class PointView(View):
  def get(self, request, id=0):
    if id>0:
      points = list(Points.objects.filter(id=id).values())
      
      if len(points) >0:
        point = points[0]
        
        datos={'message': 'Success', 'points': points}
      else:
        datos={'message': 'Point not found...'}
    else:
      points = list(Points.objects.values())
      if len(points) >0:
        datos={'message': 'Success', 'points': points}
      else:
        datos={'message': 'Points not found...'}
    return JsonResponse(datos)

class SpringView(View):
  
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get(self, request, id=0):
    if id>0:
      springs = list(Spring.objects.filter(id=id).values())
      
      if len(springs) >0:
        spring = springs[0]
        points = list(Points.objects.filter(spring=spring["id"]).values())
        datos={'message': 'Success', 'springs': spring, 'points': points}
      else:
        datos={'message': 'Spring not found...'}
    else:
      springs = list(Spring.objects.values())
      if len(springs) >0:
        datos={'message': 'Success', 'springs': springs}
      else:
        datos={'message': 'Springs not found...'}
    return JsonResponse(datos)


  def post(self, request):
    jd = json.loads(request.body)
    print(jd)
    spring = Spring(alambre=jd['alambre'], 
                    diam=jd['diam'], 
                    vueltas=jd['vueltas'], 
                    longitud=jd['longitud'], 
                    luz1=jd['luz1'], 
                    luz2=jd['luz2'])
    spring.save()

    start_time = time.time()
    NodeX, NodeY,NodeZ, storeForceSum, storeDispl, storeStress = Spring.fem(spring)
    for i in range(len(NodeX)):
      posX, posY, posZ, stress = ([] for k in range(4))
      for j in range(len(storeDispl)):
        posX.append(NodeX[i] + storeDispl[j][i][0])
        posY.append(NodeY[i] + storeDispl[j][i][1])
        posZ.append(NodeZ[i] + storeDispl[j][i][2])
        # print(i)
        # print(j)
        # print(storeStress[j][i])
        if i == 800:
          stress.append(storeStress[j][i-1])
        else:  
          stress.append(storeStress[j][i])
      point = Points(posx = posX,
                     posy = posY,
                     posz = posZ,
                     esf = stress,
                     spring = spring)
      point.save()

    print(time.time() - start_time)
    # pointsX, pointsY, pointsZ = Spring.fem(spring)
    # for i in range(len(pointsX)):
    #   point = Points(x=pointsX[i],
    #                  y=pointsY[i],
    #                  z=pointsZ[i], 
    #                  spring=spring)
    #   point.save()
    # Spring.objects.create(alambre=jd['alambre'], diam=jd['diam'], vueltas=jd['vueltas'], 
    # longitud=jd['longitud'], luz1=jd['luz1'], luz2=jd['luz2'])
    datos={'message': 'Success'}
    return JsonResponse(datos)

  def put(self, request, id):
    jd = json.loads(request.body)
    springs = list(Spring.objects.filter(id=id).values())
    if len(springs) >0:
      spring = Spring.objects.get(id=id)
      spring.alambre=jd['alambre']
      spring.diam=jd['diam']
      spring.vueltas=jd['vueltas'] 
      spring.longitud=jd['longitud']
      spring.luz1=jd['luz1']
      spring.luz2=jd['luz2']
      spring.save()
      print(spring)
      datos={'message': 'Success', 'spring': model_to_dict(spring)}  
    else:
      datos={'message': 'Spring not found...'}
    return JsonResponse(datos)


  def delete(self, request, id):
    springs = list(Spring.objects.filter(id=id).values())
    if len(springs)>0:
      Spring.objects.filter(id=id).delete()
      datos={'message': 'Success'}  
    else:
      datos={'message': 'Spring not found...'}
    return JsonResponse(datos)
