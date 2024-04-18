
class Config:
    DOMAIN = "laptop-140rfmpg.home" #! Meter este valor a ser lido de um .env (talvez)
    central_jid = f"central@{DOMAIN}"

    @staticmethod
    def get_domain_name():
        return Config.DOMAIN
    
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

