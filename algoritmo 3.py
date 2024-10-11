class Proceso:
    def _init_(self, id, tiempo_llegada, tiempo_ejecucion, prioridad=None):
        self.id = id
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante = tiempo_ejecucion
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.prioridad = prioridad


def fcfs(procesos):
    tiempo_actual = 0
    for proceso in procesos:
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada
        proceso.tiempo_espera = tiempo_actual - proceso.tiempo_llegada
        proceso.tiempo_finalizacion = tiempo_actual + proceso.tiempo_ejecucion
        proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
        tiempo_actual += proceso.tiempo_ejecucion
    return procesos


def sjf(procesos):
    tiempo_actual = 0
    procesos_terminados = 0
    n = len(procesos)
    while procesos_terminados < n:
        procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and p.tiempo_finalizacion == 0]
        if not procesos_disponibles:
            tiempo_actual += 1
            continue
        proceso_actual = min(procesos_disponibles, key=lambda p: p.tiempo_ejecucion)
        tiempo_actual += proceso_actual.tiempo_ejecucion
        proceso_actual.tiempo_finalizacion = tiempo_actual
        proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
        proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_ejecucion
        procesos_terminados += 1
    return procesos


def round_robin(procesos, quantum):
    tiempo_actual = 0
    cola = []
    procesos_terminados = 0
    n = len(procesos)
    while procesos_terminados < n:
        for proceso in procesos:
            if proceso.tiempo_llegada == tiempo_actual:
                cola.append(proceso)
        if cola:
            proceso_actual = cola.pop(0)
            if proceso_actual.tiempo_restante > quantum:
                tiempo_actual += quantum
                proceso_actual.tiempo_restante -= quantum
                cola.append(proceso_actual)
            else:
                tiempo_actual += proceso_actual.tiempo_restante
                proceso_actual.tiempo_restante = 0
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_ejecucion
                procesos_terminados += 1
        else:
            tiempo_actual += 1
    return procesos


def psjf(procesos):
    tiempo_actual = 0
    procesos_terminados = 0
    n = len(procesos)
    while procesos_terminados < n:
        procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and p.tiempo_restante > 0]
        if not procesos_disponibles:
            tiempo_actual += 1
            continue
        proceso_actual = min(procesos_disponibles, key=lambda p: p.tiempo_restante)
        proceso_actual.tiempo_restante -= 1
        tiempo_actual += 1
        if proceso_actual.tiempo_restante == 0:
            proceso_actual.tiempo_finalizacion = tiempo_actual
            proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
            proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_ejecucion
            procesos_terminados += 1
    return procesos


def mlq(procesos, colas):
    tiempo_actual = 0
    procesos_terminados = 0
    n = len(procesos)
    while procesos_terminados < n:
        for cola in colas:
            procesos_disponibles = [p for p in procesos if p.tiempo_llegada <= tiempo_actual and p.tiempo_restante > 0 and p.prioridad == cola['prioridad']]
            if procesos_disponibles:
                if cola['algoritmo'] == round_robin:
                    proceso_actual = cola['algoritmo'](procesos_disponibles, cola['quantum'])
                else:
                    proceso_actual = cola['algoritmo'](procesos_disponibles)
                tiempo_actual += proceso_actual.tiempo_ejecucion
                proceso_actual.tiempo_restante = 0
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.tiempo_ejecucion
                procesos_terminados += 1
                break
        else:
            tiempo_actual += 1
    return procesos

def ejecutar_algoritmo(algoritmo, procesos, quantum=None, colas=None):
    if algoritmo == 'fcfs':
        return fcfs(procesos)
    elif algoritmo == 'sjf':
        return sjf(procesos)
    elif algoritmo == 'round_robin':
        return round_robin(procesos, quantum)
    elif algoritmo == 'psjf':
        return psjf(procesos)
    elif algoritmo == 'mlq':
        return mlq(procesos, colas)
    else:
        raise ValueError("Algoritmo no reconocido")

# Ejemplo de uso
procesos = [
    Proceso(1, 0, 4, 1),
    Proceso(2, 1, 3, 2),
    Proceso(3, 2, 1, 1),
    Proceso(4, 3, 2, 2)
]

algoritmo = 'mlq'  # Cambiar a 'fcfs', 'sjf', 'round_robin', 'psjf' o 'mlq'
quantum = 2  # Solo para round_robin
colas = [
    {'prioridad': 1, 'algoritmo': fcfs},
    {'prioridad': 2, 'algoritmo': sjf},
    {'prioridad': 3, 'algoritmo': round_robin, 'quantum': quantum},
    {'prioridad': 4, 'algoritmo': psjf}
]  # Solo para mlq

procesos_resultado = ejecutar_algoritmo(algoritmo, procesos, quantum, colas)

print("ID\tLlegada\tEjecución\tEspera\tFinalización\tRetorno")
for proceso in procesos_resultado:
    print(f"{proceso.id}\t{proceso.tiempo_llegada}\t\t{proceso.tiempo_ejecucion}\t\t\t{proceso.tiempo_espera}\t\t{proceso.tiempo_finalizacion}\t\t\t\t{proceso.tiempo_retorno}")