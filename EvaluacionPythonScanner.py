import socket #nos proporciona acceso a las interfaces de red de bajo nivel
import sys
import os
import threading

# I define the functions i will use for my scan
# 1)Descubrir mi IP
def get_my_ip():
    # Obtiene la IP de la propia máquina
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(("10.255.255.255", 1))
        ip = st.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        st.close() #close socket
    return ip 
    
# 2)Escanear Mi red para descubrir Los dispositivos conectados
def scan_network(ip_addres):
    list_ips_network= []#va a contener u a lista de las ip de los dispositivos conectados a mi red
    def ping_network_local(current_ip):
    
        comando="ping -c 1 "+current_ip
        response=os.popen(comando).read()
    
        if "1 received" in response:
            list_ips_network.append(current_ip)
            print(current_ip)
        
    print("IP De Dispositivos conecatados a mi red:")
    for i in range(1,254) :
        current_ip= ip_addres+"."+str(i)# aca concatenamos el numero que se esta recorriendo en ese momento del for para completar el octeto de mi ip
        run=threading.Thread(target=ping_network_local ,args=(current_ip,))
        run.start()   
    return list_ips_network


#3)Escanear puertos de una IP
def scan_port_ip(ip_addres,p_resp):
    def get_service_name(port):
        try:
            service_name = socket.getservbyport(port)
            return service_name
        except OSError :
            return "Unknown"


    def scan_ports(target_ip, ports):
        open_ports = []  # Lista para almacenar los puertos abiertos
        closed_ports = []  # Lista para almacenar los puertos cerrados
        
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # Establece un tiempo de espera para la conexión
            
            try:
                s.connect((target_ip, port))
                open_ports.append(port)
                s.close()
            except (socket.timeout, ConnectionRefusedError):
                closed_ports.append(port)
                pass
        
        return open_ports,closed_ports #retornamos ambas lista con tantos los puertos open and closed

    target_ip=ip_addres
    resp=p_resp
    if resp == 1:
        ports=range(1,65536)
    elif resp==2:
        ports = [21, 22, 25, 53, 79, 80, 110, 143, 443, 534,8080]   # Lista de puertos que quieres escanear en este caso lo mas importantes
    elif resp==3:
        ports=range(1,65536)
    elif resp==4:
        ports=range(1,65536)
    else:
        print("ingrese un valor valido")
    
    print(f"\nEscaneando puertos en {target_ip}...")
    
    try:
        open_ports, closed_ports = scan_ports(target_ip, ports)
    except Exception as e:
        print(f"\n\nError al escanear puertos: {e}")
        open_ports, closed_ports = [], []
    
    if open_ports and resp!=4: #verficia si la lista contiene elementos si tiene elem entra al if sino va al else
        print("\tPuertos Abiertos")
        print("PORT    STATE   SERVICE")
        for port in open_ports:
            service_name = get_service_name(port)
            print(f"{port}/TCP  OPEN    {service_name}")
    else:
        print("No open ports found.")
     
        
    if closed_ports and resp!=3 :#verficia si la lista contiene elementos si tiene elem entra al if sino va al else
        print("\t\nPuertos Cerrados")
        print("PORT    STATE   SERVICE")
        for port in closed_ports:
            service_name = get_service_name(port)
            print(f"{port}/TCP  CLOSE    {service_name}")
    else:
        print("No open ports found.")
    

#4)Escanear puertos mas importantes de las IPs conectada a mi red
def scan_ports_network(p_list_ips_network):
    print("Escaneo de puertos de las IPs conectada a mi red")
    for ip_network in p_list_ips_network:
        scan_port_ip(ip_network,2) #le digo que me haga el esceno de tipo 2(solo puertos improtantes)
   
#5)Detectar la version de los servicios y el SO
def detect_version_OS_ip():
    print("en reparacion")
    
