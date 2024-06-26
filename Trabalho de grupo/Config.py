import os

class Config:

    DOMAIN = os.getenv("DOMAIN")
    if not DOMAIN:
        print("ERROR: DOMAIN not found in .env file")
    PASSWORD = os.getenv("PASSWORD")
    central_jid = f"central@{DOMAIN}"

    @staticmethod
    def get_domain_name():
        return Config.DOMAIN
    
    @staticmethod
    def get_password():
        return Config.PASSWORD
    
    @staticmethod
    def get_jid_name(jid):
        str_jid = str(jid)
        return str_jid.split("@")[0]
    
    @staticmethod
    def get_central_jid():
        """Retorna o jid da central."""
        return Config.central_jid
    
    @staticmethod
    def get_airport_jid(location):
        """Dado uma localização, retorna o jid do aeroporto dessa localização."""
        location = location.lower().replace(" ", "_")
        return f"airport_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_hangar_jid(location):
        """Dado uma localização, retorna o jid do hangar dessa localização."""
        # Make sure the location is lowercase and if there are spaces, replace them with underscores
        location = location.lower().replace(" ", "_")
        return f"hangar_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_ct_jid(location):
        """Dado uma localização, retorna o jid da control tower dessa localização."""
        location = location.lower().replace(" ", "_")
        return f"ct_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_plane_jid(id):
        """Dado um id, retorna o jid do avião."""
        return f"plane_{id}@{Config.DOMAIN}"
    
    @staticmethod
    def get_meteo_jid():
        return f"meteo@{Config.DOMAIN}"
    
    @staticmethod
    def identify(jid):
        """Dado um jid, identifica o tipo de agente que ele é."""
        str_jid = str(jid)
        if str_jid.startswith("airport"):
            return "airport"
        elif str_jid.startswith("hangar"):
            return "hangar"
        elif str_jid.startswith("plane"):
            return "plane"
        elif str_jid.startswith("ct"):
            return "ct"
        elif str_jid.startswith("central"):
            return "central"
        elif str_jid.startswith("meteo"):
            return "meteo"
        
        return "unknown"
    
    def get_good_weather():
        return "Clear"
    
    def get_bad_weather():
        return "Thunderstorm"

    def get_mid_weather():
        return "Rain" 
    
    @staticmethod
    def meteo_file_name():
        """Retorna a string da diretoria do ficheiro de meteorologia para alteração manual."""
        return "resources/meteo.json"

    @staticmethod
    def stats_file_name():
        """Retorna a string da diretoria do ficheiro de estatísticas."""
        return "resources/flights.json"
