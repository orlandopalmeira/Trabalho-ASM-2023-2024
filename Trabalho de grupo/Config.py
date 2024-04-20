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
        return jid.split("@")[0]
    
    @staticmethod
    def get_central_jid():
        return Config.central_jid
    
    @staticmethod
    def get_airport_jid(location):
        return f"airport_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_hangar_jid(location):
        return f"hangar_{location}@{Config.DOMAIN}"
    
    @staticmethod
    def get_plane_jid(id):
        return f"plane_{id}@{Config.DOMAIN}"
    
    @staticmethod
    def get_control_tower_jid():
        return f"ct_{id}@{Config.DOMAIN}"

