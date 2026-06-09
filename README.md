Sistema de Auxílio ao Pouso Terrestre (Missão Lua)
Integrantes

Equipe: [Nome da Equipe]

Nome	RM
Integrante 1	RMXXXXX
Integrante 2	RMXXXXX
Integrante 3	RMXXXXX
Resumo do Problema

As missões espaciais dependem de sistemas inteligentes capazes de monitorar continuamente as condições operacionais da nave e auxiliar na tomada de decisões críticas.

Este projeto simula um sistema de monitoramento de uma cápsula em processo de reentrada terrestre após uma missão lunar. O sistema recebe dados de telemetria, interpreta as condições da nave, detecta situações de risco, gera alertas automáticos e fornece recomendações para aumentar as chances de um pouso seguro.

Além disso, o sistema realiza uma análise simples de tendência térmica para auxiliar nas decisões durante a fase de reentrada.

Estruturas de Dados Utilizadas
Lista

Utilizada para armazenar dados temporários e para implementação da fila de alertas e da pilha de eventos críticos.

Exemplo:

fila_alertas = []
pilha_critica = []
Matriz (Lista de Listas)

Utilizada para armazenar todas as leituras da telemetria recebidas.

Exemplo:

matriz_leituras = []

Cada linha contém:

Horário
Ângulo de reentrada
Energia da bateria
Força G
Temperatura do escudo térmico
Estado dos módulos
Evento registrado
Dicionário

Utilizado para armazenar o estado dos módulos críticos da nave.

Exemplo:

dicionario_modulos = {}

Os módulos monitorados são:

Suporte à Vida
Energia
Comunicação
Habitat
Laboratório
Armazenamento
Fila

A fila é utilizada para registrar alertas detectados durante a análise da missão.

Exemplo:

fila_alertas.append(alerta)
Pilha

A pilha registra os últimos eventos críticos identificados pelo sistema.

Exemplo:

pilha_critica.append(evento)
Regras Lógicas do Diagnóstico

O sistema utiliza estruturas IF, ELIF e ELSE para classificar a situação da missão.

Principais operadores utilizados:

AND
OR
NOT

Expressão booleana principal:

(angulo > -5.5 or angulo < -7.5) or
(temperatura > 1500) or
(forca_g > 6.5 and bateria < 25)
Critérios utilizados
Alerta Crítico de Trajetória

Gerado quando:

angulo > -5.5 or angulo < -7.5
Alerta Crítico de Integridade

Gerado quando:

temperatura > 1500

ou

forca_g > 6.5 and bateria < 25
Status Nominal

Gerado quando:

angulo dentro da faixa segura
e bateria acima de 20%
Inconsistência Proposital

O sistema identifica situações inconsistentes nos dados.

Exemplo:

bateria < 20%
e todos os módulos ativos

Essa condição representa um conflito lógico proposital utilizado para validar a capacidade de diagnóstico do sistema.

Técnica de Previsão Utilizada

Foi utilizada uma análise simples baseada na média das três últimas temperaturas registradas pelo escudo térmico.

Exemplo:

media_temperatura_recente =
planilha['temperatura_escudo'].tail(3).mean()

Essa média é utilizada para indicar a tendência térmica da cápsula durante a reentrada.

A previsão influencia diretamente o diagnóstico e as recomendações apresentadas ao operador da missão.

Como Executar

Instale as dependências:

pip install -r requirements.txt

Execute o programa:

python main.py

Escolha uma das opções:

1 → JSON
2 → CSV
3 → TXT
4 → Dados de Teste
Exemplo de Entrada

O sistema espera os seguintes campos:

angulo_reentrada
energia_bateria
forca_g
temperatura_escudo
modulos_binarios
log_evento
Exemplo de Saída




[INSERIR PRINT DA EXECUÇÃO AQUI]




Recomendações Geradas pelo Sistema

Dependendo das condições detectadas, o sistema pode gerar recomendações como:

Trajetória Crítica
Acionar propulsores de manobra.
Corrigir o ângulo de reentrada.
Integridade Crítica
Redirecionar energia para sistemas essenciais.
Desativar módulos não prioritários.
Inconsistência Detectada
Bloquear barramento físico.
Solicitar revisão dos dados de telemetria.
Status Nominal
Preparar sequência de pouso.
Preservar energia para a fase final da missão.


Arquivos do Projeto
├── main.py
├── requirements.txt
├── data.json
├── README.md
├── docs
│   ├── relatorio.pdf
│   ├── link_video.txt
│   └── uso_ia.md


Vídeo de Apresentação

Link do vídeo:

COLE_AQUI_O_LINK_DO_YOUTUBE
Conclusões e Aprendizados

O desenvolvimento deste projeto permitiu aplicar conceitos estudados nas três primeiras fases do curso, incluindo estruturas de dados, lógica de programação, análise de dados e tomada de decisão automatizada.

O sistema demonstrou como informações de telemetria podem ser utilizadas para monitorar condições críticas durante uma missão espacial e auxiliar operadores na identificação de riscos e na definição de ações corretivas.

Além dos aspectos técnicos, o projeto reforçou a importância da organização dos dados, da validação das informações recebidas e da construção de diagnósticos confiáveis para sistemas de missão crítica.