# Receções de mensagem
## Airport

- Receber flights (origem -> destino) vindos da central (performative: *request*, body: *Trip*)

## Torre de Controlo (CT)
Irá gerir a ocupação das runways e o estado do tempo.

- Receber avião vindo do hangar e começar a viagem (performative: *inform*, body: *Trip*)
- Receber pedidos de aterragem dos aviões perto do aeroporto destino (pedidos de aterragem)

## Plane

- Recebe mensagem da CT origem para começar a viagem (performative: *inform*, body: *Trip*)
- Recebe mensagem da CT destino para aterrar (land)


## Hangar

- Recebe mensagem do aeroporto origem para disponibilizar avião à CT origem (performative: *request*, body: *Trip*)
- Recebe mensagem da CT destino para armazenar avião


## Central

- (WIP) Pedidos de gestão de stock do hangar para balancear hangares WIP

# Use cases
## 1. Realizar um flight (DESCOLAGEM)
1. A **central** envia um flight ao **aeroporto**. (performative: *request*, body: *Trip*)
2. O **aeroporto** envia um pedido de avião ao **hangar**. (performative: *request*, body: *Trip*)
3. O **hangar** envia o jid do avião selecionado à **CT**. (performative: *inform*, body: *{plane_jid: String, trip: Trip}*)
4. A **CT** envia mensagem para descolar ao **Plane**. (performative: *inform*, body: *Trip*)
    - A CT reserva uma runway para a descolagem e fica à espera que o avião indique que a descolagem acabou.
?-5. O **Plane** envia mensagem de descolagem à **CT**. (performative: *inform*, body: *plane_jid*)


Notas:
- Flight: (Central -> (Trip) -> Aeroporto -> (Trip) -> Hangar -> (Trip,Avião) -> CT -> (Trip) -> Avião)
- CT mantém estado de ocupação do hangar para fazer uma espécie de reserva de lugares e não permite aterragens quando o hangar está cheio.