# 🍕 Pizzaria - Gerenciador de Pedidos (MVP)

MVP acadêmico para a disciplina de Arquitetura de Software.

## Stack
- Python 3.11+
- Flask
- SQLite
- HTML/CSS/JavaScript

## Arquitetura
MVC + camadas: Controller → Service → Repository → Database.

## Design Patterns
1. Strategy: cálculo da taxa de entrega.
2. Factory Method: criação de pedidos Delivery e Retirada.
3. Observer: registro do histórico de alterações de status.

## Funcionalidades
- Produtos iniciais de exemplo.
- Criação de pedidos delivery ou retirada.
- Cálculo automático de subtotal, taxa e total.
- Alteração de status.
- Registro de histórico de status.
- Marcação de pagamento.
- API REST e interface web.

## Executar no Windows
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py run.py
```
Abra http://127.0.0.1:5000
