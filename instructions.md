# Compartilhamento de Banco de Dados entre Sistema de Gestão de Estoque e Sistema de Gerenciamento de Pedidos

## Cenário

Um banco opera um **Sistema de Gerenciamento de Contas** e um **Sistema de Processamento de Transações**, ambos precisando acessar e atualizar informações de clientes e contas em um banco de dados central. O objetivo é garantir que as informações das contas estejam sempre atualizadas em tempo real em ambos os sistemas, evitando inconsistências e melhorando a eficiência operacional. Para facilitar essa integração, será utilizado o **DuckDB** como banco de dados central compartilhado entre os sistemas.

## Requisitos

### Banco de Dados Centralizado com DuckDB:

- Projete uma solução de reuso que permita que o **Sistema de Gerenciamento de Contas** e o **Sistema de Processamento de Transações** atualizem e acessem informações de contas em tempo real no banco de dados central utilizando o **DuckDB**.

- Utilize o **DuckDB** como banco de dados embutido para facilitar a comunicação e compartilhamento de dados entre os sistemas.

### Gestão de Contas:

- Modele uma estrutura em que o **Sistema de Gerenciamento de Contas** possa adicionar, modificar e remover informações de clientes e contas no banco de dados central.

- Garanta que essas alterações sejam refletidas imediatamente no **Sistema de Processamento de Transações**.

### Processamento de Transações:

- Modele para que o Sistema de **Processamento de Transações** possa acessar informações atualizadas de contas durante a realização de **depósitos, saques e transferências**.

- Assegure-se de que as transações sejam registradas e que os saldos das contas sejam atualizados em **tempo real**.

## Tarefa

### Modelagem de Banco de Dados

- Criar modelos de banco de dados que representem as entidades e relacionamentos necessários para o compartilhamento eficiente de dados entre o Sistema de Gerenciamento de Contas e o Sistema de Processamento de Transações.

- O modelo deve incluir entidades como **Clientes, Contas, Transações** e os relacionamentos entre elas.

### Desenvolvimento Utilizando DuckDB
- **Implementação do Banco de Dados Central:**
    - Utilize o DuckDB para criar o banco de dados central que será compartilhado entre os sistemas.

    - Defina as tabelas e os relacionamentos conforme o modelo de dados projetado.

- **Integração dos Sistemas com o DuckDB:**
    - Desenvolva os módulos necessários em cada sistema (Gerenciamento de Contas e Processamento de Transações) para conectar-se ao banco de dados DuckDB.

    - Implemente as operações de **inserção, atualização, remoção e consulta de dados** no banco de dados.

- **Atualização em Tempo Real:**

    - **Modele** como as atualizações em tempo real são refletidas no banco de dados compartilhado e como essas mudanças são propagadas entre os sistemas utilizando o DuckDB.

    - Assegure-se de que ambos os sistemas acessem o mesmo banco de dados DuckDB e que as operações sejam **atômicas** para evitar inconsistências.

## Critérios de Avaliação

### Modelagem de Banco de Dados (100XP)
- Projetar um modelo de banco de dados que atenda às necessidades tanto do Sistema de Gerenciamento de Contas quanto do Sistema de Processamento de Transações.

- O modelo deve ser normalizado e seguir as melhores práticas de design de banco de dados.

- Deve facilitar o acesso eficiente aos dados e suportar as operações requeridas pelos sistemas.

### Atualização em Tempo Real (100XP)

- Demonstrar como as atualizações em tempo real são refletidas no banco de dados compartilhado.

- Garantir que não haja inconsistências ou conflitos de dados durante as operações simultâneas dos sistemas.

- Implementar mecanismos de controle de concorrência, se necessário, para assegurar a integridade dos dados.

### Desenvolvimento com DuckDB (300XP)
    
- Os sistemas devem ser capazes de se conectar ao banco de dados DuckDB e realizar as operações necessárias.

- O código deve seguir boas práticas de programação e estar bem documentado.

- Deve-se garantir que as operações de leitura e escrita no banco de dados sejam eficientes e seguras.


