# 📞 Previsão de Rechamada em 72h – Documentação Técnica

## 🧠 Objetivo
Identificar automaticamente clientes que têm alta probabilidade de **realizar uma nova chamada dentro de 72h**, após um atendimento.

Executado de forma automatizada **3x por dia** via job agendado.

---

## 🔁 Visão Geral do Processo

1. Coleta dados do atendimento do dia atual (`eventos.csv` ou base online)
2. Filtra apenas atendimentos válidos (ignora rechamadas anteriores)
3. Extrai features com base no histórico do cliente
4. Usa modelo de Machine Learning (árvore de decisão) para previsão
5. Grava previsões no banco `postgresql.db.chamada_prevista_72h`

---

## 🗂️ Estrutura Esperada dos Dados de Entrada

**eventos.csv**
| Coluna              | Tipo       | Descrição                            |
|---------------------|------------|----------------------------------------|
| cliente_id          | string     | Identificador único do cliente         |
| data_hora_evento    | datetime   | Data e hora do atendimento             |
| tipo_evento         | string     | 'atendimento', 'rechamada', etc.       |
| tempo_espera        | int        | Tempo de espera (minutos)              |
| problema_resolvido  | 0 ou 1     | Se o problema foi resolvido ou não     |
| tipo_reclamacao     | 0, 1, 2    | Nível da reclamação (0=simple, 2=grave)|
| atendente_novo      | 0 ou 1     | Se o atendente era novo                |

---

## ⚙️ Parâmetros

- Janela de previsão: **72h**
- Frequência de execução: **3x ao dia**
- Excluir clientes que já fizeram rechamada

---

## 🧪 Outputs

Tabela: `chamada_prevista_72h`

| Coluna              | Tipo       | Descrição                               |
|---------------------|------------|-------------------------------------------|
| cliente_id          | string     | ID do cliente                             |
| probabilidade       | float      | Probabilidade de rechamada em 72h         |
| data_referencia     | date       | Data da previsão                          |
| timestamp_execucao  | timestamp  | Quando a previsão foi gerada              |

---

## 👨‍🔧 Como executar localmente

```bash
python pipeline_runner.py --data eventos.csv
````

---

## 🛡️ Observações

* Se o cliente **já tiver feito uma rechamada**, ele é **excluído de novas previsões**
* Dados devem cobrir **pelo menos 6 a 12 meses** para treinar o modelo com confiança

```
