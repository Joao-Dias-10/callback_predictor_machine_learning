# 🤖 callback_predictor_machine_learning

Sistema preditivo baseado em Machine Learning para antecipar a possibilidade de rechamadas (callbacks) de clientes em um call center, com foco no intervalo de 72 horas após o atendimento inicial.

---

## 🎯 Objetivo

Automatizar a identificação de clientes com **alta probabilidade de retornar uma ligação** ao call center, permitindo que a operação tome ações proativas (como contatos prévios ou priorização de casos críticos).

---

## 🧱 Arquitetura

- 📦 **Machine Learning** com modelos supervisionados (Árvore de Decisão, Random Forest, etc.)
- 🧪 **Testes automatizados** com `pytest`
- 🐘 **Persistência em PostgreSQL**, via `SQLAlchemy ORM`
- 📊 **Análise e estudo** em Jupyter Notebooks
- 🔁 **Pipeline agendado** para rodar previsões 3x por dia
- 📌 **Organização orientada a objetos (POO)**

---

## 📂 Estrutura de Diretórios

```

├── config/           # Arquivos de configuração (.yaml, .env, etc.)
├── data/             # Dados brutos e processados
│   ├── raw/
│   └── processed/
├── logs/             # Logs de execução
├── notebooks/        # Cadernos Jupyter para testes manuais e EDA
├── src/              # Código-fonte principal
│   ├── api/          # Integração com APIs externas
│   ├── automation/   # Scripts de automação e agendamento
│   ├── db/           # Lógica de banco de dados
│   │   ├── connection.py
│   │   ├── init\_db.py
│   │   ├── models.py
│   │   └── queries.py
│   ├── preprocessing/ # Pré-processamento e transformação de dados
    ├── ml/           # modelos, treinamento, previsão
│   └── utils/        # Funções utilitárias
├── tests/            # Testes unitários e de integração
├── .gitignore        # Padrões de arquivos ignorados pelo Git
├── main.py           # Ponto de entrada do projeto
├── requirements.txt          


````

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10+
- scikit-learn
- pandas
- SQLAlchemy
- psycopg2 (PostgreSQL driver)
- pytest
- Jupyter

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/callback_predictor_machine_learning.git
   cd callback_predictor_machine_learning
   ````

2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco em `config.py` ou via `.env`.

5. Rode testes:

   ```bash
   pytest
   ```

6. Execute previsões (exemplo):

   ```bash
   python main.py
   ```

---

