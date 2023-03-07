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

class ForceView(View):

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get(self, request, id=0):
    if id>0:
      forces = list(Forces.objects.filter(id=id).values())
      
      if len(forces) >0:
        force = forces[0]
        datos={'message': 'Success', 'forces': force}
      else:
        datos={'message': 'Force not found...'}
    else:
      forces = list(Forces.objects.values())
      if len(forces) >0:
        datos={'message': 'Success', 'forces': forces}
      else:
        datos={'message': 'Forces not found...'}
    return JsonResponse(datos)
  
  def delete(self, request, id):
    forces = list(Spring.objects.filter(id=id).values())
    if len(forces)>0:
      Forces.objects.filter(id=id).delete()
      datos={'message': 'Success'}  
    else:
      datos={'message': 'Force not found...'}
    return JsonResponse(datos)

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
        forces = list(Forces.objects.filter(spring=spring["id"]).values())
        datos={'message': 'Success', 'spring': spring, 'points': points, 'forces': forces}
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
                    luz2=jd['luz2'],
                    diam_int1=jd['diam_int1'],
                    diam_int2=jd['diam_int2'],
                    extremo1=jd['extremo1'],
                    extremo2=jd['extremo2'],
                    vuelta_red1=jd['vuelta_red1'],
                    vuelta_red2=jd['vuelta_red2'],
                    grado=jd['grado']
                    )
    spring.save()

    start_time = time.time()
    NodeX, NodeY,NodeZ, storeForceSum, storeDispl, storeStress, deform, simulations = Spring.fem(spring)

    force = Forces(
              forces= storeForceSum,
              displacements = [(deform + deform*j) for j in range(simulations)],
              spring = spring
    )
    force.save()
    for i in range(len(NodeX)):
      posX, posY, posZ, stress = ([] for k in range(4))
      for j in range(len(storeDispl)):
        posX.append(NodeX[i] + storeDispl[j][i][0])
        posY.append(NodeY[i] + storeDispl[j][i][1])
        posZ.append(NodeZ[i] + storeDispl[j][i][2])
        if i == len(NodeX) - 1:
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
