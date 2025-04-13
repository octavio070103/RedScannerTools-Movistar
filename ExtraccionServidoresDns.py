'''DNS es un sistema distribuido que funciona como un directorio que traduce los nombre de dominio en direccion IP para la PC esto ayuda 
a que en lugar de recordar direcciones IP larga y complicas utilizemos nombres de dominios mas faciles de recordar
Aca buscamos realizar una consulta DNS(sistema de nombres de dominio) sobre el dominio que le  pasamos'''

import dns #importa el modulo dns que da funciones para trabajar con consultas y respuestas DNS en python
import dns.resolver #importamos el modulo resolver de dns que nos sirve para realizar resoluciones de nombres

#Realizamos consultas Dns
registroA = dns.resolver.query('wikipedia.org','A')  #Obtenemos los registros de tipo A (tienen la direccion Ipv4 asociada a un dominio 'wikipedia')
registroAAAA = dns.resolver.query('wikipedia.org','AAAA')#Obtenemos los registros tipo AAAA(tiene la direccion IPv6 de un dominio 'wikipedia')
registroNS = dns.resolver.query('wikipedia.org','NS')#Obtiene los registros de tipo NS(servidores de nombre para una entrada DNS)
registroMX = dns.resolver.query('wikipedia.org','MX')#obtiene los registro MX(servidores de correo)asociados a un dominio en este caso wikipedia
print(registroNS.response.to_text())#muestra el texto contenido en la respuesta del objeto registroNS.

