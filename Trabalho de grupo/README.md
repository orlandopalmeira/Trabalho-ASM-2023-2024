# Receções de mensagem

## Airport

- Receber flights (origem -> destino) vindos da central (performative: *request*, body: *Trip*)

## Torre de Controlo (CT)

- Receber avião vindo do **hangar** e começar a viagem (performative: *inform*, body: *{plane_jid: String, trip: Trip}*)
- Receber confirmação de descolagem do **avião** (performative: *confirm*, body: *"plane_jid"*)

- Receber pedidos de aterragem dos **aviões** perto do aeroporto destino (performative: *request*, body: *"plane_jid"*)
- Receber confirmação de aterragem do **avião** (performative: *inform*, body: *"plane_jid"*)

## Hangar

- Recebe mensagem do **aeroporto** origem para disponibilizar avião à CT origem (performative: *request*, body: *Trip*)

- Recebe mensagem de um **avião** para que o armazene, após concluir aterragem (performative: *inform*, body: *"plane_jid"*)

## Plane

- Recebe mensagem da **CT** origem para começar a viagem (performative: *inform*, body: *Trip*)

- Recebe mensagem da **CT** destino para aterrar (performative: *confirm*, body: *None*)


## Central

- (WIP) Pedidos de gestão de stock do hangar para balancear hangares WIP (performative: *???*, body: *???*)

# Use cases
## 1. Realizar um flight (DESCOLAGEM)
1. A **central** envia um flight ao **aeroporto**. (performative: *request*, body: *Trip*)
2. O **aeroporto** envia um pedido de avião ao **hangar**. (performative: *request*, body: *Trip*)
3. O **hangar** envia o jid do avião selecionado à **CT**. (performative: *inform*, body: *{plane_jid: String, trip: Trip}*)
4. A **CT** envia mensagem para descolar ao **Plane**. (performative: *inform*, body: *Trip*)
    - A CT reserva uma runway para a descolagem e fica à espera que o avião indique que a descolagem acabou.
5. O **Plane** envia mensagem de confirmação de descolagem à **CT**. (performative: *confirm*, body: *"plane_jid"*)


Notas:
- Flight: (Central -> (Trip) -> Aeroporto -> (Trip) -> Hangar -> (Trip,Avião) -> CT -> (Trip) -> Avião)
- CT mantém estado de ocupação do hangar para fazer uma espécie de reserva de lugares e não permite aterragens quando o hangar está cheio.

# 2. Realizar um flight (ATERRAGEM)
1. O **Plane** envia mensagem de pedido de aterragem à **CT**. (performative: *request*, body: *"plane_jid"*)
2. A **CT** verifica se as condições permitem aterrar, e envia mensagem ao **Plane**. (performative: *confirm*, body: *None*)
    - As condições são: runways disponíveis, hangares disponíveis, condições meteorológicas favoráveis.
3. O **Plane** envia mensagem de aterragem à **CT** e ao **Hangar**. (performative: *inform*, body: *"plane_jid"*)


# ideia de gestão do CT

- sempre que um hangar manda pedido de voo para a CT, a CT guarda o pedido numa queue. Sempre que é adicionado um pedido à queue, é lançado um oneshotbehavior(DispatchPlanes) que checka a queue e faz um `for flight in queue: if all_condition_are_met: descolar_aviao()`. Este behavior dá prioridade aos voos que estão há mais tempo na queue e também que são de levantar, para que depois não haja deadlocks ao tentar aterrar um avião e o hangar estar cheio.
Este DispatchPlanes tbm é acionado sempre que um avião é posto no hangar e ele estava vazio. Tbm sempre que as condições meteorologicas passem a estar boas, o DispatchPlanes é acionado.