import grass.script as grass
import os
import math
import numpy





class GrassComands(object):
    def __init__(self,Map_vect_poits):
        self.Map_vect_poits=Map_vect_poits
        self.Xcoord_list="" # essa lista sera criada na funcao ReturnXY, e tera os valores das cordenadas do Xcoord
        self.Ycoord_list="" # essa lista sera criada na funcao ReturnXY, e tera os valores das cordenadas do Ycoord
        self.list_values=[]

    def addcol(self):
        grass.run_command ('v.db.addcol', map=self.Map_vect_poits, columns='X_Corrd double precision,Y_Corrd double precision,EucDMean double precision', overwrite = True) #adciona as colunas x y

    def UpdateCorrds(self):
        grass.read_command ('v.to.db', map=self.Map_vect_poits, option='coor', columns="X_Corrd,Y_Corrd", overwrite = True)  #atualiza as colunas X_Corrd,Y_Corrd com as coordenadas


    def ReturnXY(self):

        Xcoord=grass.read_command('v.db.select',map=self.Map_vect_poits,column='X_Corrd') # retorna as corrdenadas da coluna x
        Xcoord_split=Xcoord.split("\n");Xcoord_split.remove("");Xcoord_split.remove("X_Corrd"); Xcoord_split=map(float, Xcoord_split) #limpando a lista removendo espacos em branco e transformando tudo em float
        self.Xcoord_list=Xcoord_split

        Ycoord=grass.read_command('v.db.select',map=self.Map_vect_poits,column='Y_Corrd') # retorna as corrdenadas da coluna y
        Ycoord_split=Ycoord.split("\n");Ycoord_split.remove("");Ycoord_split.remove("Y_Corrd"); Ycoord_split=map(float, Ycoord_split) #limpando a lista removendo espacos em branco e transformando tudo em float
        self.Ycoord_list=Ycoord_split





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
        count=0
        for i in self.Xcoord_list:
            query="X_Corrd="+`i`
            grass.read_command('v.db.update',map=self.Map_vect_poits,col='EucDMean',value=self.list_values[count],where=query)
            count=count+1    







class Main(GrassComands):
    def __init__(self, Map_vect_poits):
        GrassComands.__init__(self, Map_vect_poits)
    def Run(self):
        GrassComands.addcol(self) # chama a funcao que add as colunas
        GrassComands.UpdateCorrds(self) # chama funcao que atualiza as coordenadas para as colunas X e Y
        GrassComands.ReturnXY(self) # pega as 
        GrassComands.CalculaEucdist(self)
        GrassComands.UpdateValueMeanDist(self)




Map_vect_poits="Point_selecionados_10_shp"
EstanciaPrincipal=Main(Map_vect_poits)   
EstanciaPrincipal.Run()