#6)escaneo completo de la red intentando ser lo mas silencioso y profesional posible
def scan_completed_network(p_ip_addres):
    import subprocess

    def run_nmap_command(command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    # Ejemplo de comando nmap a ejecutar
    nmap_command = "nmap -Pn -sT -A -T2 -sV -F "+p_ip_addres

    # Ejecutar el comando nmap
    run_nmap_command(nmap_command)

#7)escaneo rapido de la red buscando rapidez pero sacrificando el silencio y demas datos que no son principales
def scan_fast_network(p_ip_addres):
    import subprocess

    def run_nmap_command(command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    # Ejemplo de comando nmap a ejecutar
    nmap_command = "nmap -Pn -sT -A "+p_ip_addres

    # Ejecutar el comando nmap
    run_nmap_command(nmap_command)

#8)detecta los puertos abiertos TCP y UDO mostrando el banner del servicio con la tecnica Banner Grabbing
def ports_banner_grabbing(p_list_ips_network):
    
    ports = [21, 22, 25, 534, 79, 80, 110, 443, 8080]
    
    for ip_actual in p_list_ips_network:
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((ip_actual,port))
                banner = s.recv(1024)
                print("Banner encontrado en IP = " + ip_actual + ", puerto = " + str(port))
                print("Banner = " + banner.decode())
            except socket.error as e:
                print(f"Error al conectar a {ip_actual}, puerto {port}: {e}")
            finally:
                s.close()

def main():
    respuesta = 1
    while int(respuesta) !=0 :
        print("**************** Escaner De Redes ****************")
        print('''\t0)Pulse 0 para salir del Programa
                1)Descubrir mi IP
                2)Escanear Mi red para descubrir Los dispositivos conectados
                3)Escanear puertos de una IP
                4)Escanear puertos mas importantes de las IPs conectada a mi red
                5)Detectar la version de los servicios y el SO
                6)Realizar un escaneo completo de la red
                7)Realizar un escaneo rapido de la red
                8)mostrar los puertos TCP y UDP con el banner del servicio(Banner Grabbing)
            ''')
        respuesta=int(input("Seleccione una opcion: "))
        
        if respuesta == 0:
            break
        elif respuesta == 1 : 
            print("Tu dirección IP es: ", get_my_ip())#we call the fuction get_my_ip that contains get my ip      
        elif respuesta == 2 : 
            ip=get_my_ip()
            subnet=".".join(ip.split(".")[:-1])
            scan_network(subnet)#we call the fuction scan_network that contains a network scanner
        elif respuesta == 3 :
            ip=input("Ingrese la Ip de la red que quiere ver los puertos: ")
            resp=int(input('''Tipo de Escaneo
                1)Escanear todos los puertos
                2)Escanear solo lo mas importantes'
                3)Obtener solo los puertos abiertos
                4)Obtener solo los puertos cerrados
                respuesta: '''))
            scan_port_ip(ip,resp)#we call the futction that I scanned the ports through a certain IP 
        elif respuesta == 4 :
            ip=get_my_ip()
            subnet=".".join(ip.split(".")[:-1])#obtengo los ultimos 3 octetos de mi ip para poder obtener los ip dentro de mi red
            #obtengo la lista de las ip dentro de mi red 
            list_ips_network=scan_network(subnet)#we call the fuction scan_network that contains a network scanner
            scan_ports_network(list_ips_network)
            
        elif respuesta == 5 :
            ip_addres=input("Ingrese la Ip de la red que quiere ver el SO ")
            detect_version_OS_ip(ip_addres)
        elif respuesta == 6 :
            ip_addres=input("Ingrese la Ip o el rango de Ip de la red que quiere escanear de forma completa")
            scan_completed_network(ip_addres)
        elif respuesta == 7 :
            ip_addres=input("Ingrese la Ip o el rango de Ip de la red que quiere escanear de forma rapida")
            scan_fast_network(ip_addres)
        elif respuesta == 8 :
            ip=get_my_ip()
            subnet=".".join(ip.split(".")[:-1])
             #obtengo la lista de las ip dentro de mi red 
            list_ips_network=scan_network(subnet)#we call the fuction scan_network that contains a network scanner
            ports_banner_grabbing(list_ips_network)#obtengo los servicio UDP y TCP mas relevantes con bannergrabing,le paso las ips de mi red
        
        else:
                print("Opción no válida. Por favor, selecciona una opción válida.")
                
if __name__ == "__main__": #es una construcción común en Python que se utiliza para determinar si el script se está ejecutando como un programa principal o si se está importando como un módulo en otro script.
    main()