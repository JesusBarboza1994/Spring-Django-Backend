from django.db import models


# from points.models import Points
import math
import numpy as np

# Create your models here.
class Spring(models.Model):
  alambre = models.DecimalField(max_digits=4, decimal_places=2)
  diam = models.DecimalField(max_digits=5, decimal_places=2)
  vueltas = models.DecimalField(max_digits=6, decimal_places=3)
  longitud = models.DecimalField(max_digits=6, decimal_places=2)
  luz1 = models.IntegerField()
  luz2 = models.IntegerField()
  
  def __str__(self):
    return f'Res. Susp. {self.alambre}x{self.diam}x{self.longitud}x{self.vueltas}'

  def prueba(spring):
    print("hey!!!!!!!!!!!!!!!!!!!!!!!")
    print(spring.alambre*2)

  
  def fem(spring):
    nodos_x_vta = 80
    elementos = int(float(spring.vueltas) * nodos_x_vta)
    nodos = elementos + 1
    radio = (float(spring.diam) - float(spring.alambre)) / 2
    # DIVISIÓN DEL RESORTE EN CUERPO Y EXTREMOS
    h_helice = float(spring.longitud) - float(spring.alambre)
    h_extremo1 = float(spring.alambre) + float(spring.luz1)
    h_extremo2 = float(spring.alambre) + float(spring.luz2)
    h_cuerpo = h_helice - h_extremo1 - h_extremo2
    node_array = []
    node_theta = []
    node_vta = []
    for i in range(nodos):
      node_array.append(i)
      node_theta.append(i * 360 / nodos_x_vta)
      node_vta.append(i / nodos_x_vta)

    ### PROPIEDADES DEL MATERIAL DEL RESORTE 
    youngModulus = 206700 #en MPa
    shearModulus = 79500; #en MPa

    ### CONDICIONES DE CONTORNO 
    lownode1 =  14  #10     #2         #
    lownode2 =  39  #35     #11        #
    lownode3 =  64 #60     #20        #
    upnode1 = 575 #790 #740    #222       #
    upnode2 = 600 #793 #765    #231       #
    upnode3 = 625 #796 #790    #240       #

    area = 0.25*math.pi*float(spring.alambre)**2 #en mm2
    inercia = 0.25*math.pi*(float(spring.alambre)/2)**4 #en mm4
    inerciapolar = inercia*2 
    # for i in range(nodos):
    #   point = Points(x = node_coordX(node_theta[i], radio),
    #                  y = node_coordY(node_vta[i],nodos_x_vta,spring, h_extremo1, h_extremo2, h_helice, h_cuerpo),
    #                  z = node_coordZ(node_theta[i], radio),
    #                  spring = spring)
    #   point.save()

    NodeX = [node_coordX(i, radio) for i in node_theta]
    NodeZ = [node_coordZ(i, radio) for i in node_theta]
    NodeY = [node_coordY(i, nodos_x_vta,spring, h_extremo1, h_extremo2, h_helice, h_cuerpo) for i in node_vta]

    #Declarar las dimensiones XYZ de cada elemento viga
    ElemX=[]
    ElemY=[]
    ElemZ=[]
    Long=[]

    #Declarar vectores unitarios axial(x), transversal(z) y vertical(y) del elemento
    unit_xX = [] 
    unit_zX = []
    unit_yX = []
    unit_xY = [] 
    unit_zY = []
    unit_yY = []
    unit_xZ = [] 
    unit_zZ = []
    unit_yZ = []

    #Declarar angulos entre ejes locales (xyz) y globales(XYZ) del elemento
    ang_xX = []
    ang_zX = [] 
    ang_yX = []
    ang_xY = []
    ang_zY = [] 
    ang_yY = []
    ang_xZ = []
    ang_zZ = [] 
    ang_yZ = []
    
    #Declarar vectores acumuladores de matrices
    vectorKlocal = []
    vectorT = []
    vectorTprime = []
    vectorKGlobal=[]

    #OPERACIONES POR ELEMENTO   

    for ii in range(nodos):
      if ii != nodos_x_vta*float(spring.vueltas):

        #Direccion de los elementos
        ElemX.append(NodeX[ii+1]-NodeX[ii])
        
        ElemY.append(NodeY[ii+1]-NodeY[ii])
        
        ElemZ.append(NodeZ[ii+1]-NodeZ[ii])
        Long.append(math.pow(math.pow(ElemX[ii],2)+math.pow(ElemY[ii],2)+math.pow(ElemZ[ii],2),0.5))

        #Unitario direccion axial (x)
        unit_xX.append(ElemX[ii]/Long[ii])
        unit_xY.append(ElemY[ii]/Long[ii])
        unit_xZ.append(ElemZ[ii]/Long[ii])

        #Unitario direccion transversal (z)
        unit_zX.append(-unit_xZ[ii]/abs(unit_xZ[ii])*math.pow(math.pow(unit_xZ[ii],2)/(math.pow(unit_xZ[ii],2)+math.pow(unit_xX[ii],2)),0.5))
        unit_zY.append(0)
        unit_zZ.append(unit_xX[ii]/abs(unit_xX[ii])*math.pow(math.pow(unit_xX[ii],2)/(math.pow(unit_xZ[ii],2)+math.pow(unit_xX[ii],2)),0.5))
                
        #Unitario direccion vertical (y)
        unit_yX.append(unit_xZ[ii]*unit_zY[ii]-unit_xY[ii]*unit_zZ[ii])
        unit_yY.append(unit_xX[ii]*unit_zZ[ii]-unit_xZ[ii]*unit_zX[ii])
        unit_yZ.append(-(unit_xX[ii]*unit_zY[ii]-unit_xY[ii]*unit_zX[ii]))

        #Angulos ejes locales (xyz) vs ejes globales (XYZ)

        #Angulos del eje local x con los globales XYZ
        ang_xX.append(math.acos(unit_xX[ii])*180/math.pi)
        ang_xY.append(math.acos(unit_xY[ii])*180/math.pi)
        ang_xZ.append(math.acos(unit_xZ[ii])*180/math.pi)

        #Angulos del eje local z con los globales XYZ
        ang_zX.append(math.acos(unit_zX[ii])*180/math.pi)
        ang_zY.append(math.acos(unit_zY[ii])*180/math.pi)
        ang_zZ.append(math.acos(unit_zZ[ii])*180/math.pi)
        
        #Angulos del eje local y con los globales XYZ
        ang_yX.append(math.acos(unit_yX[ii])*180/math.pi)
        ang_yY.append(math.acos(unit_yY[ii])*180/math.pi)
        ang_yZ.append(math.acos(unit_yZ[ii])*180/math.pi)
            
        #Elementos de la matriz de rigidez
        kappa = 0.886
        phi_z = 12*youngModulus*inercia/(kappa*shearModulus*area*math.pow(Long[ii],2))
        phi_y = 12*youngModulus*inercia/(kappa*shearModulus*area*math.pow(Long[ii],2))
        phi_bar_z = 1/(1+phi_z)
        phi_bar_y = 1/(1+phi_y)

        k1 = youngModulus*area/Long[ii]
        k2 = 12*phi_bar_z*youngModulus*inercia/math.pow(Long[ii],3)
        k3 = 6*phi_bar_z*youngModulus*inercia/math.pow(Long[ii],2)
        k4 = 12*phi_bar_y*youngModulus*inercia/math.pow(Long[ii],3)
        k5 = 6*phi_bar_y*youngModulus*inercia/math.pow(Long[ii],2)
        k6 = shearModulus*inerciapolar/Long[ii]
        k7 = (4+phi_y)*phi_bar_y*youngModulus*inercia/Long[ii]
        k8 = (4+phi_z)*phi_bar_z*youngModulus*inercia/Long[ii]
        k9 = (2-phi_y)*phi_bar_y*youngModulus*inercia/Long[ii]
        k10 = (2-phi_z)*phi_bar_z*youngModulus*inercia/Long[ii]

        #Creacion de la matriz vacia de rigidez 12x12
        matrizRigLocal = np.zeros((12,12))
              
        #Asignacion de los elementos a la matriz
        matrizRigLocal[0][0]  = k1
        matrizRigLocal[6][0]  = -k1

        matrizRigLocal[1][1]  = k2
        matrizRigLocal[5][1]  = k3
        matrizRigLocal[7][1]  = -k2
        matrizRigLocal[11][1] = k3

        matrizRigLocal[2][2]  = k4
        matrizRigLocal[4][2]  = -k5
        matrizRigLocal[8][2]  = -k4
        matrizRigLocal[10][2] = -k5

        matrizRigLocal[3][3]  = k6
        matrizRigLocal[9][3]  = -k6

        matrizRigLocal[2][4]  = -k5
        matrizRigLocal[4][4]  = k7
        matrizRigLocal[8][4]  = k5
        matrizRigLocal[10][4] = k9

        matrizRigLocal[1][5]  = k3
        matrizRigLocal[5][5]  = k8
        matrizRigLocal[7][5]  = -k3
        matrizRigLocal[11][5] = k10

        matrizRigLocal[0][6]  = -k1
        matrizRigLocal[6][6]  = k1

        matrizRigLocal[1][7]  = -k2
        matrizRigLocal[5][7]  = -k3
        matrizRigLocal[7][7]  = k2
        matrizRigLocal[11][7] = -k3  

        matrizRigLocal[2][8]  = -k4
        matrizRigLocal[4][8]  = k5
        matrizRigLocal[8][8]  = k4
        matrizRigLocal[10][8] = k5

        matrizRigLocal[3][9]  = -k6
        matrizRigLocal[9][9]  = k6

        matrizRigLocal[2][10] = -k5
        matrizRigLocal[4][10] = k9
        matrizRigLocal[8][10] = k5
        matrizRigLocal[10][10]= k7

        matrizRigLocal[1][11] = k3
        matrizRigLocal[5][11] = k10
        matrizRigLocal[7][11] = -k3
        matrizRigLocal[11][11]= k8
        
        #Matriz Vacia de transformacion de coordenadas local a global
        matrizTransCoord = np.zeros((12,12))

        #Asignacion de los cosenos directores a la matriz de transformacion
        for u in range(4):
          matrizTransCoord[0+3*u][0+3*u] = unit_xX[ii]
          matrizTransCoord[0+3*u][1+3*u] = unit_xY[ii]
          matrizTransCoord[0+3*u][2+3*u] = unit_xZ[ii]
          matrizTransCoord[1+3*u][0+3*u] = unit_yX[ii]
          matrizTransCoord[1+3*u][1+3*u] = unit_yY[ii]
          matrizTransCoord[1+3*u][2+3*u] = unit_yZ[ii]
          matrizTransCoord[2+3*u][0+3*u] = unit_zX[ii]
          matrizTransCoord[2+3*u][1+3*u] = unit_zY[ii]
          matrizTransCoord[2+3*u][2+3*u] = unit_zZ[ii]

        #Almacenar matriz de rigidez del elemento
        vectorKlocal.append(matrizRigLocal)
        #Almacenar Matriz de transformacion del elemento
        vectorT.append(matrizTransCoord)
        vectorTprime.append(np.transpose(matrizTransCoord))
        #Calculo de la matriz de rigidez global
        firstProd = []
        matrizRigGlobal = []
        firstProd.append(np.matmul(np.transpose(matrizTransCoord),matrizRigLocal))
        matrizRigGlobal.append(np.matmul(firstProd,matrizTransCoord))
        #Almacenar matriz de rigidez global del elemento
        vectorKGlobal.append(matrizRigGlobal)

    # FIN FOR DE OPERACIONES POR ELEMENTO    
    # Crear la supermatriz de rigidez del solido
    superMatrix = np.zeros((nodos*6+18,nodos*6+18)) 
    # Numero de filas de la supermatriz de rigidez: #Nodos * Grados de libertad de cada nodo (son 6 en 3D). Se suman 18 filas más para las condic. contorno
    
    # Incorporar las matrices de rigidez global de cada elemento a la matriz.
    for p in range(len(vectorKGlobal)):
      matrix = vectorKGlobal[p][0][0]
      superMatrix = sumMatrix(superMatrix,matrix,(p)*6,(p)*6)
    
    # Utilización de las condiciones de contorno.

    for q in range(3):
    # UX, UY, UZ de los nodos de la base
      superMatrix[nodos*6 + q + 0][(lownode1)*6+q] = 1
      superMatrix[nodos*6 + q + 3][(lownode2)*6+q] = 1
      superMatrix[nodos*6 + q + 6][(lownode3)*6+q] = 1

    # UX, UY, UZ de los nodos del tope
      superMatrix[nodos*6 + q + 9][(upnode1)*6+q] = 1
      superMatrix[nodos*6 + q + 12][(upnode2)*6+q] = 1
      superMatrix[nodos*6 + q + 15][(upnode3)*6+q] = 1

    # FX, FY, FZ de los nodos de la base
      superMatrix[(lownode1)*6+q][nodos*6 + q] = -1
      superMatrix[(lownode2)*6+q][nodos*6 + q + 3] = -1
      superMatrix[(lownode3)*6+q][nodos*6 + q + 6] = -1
        
    # FX, FY, FZ de los nodos del tope
      superMatrix[(upnode1)*6+q][nodos*6 + q + 9] = -1
      superMatrix[(upnode2)*6+q][nodos*6 + q + 12] = -1
      superMatrix[(upnode3)*6+q][nodos*6 + q + 15] = -1 

    # CONFIGURACION DE LA SIMULACION
    # Almacenes de resultados
    storeForces = [] #Almacena matrices de 6 filas (6 nodos BC) x 3 columnas (X,Y,Z)
    storeDispl = [] #Almacena matrices de despl. con filas=Total de nodos y 6 columnas (Despl. Traslacional XYZ y Angular XYZ)
    storeStress= [] #Almacena datos de esfuerzos
    storeSummary = []

    storeForceSum = [] #Vector con la fuerza de reaccion en KG de cada simulacion.
    storevmuy     = []
    storevmdz     = []
    storevmdy     = []
    storevmuz     = []
    storecuy      = []
    storecdz      = []
    storecdy      = []
    storecuz      = []

    deltaY = 0

    #Calculo de la inversa = el vector solucion de desplazamientos y fuerzas "solut"
    inverse = np.linalg.inv(superMatrix)

    ##Iteracion de simulaciones!
    for jj in range(6):
      deltaY = -25-jj*25

      #Vector de coeficientes independientes:
      coef = []
      for pp in range(len(superMatrix)):
        coef.append([0])

      coef[len(coef)-8]=[deltaY]
      coef[len(coef)-5]=[deltaY]
      coef[len(coef)-2]=[deltaY]
        
      # Vector columna tiene los desplazamientas traslacionales y las rotaciones
      # Los datos están agrupados de 6 en 6. Luego de esto vienen 3 datos de fuerza por cada punto de condición de contorno.
      solut = np.dot(inverse, coef) 

      #Matriz de desplazamientos!
      displaceMatrix = []
      w=0
      for v in range(nodos):
        displaceVect=[]
        for uu in range(6):
          displaceVect.append(solut[w][0])
          w=w+1
        displaceMatrix.append(displaceVect)

      #Matriz de fuerzas en los nodos de las condiciones de contorno
      forceMatrix = []
      for vv in range(6): #Son 6 nodos de las condiciones de contorno. Esta matriz tendra 6 filas. 
        forceVect = []
        for uv in range(3): #Cada fila tendra las fuerzas X,Y,Z de los nodos (3 columnas)
          forceVect.append(solut[w][0])
          w = w+1
        forceMatrix.append(forceVect)

      forceSum = (forceMatrix[0][1] + forceMatrix[1][1] + forceMatrix[2][1])/9.81
      storeForceSum.append(forceSum) 

      # Vector de desplazamientos POR ELEMENTO
      dispLoc = []
      dispGlob = []
      for nn in range(nodos):
        if nn !=nodos_x_vta*float(spring.vueltas):
          dispGlob.append(displaceMatrix[nn]+displaceMatrix[nn+1])

      for mm in range(nodos):
        if mm !=nodos_x_vta*float(spring.vueltas):
          dispglob1 = dispGlob[mm]
          dispLoc.append(np.dot(vectorT[mm],np.transpose(dispglob1)))
      
      storeForces.append(forceMatrix)
      storeDispl.append(displaceMatrix)

      # CALCULO DE ESFUERZOS

      stressMatrix=[] #Matriz de esfuerzos, tendremos 6 esfuerzos por fila (cada elemento es una fila tendra sus esfuerzos)

      cuy=[]
      cdz=[]
      cdy=[]
      cuz=[]
      vmuy=[]
      vmdz=[]
      vmdy=[]
      vmuz=[]

      for pq in range(nodos):
        if pq !=nodos_x_vta*float(spring.vueltas):
          longitud = Long[pq]
          u1 =    dispLoc[pq][0]
          u2 =    dispLoc[pq][6]
          v1 =    dispLoc[pq][1]
          v2 =    dispLoc[pq][7]
          w1 =    dispLoc[pq][2]
          w2 =    dispLoc[pq][8]
          angx1 = dispLoc[pq][3] 
          angx2 = dispLoc[pq][9]
          angy1 = dispLoc[pq][4] 
          angy2 = dispLoc[pq][10]
          angz1 = dispLoc[pq][5] 
          angz2 = dispLoc[pq][11]
          radio = float(spring.alambre)/2
  
          phiz=12*youngModulus*inercia/(kappa*shearModulus*area*math.pow(longitud,2))
          phiy=12*youngModulus*inercia/(kappa*shearModulus*area*math.pow(longitud,2))
          phibar_z=1/(1+phiz)
          phibar_y=1/(1+phiy)

          s1 = youngModulus*(u2-u1)/longitud
          t1 = shearModulus*(angx2-angx1)*radio/longitud
          s2 = youngModulus*radio*(angz2-angz1)/longitud
          t2 = -shearModulus*phiz*phibar_z*(2*v1+angz1*longitud-2*v2+angz2*longitud)/(2*longitud)
          s3 = youngModulus*radio*(angy2-angy1)/longitud
          t3 = -shearModulus*phiy*phibar_y*(2*w1-angy1*longitud-2*w2-angy2*longitud)/(2*longitud)

          elemStress = []

          elemStress.append(longitud)
          elemStress.append(v1)
          elemStress.append(angz1)
          elemStress.append(v2)
          elemStress.append(angz2)
          elemStress.append(w1)
          elemStress.append(angy1)
          elemStress.append(w2)
          elemStress.append(angy2)
          elemStress.append(phiz)
          elemStress.append(phiy)
          elemStress.append(phibar_z)
          elemStress.append(phibar_y)
          elemStress.append(s1)
          elemStress.append(t1)
          elemStress.append(s2)
          elemStress.append(t2)
          elemStress.append(s3)
          elemStress.append(t3)
          #elemStress.append(phiz)
          #elemStress.append(phiy)
          #elemStress.append(phibar_z)
          #elemStress.append(phibar_y)

          esfNorm_UP_Y        = s1-s3
          esfNorm_DOWN_Z      = s1-s2
          esfNorm_DOWN_Y      = s1+s3
          esfNorm_UP_Z        = s1+s2
          esfCorte_UP_Y       = t1+t2
          esfCorte_DOWN_Z     = t1-t3
          esfCorte_DOWN_Y     = t1-t2
          esfCorte_UP_Z       = t1+t3
          esfVonMises_UP_Y    = math.pow(math.pow(esfNorm_UP_Y,  2)+3*math.pow(esfCorte_UP_Y,  2),0.5)
          esfVonMises_DOWN_Z  = math.pow(math.pow(esfNorm_DOWN_Z,2)+3*math.pow(esfCorte_DOWN_Z,2),0.5)
          esfVonMises_DOWN_Y  = math.pow(math.pow(esfNorm_DOWN_Y,2)+3*math.pow(esfCorte_DOWN_Y,2),0.5)
          esfVonMises_UP_Z    = math.pow(math.pow(esfNorm_UP_Z,  2)+3*math.pow(esfCorte_UP_Z,  2),0.5)
          
          elemStress.append(esfNorm_UP_Y        )
          elemStress.append(esfNorm_DOWN_Z      )
          elemStress.append(esfNorm_DOWN_Y      )
          elemStress.append(esfNorm_UP_Z        )
          elemStress.append(esfCorte_UP_Y       )
          elemStress.append(esfCorte_DOWN_Z     )
          elemStress.append(esfCorte_DOWN_Y     )
          elemStress.append(esfCorte_UP_Z       )
          elemStress.append(esfVonMises_UP_Y    )
          elemStress.append(esfVonMises_DOWN_Z  )
          elemStress.append(esfVonMises_DOWN_Y  )
          elemStress.append(esfVonMises_UP_Z    )

          stressMatrix.append(elemStress)

          vmuy.append(esfVonMises_UP_Y)
          vmdz.append(esfVonMises_DOWN_Z)
          vmdy.append(esfVonMises_DOWN_Y)
          vmuz.append(esfVonMises_UP_Z)

          cuy.append(abs(esfCorte_UP_Y  ))
          cdz.append(abs(esfCorte_DOWN_Z))
          cdy.append(abs(esfCorte_DOWN_Y))
          cuz.append(abs(esfCorte_UP_Z  ))

      vmuyMAX = np.max(vmuy)
      vmdzMAX = np.max(vmdz)
      vmdyMAX = np.max(vmdy)
      vmuzMAX = np.max(vmuz)
      cuyMAX = np.max(cuy)
      cdzMAX = np.max(cdz)
      cdyMAX = np.max(cdy)
      cuzMAX = np.max(cuz)

      storeStress.append(stressMatrix)
      
      storevmuy.append(vmuyMAX)
      storevmdz.append(vmdzMAX)
      storevmdy.append(vmdyMAX)
      storevmuz.append(vmuzMAX)
      storecuy.append(cuyMAX)
      storecdz.append(cdzMAX)
      storecdy.append(cdyMAX)
      storecuz.append(cuzMAX)

    # showResults(stressMatrix,deltaY,"Stress")

    # RESUMEN
    storeSummary.append(storeForceSum )
    storeSummary.append(storevmuy     )
    storeSummary.append(storevmdz     )
    storeSummary.append(storevmdy     )
    storeSummary.append(storevmuz     )
    storeSummary.append(storecuy      )
    storeSummary.append(storecdz      )
    storeSummary.append(storecdy      )
    storeSummary.append(storecuz      )

    # showResults(storeSummary,deltaY,"RESUMEN")

    return storeSummary
    # return [node_array, node_theta, node_vta]


