# 📦 Requisitos do Projeto LabInventory

O **LabInventory** é um sistema de gerenciamento de materiais do laboratório **NAVIR**, desenvolvido com **Django**, que permite o controle de usuários, materiais e empréstimos de forma prática.

---

## ✅ Requisitos Funcionais

### RF01 – Cadastro de Usuários
- O sistema deve permitir o cadastro de usuários com os seguintes campos:
    - Nome
    - E-mail
    - Matrícula (ou ID institucional)
    - Tipo de usuário (aluno, professor, técnico, etc)
- Os usuários devem se autenticar com login e senha.
- Deve existir diferenciação entre usuários comuns e administradores.

### RF02 – Cadastro de Materiais
- Permitir o registro de materiais com os seguintes dados:
    - Nome do material
    - Descrição
    - Quantidade total
    - Localização (ex: armário, prateleira)
    - Categoria (ex: componente eletrônico, ferramenta, etc)

### RF03 – Empréstimo de Materiais
- Usuários autenticados podem solicitar o empréstimo de materiais.
- O sistema deve registrar:
    - Materiais retirados
    - Data do empréstimo
    - Nome do responsável (usuário)
    - Data prevista para devolução
- A quantidade disponível deve ser atualizada automaticamente.

### RF04 – Devolução de Materiais
- O sistema deve permitir registrar a devolução dos materiais.
- Deve atualizar a quantidade disponível.
- Deve registrar:
    - Quem devolveu
    - Data da devolução
    - Se houve atraso

### RF05 – Histórico de Empréstimos
- O sistema deve apresentar um histórico completo dos empréstimos e devoluções.
- Permitir filtros por:
    - Nome do usuário
    - Nome do material
    - Período de empréstimo
    - Status (devolvido ou não)

---

## ❌ Requisitos Não Funcionais

### RNF01 – Interface Web
- Interface responsiva e amigável.
- Desenvolvida com Django + Bootstrap ou outro framework CSS.

### RNF02 – Segurança
- Autenticação obrigatória para empréstimos/devoluções.
- Controle de permissões entre usuários comuns e administradores.
- Proteção de dados sensíveis dos usuários.

### RNF03 – Escalabilidade
- Código modular para facilitar manutenção e expansão.
- Preparado para futuras funcionalidades como:
    - Notificações por e-mail
    - Geração de relatórios em PDF
    - Alerta de devoluções atrasadas

---

## 🛠️ Tecnologias Utilizadas
- Python
- Django
- SQLite
- Bootstrap (frontend)
- MkDocs (documentação)

---

> Desenvolvido por Vinicius Melchior para o laboratório NAVIR.
