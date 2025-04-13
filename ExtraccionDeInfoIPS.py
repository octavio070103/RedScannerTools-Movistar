import whois

def get_whois_info(domain):
    try:
        # Obtener información WHOIS para el dominio
        domain_info = whois.whois(domain)

        # Mostrar la información WHOIS
        print("Dominio:", domain_info.domain)
        print("Registrador:", domain_info.registrar)
        print("Fecha de creación:", domain_info.creation_date)
        print("Fecha de vencimiento:", domain_info.expiration_date)
        print("Servidores de nombres:", domain_info.name_servers)
        print("Servidor WHOIS:", domain_info.whois_server)
        print("Fecha de actualización:", domain_info.updated_date)

    except whois.parser.PywhoisError as e:
        print(f"Error: {e}")

# Ejemplo de uso
nombre_dominio = "wikipedia.org"
get_whois_info(nombre_dominio)
