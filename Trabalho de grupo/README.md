# Receções de mensagem
## Airport

- Receber flights (origem -> destino) vindos da central

## Torre de Controlo (CT)
Irá gerir a ocupação das runways e o estado do tempo.

- Receber avião vindo do hangar e começar a viagem (pedidos de descolagem)
- Receber pedidos de aterragem dos aviões perto do aeroporto destino (pedidos de aterragem)

## Plane

- Recebe mensagem da CT origem para começar a viagem (start_trip)
- Recebe mensagem da CT destino para aterrar (land)


## Hangar

- Recebe mensagem do aeroporto origem para disponibilizar avião à CT origem
- Recebe mensagem da CT destino para armazenar avião


## Central

- (WIP) Pedidos de gestão de stock do hangar para balancear hangares WIP

# Use cases
## 1. Realizar um flight
1. A **central** envia um flight ao **aeroporto**. (performative:, body: )
2. O **aeroporto** envia um pedido de avião ao **hangar**. (performative:, body: )
3. O **hangar** envia o jid do avião selecionado à **CT**. (performative:, body: )
4. A **CT** envia mensagem para descolar ao **Plane**. (performative:, body: )

Flight: (Central -> (Trip) -> Aeroporto -> (Trip) -> Hangar -> (Trip,Avião) -> CT -> (Trip) -> Avião)