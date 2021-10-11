"""
Created on Mon Sep 20 20:21:02 2021

@author: MonicaYazmin
"""
import csv

registros = []

with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    registros = list(lector)
  
#Opción 1) Rutas de importación y exportación: las 10 rutas más demandadas

def rutas_exp_imp (direction):
    contador = 0
    valor = 0
    rutas_contadas = []
    rutas_conteo = []
    
    for ruta in registros:
        if ruta["direction"] == direction:
            ruta_actual = [ruta["origin"], ruta["destination"]]
            #print(ruta_actual)
            if ruta_actual not in rutas_contadas:
                for ruta_bd in registros:
                    if ruta_actual == [ruta_bd["origin"], ruta_bd["destination"]]:
                        contador += 1
                        valor = valor + int(ruta["total_value"])
                
                rutas_contadas.append(ruta_actual)
                rutas_conteo.append([ruta["origin"], ruta["destination"], contador, valor])
                contador = 0
                valor = 0
    
    rutas_conteo.sort(reverse = True, key = lambda x:x[3])
    return rutas_conteo
                    


conteo_exportaciones = rutas_exp_imp("Exports")
conteo_importaciones = rutas_exp_imp("Imports")

print("""-----------------------------------------------------------------------------------------\n<<<<<<<<<<< I M P O R T I N G  R O U T E S:  S Y N E R G Y  L O G I S T I C S >>>>>>>>>>>\n-----------------------------------------------------------------------------------------""")    
print ("{:<25} {:<25} {:<25} {:<25}".format("Origin", "Destination", "Frequency", "Total value"))
print("-----------------------------------------------------------------------------------------")

for v in conteo_importaciones:
    Origin, Destination, Frequency, Total = v
    print ("{:<25} {:<25} {:<25} {:<25}".format( Origin, Destination, Frequency, Total))

print("""-----------------------------------------------------------------------------------------\n<<<<<<<<<<< E X P O R T I N G  R O U T E S:  S Y N E R G Y  L O G I S T I C S >>>>>>>>>>>\n-----------------------------------------------------------------------------------------""")    
print ("{:<25} {:<25} {:<25} {:<25}".format("Origin", "Destination", "Frequency", "Total value"))
print("-----------------------------------------------------------------------------------------")

for w in conteo_exportaciones:
    Origin, Destination, Frequency, Total = w
    print ("{:<25} {:<25} {:<25} {:<25}".format( Origin, Destination, Frequency, Total))

#Opción 2) Medio de transporte utilizado de importación y exportación: los 3 medios de transporte más importantes
    transportes = {}
    
    for line in registros:
        transportes[line['transport_mode']] = transportes.get(line['transport_mode'],[]) + [line['total_value']]
        
    
    transportes_valores ={}
    for transporte, valor_lista in transportes.items():
        valor_suma = 0
        for valor in valor_lista:
            valor_suma = valor_suma + int(valor)
        transportes_valores[transporte] = valor_suma
        
        lista_transportes_valores = zip(transportes_valores.keys(), transportes_valores.values())
        lista_transportes_valores = list(lista_transportes_valores)
        lista_transportes_valores.sort(reverse = True)
   
print("""-----------------------------------------------------------------------------------------\n<<<<<<<<<<<<  T R A N S P O R T  M O D E :  S Y N E R G Y  L O G I S T I C S >>>>>>>>>>>>\n-----------------------------------------------------------------------------------------""")    
print ("{:<25} {:<25}".format("Transport mode", "Total value"))
print("-----------------------------------------------------------------------------------------")

for m in lista_transportes_valores:
    Transport, Total = m
    print ("{:<25} {:<25}".format( Transport, Total))

#Opción 3) Valor total de importaciones y exportaciones: paises que generan el 80%
        

def valor_movimiento(direccion):
	contados = []
	valores_paises = []

	for viaje in registros:
		actual = [direccion, viaje["origin"]] 
		valor = 0
		operaciones = 0

		if actual in contados:
			continue

		for movimiento in registros:
			if actual == [movimiento["direction"], movimiento["origin"]]:
				valor += int(movimiento["total_value"])
				operaciones += 1
		
		contados.append(actual)
		valores_paises.append([direccion, viaje["origin"], valor, operaciones])
	
	valores_paises.sort(reverse = True, key = lambda x:x[2])
  
	return valores_paises


valores_paises = valor_movimiento("Exports")


def porcentaje_pais(lista_paises, porcentaje = 0.8):
	valor_total = 0
	for pais in lista_paises:
		valor_total += pais[2]
	
	paises = []
	porcentajes_calculados = []
	valor_actual = 0

	for pais in lista_paises:
		valor_actual += pais[2]
		porcentaje_actual = round(valor_actual/valor_total, 3)
		paises.append(pais)
		porcentajes_calculados.append(porcentaje_actual)

		if porcentaje_actual <= porcentaje:
			continue
		else:
			if porcentaje_actual - porcentaje <= porcentajes_calculados[-2] - porcentaje:
				break
			else:
				paises.pop(-1)
				porcentajes_calculados.pop(-1)
				break
	
	return paises


paises_80 = porcentaje_pais(valor_movimiento("Exports"))
paises80 = porcentaje_pais(valor_movimiento("Imports"))


  
print("""-----------------------------------------------------------------------------------------\n<<<<<<<<<<<<<<<<<<<  E X P O R T S:  S Y N E R G Y  L O G I S T I C S >>>>>>>>>>>>>>>>>>>\n   C O U N T R I E S  T H A T  G E N E R A T E  8 0 %  O F  T H E  T O T A L  V A L U E \n-----------------------------------------------------------------------------------------""")    
print ("{:<25} {:<25} {:<25} {:<25}".format("Direction", "Country", "Total value", "Operations"))
print("-----------------------------------------------------------------------------------------")

for z in paises_80:
    Direction, Country, Total, Operations = z
    print ("{:<25} {:<25} {:<25} {:<25}".format( Direction, Country, Total, Operations))


print("""-----------------------------------------------------------------------------------------\n<<<<<<<<<<<<<<<<<<<  I M P O R T S:  S Y N E R G Y  L O G I S T I C S >>>>>>>>>>>>>>>>>>>\n   C O U N T R I E S  T H A T  G E N E R A T E  8 0 %  O F  T H E  T O T A L  V A L U E \n-----------------------------------------------------------------------------------------""")    
print ("{:<25} {:<25} {:<25} {:<25}".format("Direction", "Country", "Total value", "Operations"))
print("-----------------------------------------------------------------------------------------")

for y in paises80:
    Direction, Country, Total, Operations = y
    print ("{:<25} {:<25} {:<25} {:<25}".format( Direction, Country, Total, Operations))
