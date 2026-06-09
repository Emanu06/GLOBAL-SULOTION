import pandas as pd

CAMPOS_OBRIGATORIOS = ['angulo_reentrada', 'energia_bateria', 'forca_g', 'temperatura_escudo', 'modulos_binarios', 'log_evento']
NOMES_MODULOS = ["SUPORTE_VIDA", "ENERGIA", "COMUNICACAO", "HABITAT", "LABORATORIO", "ARMAZENAMENTO"]

def main():
    print("  SISTEMA DE AUXÍLIO AO POUSO TERRESTRE (MISSÃO LUA) ")
    
    opcao = input("Digite 1 para JSON, 2 para CSV, 3 para TXT ou 4 para Dados de Teste: ").strip()

    planilha = None

    if opcao in ["1", "2", "3"]:
        caminho_arquivo = input("Digite o caminho do arquivo com a extensão: ").strip()
        planilha = reconhecer_planilha(caminho_arquivo)
    elif opcao == "4":
        planilha = gerar_dados_teste()
    else:
        print("[ERRO] Opção inválida.")
        return

    if planilha is None:
        print("[ESTADO CRÍTICO] Falha catastrófica: Arquivo corrompido ou formato ilegível.")
        return

    if not validar_campos_telemetria(planilha):
        print("[ESTADO CRÍTICO] Abortar análise. Dados de telemetria incompletos para o pouso.")
        return

    calcular_condicoes_pouso(planilha)


def reconhecer_planilha(caminho_arquivo):
    try:
        extensao = caminho_arquivo.lower()
        if extensao.endswith('.csv'):
            return pd.read_csv(caminho_arquivo)
        elif extensao.endswith('.json'):
            return pd.read_json(caminho_arquivo)
        elif extensao.endswith('.txt'):
            return pd.read_csv(caminho_arquivo, sep='\t')
        else:
            return pd.read_excel(caminho_arquivo)
    except Exception as e:
        print(f"[ERRO DE FORMATO] Não foi possível ler o arquivo. Detalhes: {e}")
        return None


def validar_campos_telemetria(planilha):
    colunas_arquivo = planilha.columns.tolist()
    campos_faltantes = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in colunas_arquivo]
    
    if campos_faltantes:
        print(f"[ERRO DE VALIDAÇÃO] Estão faltando os seguintes dados essenciais: {campos_faltantes}")
        return False
    
    print("[SUCESSO] Todos os campos de telemetria necessários foram validados!")
    return True


