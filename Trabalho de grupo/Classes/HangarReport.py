import time

class HangarReport:
    SCARSE  = "scarse"
    CROWDED = "crowded"

    def __init__(self, mode, location, priority):
        """
        Cria um objeto HangarReport com os seguintes atributos:
        mode: SCARSE ou CROWDED
        location: Localização do hangar
        priority: Número de vagas disponíveis ou por ocupar, dependendo se é SCARSE ou CROWDED, respetivamente. Quanto menor, mais urgente.
        timestamp: Timestamp da criação do objeto
        """
        if mode not in [HangarReport.SCARSE, HangarReport.CROWDED]:
            raise ValueError(f"Invalid mode: {mode}. Possible values: {HangarReport.SCARSE} as HangarReport.SCARSE, {HangarReport.CROWDED} and HangarReport.CROWDED")
        self.type = mode
        self.location = location
        self.priority = priority # Número de vagas disponíveis ou por ocupar, dependendo se é SCARSE ou CROWDED, respetivamente.
        self.timestamp = time.time()

    def get_type(self) -> str:
        return self.type

    def get_location(self) -> str:
        return self.location
    
    def get_priority(self) -> int:
        return self.priority
    
    def get_timestamp(self) -> float:
        return self.timestamp
    
    def decrease_priority(self):
        self.priority -= 1
    
    def __str__(self) -> str:
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        return f"{self.location} ({self.priority}) ({date})"
    
    def __lt__(self, other):
        if self.priority == other.priority:
            return self.timestamp > other.timestamp
        return self.priority < other.priority



if __name__ == "__main__":
    location = "Lisboa"
    priority = 2
    r  = HangarReport(HangarReport.SCARSE, location, 3)
    r2 = HangarReport(HangarReport.SCARSE, location, 3)
    res = r > r2
    print(res)