# Calcula coordenada X del nodo. Entrada: Posicion angular en grados sexagesimales.
def node_coordX(nodeValue, radio):
  return radio * math.cos(nodeValue * math.pi / 180)

# Calcula coordenada Z del nodo. Entrada: Posicion angular en grados sexagesimales.
def node_coordZ (nodeValue, radio):                
  return -radio * math.sin(nodeValue * math.pi / 180)

def node_coordY(node_value, nodos_x_vta, spring, h_extremo1, h_extremo2, h_helice, h_cuerpo):                 #Calcula coordenada Y del nodo. Entrada: Posicion angular en fraccion de vuelta.
  if node_value<= 1:
    return ((node_value*360)**2)/(360*360/h_extremo1)
  elif node_value>(float(spring.vueltas) - 1):
    return ((node_value*360-float(spring.vueltas) * 360)**2) / ( 360 * 360 / ( -h_extremo2) ) + h_helice
  elif node_value>1 and node_value<=(float(spring.vueltas) - 1):
    inc = h_cuerpo / ((float(spring.vueltas) - 2) * 360) * 360 / nodos_x_vta
    return h_extremo1 + inc * ( node_value*nodos_x_vta-nodos_x_vta)

def sumMatrix(bigMatrix,matrix,indexROW,indexCOL): 
    """Suma los elementos una matriz (matrix) dentro de la matriz mayor (bigMatrix), desde unos índices iniciales (indexROW, indexCOL)."""
    m=0   
    for i in range(indexROW,indexROW+len(matrix)):
        n=0
        for j in range(indexCOL,indexCOL+len(matrix)):
            bigMatrix[i][j] = bigMatrix[i][j]+ matrix[m][n]
            n = n+1
        m=m+1
  
    return bigMatrix
