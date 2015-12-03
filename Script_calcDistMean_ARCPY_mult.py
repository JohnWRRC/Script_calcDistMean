import arcpy
import os
import numpy

folder=arcpy.GetParameterAsText(0)
os.chdir(folder)
fcs=arcpy.ListFeatureClasses()
class GrassComands(object):
    def __init__(self,Map_vect_poits):
        self.Map_vect_poits=Map_vect_poits
        self.Xcoord_list=[] # essa lista sera criada na funcao ReturnXY, e tera os valores das cordenadas do Xcoord
        self.Ycoord_list=[] # essa lista sera criada na funcao ReturnXY, e tera os valores das cordenadas do Ycoord
        self.list_values=[]        
        
        
    def addcol(self):
        try:
            arcpy.AddField_management(self.Map_vect_poits, "EucDMean", "DOUBLE", 20, 20)
        except:
            pass
        
    def UpdateCorrds(self):
        arcpy.AddGeometryAttributes_management(self.Map_vect_poits,"POINT_X_Y_Z_M","#","#","#")
        
    def ReturnXY(self):
        rows_point = arcpy.SearchCursor(self.Map_vect_poits,fields="POINT_X;POINT_Y")
        for row in rows_point:
            self.Xcoord_list.append(row.getValue("POINT_X"))
            self.Ycoord_list.append(row.getValue("POINT_Y"))
            
            
            
    #
    #def check_LatLong(self):
        #test=int(self.Xcoord_list[i])
        #if len(test)==2:
            
        #for i in xrange(len(self.Xcoord_list)):
            
    def CalculaEucdist(self ):
        for i in range(len(self.Xcoord_list)):
    
            Xa=self.Xcoord_list[i] # atribuindo o X fixo
            Ya=self.Ycoord_list[i] # atribuindo o X fixo
            #print "X",Xa," Y",Ya
            list_values_eucdists=[] # lista temporaria que vai guardar todos os valores das distancias medidsa para o ponto da vez
            for a in range(len(self.Xcoord_list)):
                Xb=self.Xcoord_list[a] # atribuindo o X variante
                Yb=self.Ycoord_list[a] # atribuindo o Y variante
                if Xa!=Xb and Ya!=Yb:
    
                    d = math.sqrt(abs((Xa-Xb) + (Ya-Yb))) # calculando a distancia entre pontos
                    #print "N",i,"Xa",Xa," Ya",Ya
    
                    list_values_eucdists.append(d)
            Mean=numpy.mean(list_values_eucdists)
            self.list_values.append(Mean)
    
    
    
    
    #
    def UpdateValueMeanDist(self):    
        rows = arcpy.UpdateCursor(self.Map_vect_poits) #this is my feature layer
        count=0
        for row in rows:
            row.setValue('EucDMean', self.list_values[count])
            rows.updateRow(row)
            count=count+1
        del rows    
        
    
#

class Main(GrassComands):
    def __init__(self, Map_vect_poits):
        GrassComands.__init__(self, Map_vect_poits)
    def Run(self):
        GrassComands.addcol(self) # chama a funcao que add as colunas
        GrassComands.UpdateCorrds(self) # chama funcao que atualiza as coordenadas para as colunas X e Y
        GrassComands.ReturnXY(self) # pega as 
        GrassComands.CalculaEucdist(self)
        GrassComands.UpdateValueMeanDist(self)




for Map_vect_poits in fcs:
    EstanciaPrincipal=Main(Map_vect_poits)   
    EstanciaPrincipal.Run() 

