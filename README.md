# Simulador de Viagens

API em Python/Django para simular viagens de carro no Brasil, calculando rota, distância, tempo estimado, consumo de combustível e custo total com base em dados reais de geolocalização e roteamento.

## Visão geral

Este projeto usa:

- Django 5
- Django REST Framework
- PostgreSQL
- Docker e Docker Compose
- OpenStreetMap Nominatim para geocodificação
- OSRM (Open Source Routing Machine) para cálculo de rota por estrada

A aplicação permite criar simulações de viagem entre duas cidades ou endereços, selecionar um veículo do catálogo, aplicar preço do combustível e obter um resultado com:

- distância total
- duração estimada
- consumo em litros
- custo do combustível
- custo de pedágios
- custo total
- geometria da rota em GeoJSON

## Funcionalidades

- busca geográfica por endereço no Brasil
- cálculo de rota real por estradas
- suporte a veículos com tipos de combustível e consumo
- catálogo de pedágios
- criação de simulações de viagem via API REST
- persistência das simulações em banco de dados

## Estrutura do projeto

- `config/` — configurações do projeto Django
- `trips/` — app principal com modelos, serializers, serviços e endpoints
- `manage.py` — entry point do Django
- `docker-compose.yml` — ambiente com PostgreSQL e aplicação
- `.env.example` — variáveis de ambiente de exemplo
- `requirements.txt` — dependências do projeto

## Requisitos

- Python 3.12+
- pip
- PostgreSQL
- Docker e Docker Compose (opcional, para rodar o ambiente completo)

## Configuração do ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/Dagmar87/simulador-viagens.git
   cd simulador-viagens
   ```

2. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   No Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Copie o arquivo de exemplo de variáveis de ambiente:

   ```bash
   copy .env.example .env
   ```

   ou em Linux/macOS:

   ```bash
   cp .env.example .env
   ```

5. Ajuste os valores do arquivo `.env` conforme seu ambiente:

   Para execução local com PostgreSQL instalado na máquina:

   ```env
   DEBUG=True
   SECRET_KEY=sua-chave-secreta
   DB_NAME=simulador_viagens
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   NOMINATIM_URL=https://nominatim.openstreetmap.org/search
   OSRM_URL=https://router.project-osrm.org
   ```

   Para execução com Docker Compose, use:

   ```env
   DEBUG=True
   SECRET_KEY=sua-chave-secreta
   DB_NAME=simulador_viagens
   DB_USER=simulador
   DB_PASSWORD=simulador_password
   DB_HOST=db
   DB_PORT=5432
   NOMINATIM_URL=https://nominatim.openstreetmap.org/search
   OSRM_URL=https://router.project-osrm.org
   ```

## Executando localmente

### Sem Docker

1. Crie o banco de dados PostgreSQL:

   ```sql
   CREATE DATABASE simulador_viagens;
   ```

2. Aplique as migrações:

   ```bash
   python manage.py migrate
   ```

3. Execute a aplicação:

   ```bash
   python manage.py runserver
   ```

A API ficará disponível em:

- http://localhost:8000/api/

### Com Docker

1. Suba os serviços:

   ```bash
   docker-compose up --build
   ```

2. A aplicação estará disponível em:

   - API: http://localhost:8000/api/
   - PostgreSQL: localhost:5432

## Endpoints

### Veículos

- `GET /api/vehicles/` — lista veículos
- `POST /api/vehicles/` — cria veículo
- `GET /api/vehicles/<id>/` — detalhes do veículo
- `PUT /api/vehicles/<id>/` — atualiza veículo
- `DELETE /api/vehicles/<id>/` — remove veículo

### Pedágios

- `GET /api/tolls/` — lista pedágios
- `POST /api/tolls/` — cria pedágio
- `GET /api/tolls/<id>/` — detalhes do pedágio
- `PUT /api/tolls/<id>/` — atualiza pedágio
- `DELETE /api/tolls/<id>/` — remove pedágio

### Simulações

- `GET /api/simulations/` — lista simulações
- `POST /api/simulations/` — cria nova simulação
- `GET /api/simulations/<id>/` — detalhes da simulação
- `PUT /api/simulations/<id>/` — atualiza simulação
- `DELETE /api/simulations/<id>/` — remove simulação

## Exemplo de criação de simulação

```bash
curl -X POST http://localhost:8000/api/simulations/ \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "São Paulo, SP",
    "destination": "Campinas, SP",
    "vehicle_id": 1,
    "fuel_price": 5.89,
    "average_speed_kmh": 80,
    "round_trip": false
  }'
```

Resposta esperada:

```json
{
  "id": 1,
  "origin": "São Paulo, SP",
  "destination": "Campinas, SP",
  "fuel_price": "5.89",
  "average_speed_kmh": "80.00",
  "round_trip": false,
  "distance_km": "100.20",
  "duration_minutes": "75.15",
  "fuel_liters": "7.35",
  "fuel_cost": "43.30",
  "toll_cost": "0.00",
  "total_cost": "43.30",
  "route_geometry": {},
  "created_at": "2026-10-08T00:00:00Z"
}
```

## Observações

- O cálculo usa o endereço informado para localizar as coordenadas geográficas.
- A rota é calculada com o serviço OSRM, que considera a rede viária real.
- O projeto foi pensado para uso em ambiente de desenvolvimento com uma base de dados PostgreSQL local ou em container.
- Para produção, recomenda-se configurar `DEBUG=False`, segurança do Django, uso de segredo forte e ambiente com banco e serviços dedicados.

## Contribuição

Pull requests e melhorias são bem-vindas. Para contribuir:

1. crie uma branch para a mudança
2. implemente a melhoria ou correção
3. teste a funcionalidade localmente
4. abra um PR descrevendo a alteração

## Licença

Este projeto está em desenvolvimento e não possui licença definida ainda.
