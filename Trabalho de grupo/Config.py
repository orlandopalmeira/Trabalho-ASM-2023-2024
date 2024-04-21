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
        """Retorna o jid da central"""
        return Config.central_jid
    
    @staticmethod
    def get_airport_jid(location):
        """Dado uma localização, retorna o jid do aeroporto dessa localização"""
        return f"airport_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_hangar_jid(location):
        """Dado uma localização, retorna o jid do hangar dessa localização"""
        return f"hangar_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_control_tower_jid(location):
        """Dado uma localização, retorna o jid da control tower dessa localização"""
        return f"ct_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_plane_jid(id):
        """Dado um id, retorna o jid do avião"""
        return f"plane_{id}@{Config.DOMAIN}"
    
    @staticmethod
    def identify(jid):
        """Dado um jid, identifica o tipo de agente que ele é"""
        str_jid = str(jid)
        if str_jid.startswith("airport"):
            return "airport"
        if str_jid.startswith("hangar"):
            return "hangar"
        if str_jid.startswith("plane"):
            return "plane"
        if str_jid.startswith("ct"):
            return "ct"
        if str_jid.startswith("central"):
            return "central"
        return "unknown"

