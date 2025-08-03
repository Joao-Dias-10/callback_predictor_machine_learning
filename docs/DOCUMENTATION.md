# Documento Técnico - Callback Predictor (Machine Learning)

## 1. Visão Geral

O projeto **Callback Predictor** tem como objetivo prever, com base em dados históricos de atendimento, quais clientes possuem maior probabilidade de realizar uma **rechamada dentro de 72 horas**. Essa previsão auxilia equipes de atendimento na priorização de contatos e melhoria de processos.

---

## 2. Componentes Principais

### 2.1. Preditor (`RechamadaPredictor`)
- Utiliza `RandomForestClassifier` do `scikit-learn`
- Treinamento com features como: `tempo_atendimento`, `qtd_contatos`, `tipo_solicitacao`
- Saída: lista de clientes com alta probabilidade de rechamada (`num_cliente`)

### 2.2. Banco de Dados (`ChamadaDB`)
- Conecta via SQLAlchemy ORM
- Modelos: `Chamada`, `CallbackScore72h`
- Métodos:
  - `get_call_history()`: retorna chamadas dos últimos 12 meses
  - `insert_callback_score(df, dia)`: insere previsão do dia

### 2.3. Manipulação de Arquivos (`FileOrchestration`)
- Leitura e escrita de CSVs com pandas
- Suporta tanto `DataFrames` quanto listas de objetos (ORM)

### 2.4. Logger
- Configuração centralizada via `LoggerConfig`
- Gera logs em arquivo e console com nível configurável (`INFO`, `DEBUG`, etc.)

---

## 3. Pipeline Operacional

1. **Carregamento de histórico** (via ORM ou CSV)
2. **Treinamento do modelo**
3. **Aplicação do modelo sobre dados do dia**
4. **Exportação dos resultados**
5. **Persistência em banco**

---

## 4. Testes

- Testes unitários com `pytest`
- Cobertura:
  - Geração e leitura de CSV
  - Logger configurável
  - Inserção e leitura do banco
  - Precisão do modelo preditivo

---

## 5. Requisitos

- Python 3.10+
- Pandas, Scikit-learn, SQLAlchemy
- Banco compatível com SQLAlchemy (ostgreSQL)

---

## 6. Considerações Finais

O projeto está modularizado e pronto para:
- Integração com pipelines de ETL
- Deploy em sistemas batch/diários
- Evolução para modelos mais robustos (ex: XGBoost)

