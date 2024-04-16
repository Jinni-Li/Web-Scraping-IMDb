import requests
import builtwith
import whois
import os
class BackgroundResearch:
    def __init__(self, seed_page):
        self.seed_page = seed_page

    def robot_txt(self):
        """
        Devuelve el robot.txt de la seed_url.
        """
        try:
            domain = self.seed_page.split('/')[0] + '//' + self.seed_page.split('/')[2]
            resp = requests.get(domain + '/robots.txt', data=None)
            return resp.text
        except Exception as e:
            print("Error en la obtencion de robot.txt:", e)
            return None

    def tech_used(self):
        """
        Devuelve las tecnologías usadas en la construcción de la página.
        """
        try:
            tech = builtwith.parse(self.seed_page)
            return tech
        except Exception as e:
            print("Error en la obtencion de tecnologias utilizadas:", e)
            return None

    def get_domain_owner(self):
        """
        Retorna un diccionario con la información del propietario del dominio.
        """
        try:
            domain_info = whois.whois(self.seed_page)
            return domain_info
        except Exception as e:
            print("Error en la obtencion de informacion del propietario del dominio:", e)
            return None

    def perform_research(self, output_file):
        """
        Escribe el resultado en un archivo de texto.

        Parameters:
        -   output_file (str): El nombre del archivo de texto donde se escribirá el resultado.
        """
        try:
            output_path = os.path.join('dataset', output_file)
            with open(output_path, 'w') as file:
                file.write("################################\n"
                           "# Background Research IMDb.com #\n"
                           "################################\n"
                           "- Se realiza 3 investgaciones: robot.txt, tecnologias utilizadas de la web"
                           " y la informacion del dominio de la web.\n"
                           "- No se ha examidado el `sitemap` dado que IMDb.com no lo proporciona\n"
                           "- En este documento no se encuentran tildes debido a problemas del formato\n\n"
                           "#############\n"
                           "# Robot.txt #\n"
                           "#############\n")

                robot_txt = self.robot_txt()
                if robot_txt:
                    file.write(robot_txt)
                else:
                    file.write("No se pudo obtener el archivo robot.txt\n")

                file.write("\n\n"
                           "\n##########################\n"
                           "# Tecnologias utilizadas #\n"
                           "##########################\n")
                tech_used = self.tech_used()
                if tech_used:
                    file.write(str(tech_used))
                else:
                    file.write("No se pudo obtener informacion sobre las tecnologias utilizadas\n")

                file.write("\n\n"
                           "\n###########################################\n"
                           "# Informacion del propietario del dominio #\n"
                           "###########################################\n")
                domain_owner = self.get_domain_owner()
                if domain_owner:
                    file.write(str(domain_owner))
                else:
                    file.write("No se pudo obtener informacion sobre el propietario del dominio\n")

            print("La `Background Research` se ha completado y los resultados se han guardado en", output_file)
        except Exception as e:
            print("Error al escribir en el archivo de salida:", e)