def calcular_condicoes_pouso(planilha):
    print("RELATÓRIO DE CÁLCULO DE REENTRADA")
    
    matriz_leituras = []
    for idx, row in planilha.iterrows():
        linha = [row['horario'], row['angulo_reentrada'], row['energia_bateria'], row['forca_g'], row['temperatura_escudo'], row['modulos_binarios'], row['log_evento']]
        matriz_leituras.append(linha)
    
    fila_alertas = []
    pilha_critica = []
    
    dados_atuais = planilha.iloc[-1]
    
    angulo = dados_atuais['angulo_reentrada']
    bateria = dados_atuais['energia_bateria']
    forca_g = dados_atuais['forca_g']
    temperatura = dados_atuais['temperatura_escudo']
    byte_modulos = int(dados_atuais['modulos_binarios'])
    log_evento = dados_atuais['log_evento']
    
    dicionario_modulos = {}
    for i, nome in enumerate(NOMES_MODULOS):
        status = (byte_modulos >> i) & 1
        dicionario_modulos[nome] = "OPERACIONAL" if status == 1 else "CRÍTICO/DESATIVADO"

    if len(planilha) >= 3:
        media_temperatura_recente = planilha['temperatura_escudo'].tail(3).mean()
        tendencia_txt = f"{media_temperatura_recente:.1f}°C (Estável)" if media_temperatura_recente <= temperatura else f"{media_temperatura_recente:.1f}°C (Em elevação térmica!)"
    else:
        tendencia_txt = "Dados insuficientes para calcular tendência térmica."

    print(f"-> Horário do Registro: {dados_atuais['horario']}")
    print(f"-> Último Evento do Log: {log_evento}")
    print(f"-> Ângulo de Ataque Atual: {angulo}°")
    print(f"-> Força G Detectada: {forca_g} G")
    print(f"-> Temperatura do Escudo Térmico: {temperatura}°C")
    print(f"-> Média Térmica Recente (Previsão): {tendencia_txt}")
    print(f"-> Reserva de Energia das Baterias: {bateria}%")
    print("-" * 50)
    print("STATUS INDIVIDUAL DOS MÓDULOS CRÍTICOS:")
    for modulo, status in dicionario_modulos.items():
        print(f"   [{modulo}]: {status}")
    print("-" * 50)

    if bateria < 20.0 and byte_modulos == 63:
        fila_alertas.append("ALERTA: Falha Crítica de Inconsistência de Hardware")
        pilha_critica.append("CONFLITO_LOGICO_ENERGIA_X_MODULOS")
        print("[DIAGNÓSTICO]: INCONSISTÊNCIA PROPOSITAL DETECTADA")
        print("RECOMENDAÇÃO: Bloquear barramento físico imediato. Bateria em colapso mas registros indicam carga total ligada.")
        return

    if angulo > -5.5 or angulo < -7.5:
        fila_alertas.append("ALERTA: Erro Crítico de Trajetória")
        pilha_critica.append("ABORT_PATH_ERROR")
        print("[DIAGNÓSTICO]: ALERTA CRÍTICO DE TRAJETÓRIA")
        if angulo > -5.5:
            print("RECOMENDAÇÃO: Acionar propulsores de manobra (RCS) para inclinar o nariz para BAIXO.")
            print("Risco: A nave pode ricochetear na atmosfera e se perder no espaço profundo.")
        else:
            print("RECOMENDAÇÃO: Acionar propulsores de manobra (RCS) para inclinar o nariz para CIMA.")
            print("Risco: Ângulo muito acentuado. Desaceleração extrema e destruição térmica iminente.")
            
    elif temperatura > 1500 or (forca_g > 6.5 and bateria < 25.0):
        fila_alertas.append("ALERTA: Falha Estrutural Térmica")
        pilha_critica.append("ABORT_THERMAL_FAIL")
        print("[DIAGNÓSTICO]: ALERTA CRÍTICO DE INTEGRIDADE DA CÁPSULA")
        print("RECOMENDAÇÃO: Ejetar módulos de serviço não utilizados. Direcionar 100% da energia restante para os geradores de campo magnético defletor e suporte à vida.")
        
    elif (angulo <= -5.5 and angulo >= -7.5) and not (bateria < 20.0):
        print("[DIAGNÓSTICO]: STATUS NOMINAL (SEGURO)")
        print("RECOMENDAÇÃO: Condições ótimas de pouso. Liberar travas dos paraquedas primários em 10 segundos. Desligar computadores secundários para preservar as baterias até o impacto na água.")
        
    else:
        print("[DIAGNÓSTICO]: STATUS EM ATENÇÃO")
        print("RECOMENDAÇÃO: Monitorar telemetria. Pequenas oscilações detectadas, mas dentro da margem de sobrevivência.")


def gerar_dados_teste():
    print("\n[INFO] Simulando recepção de telemetria de órbita lunar...")

    dados = pd.DataFrame({
        'horario': ['21:00', '21:10', '21:20', '21:30', '21:40', '21:50', '22:00', '22:10'],
        'angulo_reentrada': [-6.2, -6.1, -6.0, -5.2, -6.5, -6.5, -6.5, -6.5],       
        'energia_bateria': [90, 85, 80, 78, 70, 65, 55, 15],
        'forca_g': [1.0, 2.3, 4.1, 5.8, 4.5, 4.8, 5.0, 5.2],
        'temperatura_escudo': [120, 580, 1100, 1350, 1200, 1250, 1280, 1310],
        'modulos_binarios': [63, 63, 63, 61, 61, 57, 57, 63],
        'log_evento': [
            'INICIALIZACAO_SISTEMA',
            'CAPTURA_DE_CORREDOR',
            'INICIO_FRENAGEM',
            'QUEDA_MODULO_LABORATORIO',
            'ESTABILIZACAO_TERMICA',
            'DESCONEXAO_MODULO_ARMAZENAMENTO',
            'MODO_ECONOMIA_ATIVADO',
            'ANOMALIA_DE_TENSAO_DETECTADA'
        ]
    })
    return dados


if __name__ == '__main__':
    main()