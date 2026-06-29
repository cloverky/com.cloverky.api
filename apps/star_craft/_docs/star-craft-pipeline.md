# star_craft 허브 파이프라인 전략

## 1. 역할 정의

`star_craft`는 스타 토폴로지의 **허브**다.  
스포크(`fridge`, `titanic`, `secom` 등)는 허브를 통해서만 Graph DB · Vector DB에 접근한다.  
스포크 간 직접 DB 연결은 금지한다.

```
spoke → star_craft (Hub) → Graph DB (Neo4j)
                         → Vector DB (Qdrant)
```

---

## 2. DB 선택

| 역할 | 기술 | 포트 | 용도 |
|------|------|------|------|
| **Graph DB** | Neo4j 5.x | 7474 (HTTP) / 7687 (Bolt) | 식재료 온톨로지, 레시피 관계 그래프, 스포크 간 연관 맵 |
| **Vector DB** | Qdrant | 6333 (REST) / 6334 (gRPC) | 식재료 임베딩, 레시피 시맨틱 검색, RAG 컨텍스트 |

### 선택 근거

- **Neo4j**: 식재료↔레시피↔카테고리 관계를 Cypher로 자연스럽게 표현. Community Edition 무료.
- **Qdrant**: Rust 기반 경량 벡터 DB. REST/gRPC 모두 지원. 로컬 Docker에서 안정적.

---

## 3. Docker Compose 추가 계획

`docker-compose.yaml`에 아래 두 서비스를 추가한다.

```yaml
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"   # Browser UI
      - "7687:7687"   # Bolt (드라이버 연결)
    environment:
      - NEO4J_AUTH=neo4j/cloverky_graph
      - NEO4J_PLUGINS=["apoc"]
    volumes:
      - neo4j_data:/data
    restart: always

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    restart: always

volumes:
  neo4j_data:
  qdrant_data:
```

`.env`에 추가할 변수:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=cloverky_graph
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

---

## 4. star_craft 앱 구조 (헥사고날)

```
star_craft/
├── adapter/
│   ├── inbound/
│   │   └── api/
│   │       └── v1/
│   │           └── hub_router.py
│   └── outbound/
│       ├── graph/
│       │   └── neo4j_graph_repository.py
│       └── vector/
│           └── qdrant_vector_repository.py
├── app/
│   ├── dtos/
│   │   ├── graph_dto.py
│   │   └── vector_dto.py
│   ├── ports/
│   │   ├── input/
│   │   │   └── hub_use_case.py
│   │   └── output/
│   │       ├── graph_repository.py
│   │       └── vector_repository.py
│   └── use_cases/
│       └── hub_interactor.py
├── dependencies/
│   └── hub.py
└── _docs/
    └── star-craft-pipeline.md
```

---

## 5. 포트 설계

### 5-1. GraphRepository (ABC)

```python
class GraphRepository(ABC):
    async def upsert_node(self, label: str, props: dict) -> str: ...
    async def upsert_relation(self, from_id: str, to_id: str, rel_type: str) -> None: ...
    async def query(self, cypher: str, params: dict) -> list[dict]: ...
```

### 5-2. VectorRepository (ABC)

```python
class VectorRepository(ABC):
    async def upsert(self, collection: str, id: str, vector: list[float], payload: dict) -> None: ...
    async def search(self, collection: str, vector: list[float], top_k: int) -> list[VectorHit]: ...
    async def delete(self, collection: str, id: str) -> None: ...
```

### 5-3. HubUseCase (ABC)

```python
class HubUseCase(ABC):
    # 스포크가 식재료·레시피 관계를 허브에 위임
    async def register_ingredient_relation(self, cmd: RelationCommand) -> None: ...
    # 임박 재료 기반 레시피 후보 조회
    async def search_recipes(self, cmd: SearchCommand) -> list[RecipeResult]: ...
```

---

## 6. 파이프라인 흐름

### 6-1. 스포크 → 허브: 온톨로지 등록

```
fridge (spoke)
  └─ InventoryInteractor
       └─ HubUseCase.register_ingredient_relation()
            └─ HubInteractor
                 ├─ GraphRepository.upsert_node()   → Neo4j
                 └─ VectorRepository.upsert()       → Qdrant
```

### 6-2. 허브 → 스포크: 레시피 추천

```
Client
  └─ hub_router (inbound)
       └─ HubUseCase.search_recipes()
            └─ HubInteractor
                 ├─ VectorRepository.search()   → Qdrant (시맨틱)
                 └─ GraphRepository.query()     → Neo4j  (관계 필터)
```

### 6-3. Exaone 오케스트레이터 연동

임박 재료 → Exaone 프롬프트 → 응답 파싱 → 임베딩 → Qdrant 검색

```
FakerOrchestrator.achat()          (core.lol)
  └─ "냉장고 재료: [당근, 두부] → 레시피 제안" 프롬프트
       └─ 응답 파싱 → embedding → VectorRepository.search()
```

---

## 7. 컬렉션 · 레이블 규칙

### Neo4j 노드 레이블

| 레이블 | 주요 속성 |
|--------|-----------|
| `Ingredient` | `name`, `category`, `shelf_life_days` |
| `Recipe` | `name`, `difficulty`, `cook_time_min` |
| `Category` | `name` |

### Neo4j 관계 타입

| 관계 | 방향 |
|------|------|
| `CONTAINS` | Recipe → Ingredient |
| `BELONGS_TO` | Ingredient → Category |

### Qdrant 컬렉션

| 컬렉션 | 벡터 dim | 용도 |
|--------|----------|------|
| `recipes` | 768 | 레시피 텍스트 임베딩 |
| `ingredients` | 768 | 식재료 시맨틱 검색 |

임베딩 모델: Gemini `text-embedding-004` (기존 Keymaker 패턴 재사용)

---

## 8. 구현 순서

1. `docker-compose.yaml` — Neo4j · Qdrant 서비스 + volumes 추가
2. `clover/.env` — 연결 변수 추가
3. `star_craft/app/ports/output/` — `GraphRepository` · `VectorRepository` ABC
4. `star_craft/app/ports/input/` — `HubUseCase` ABC
5. `star_craft/app/dtos/` — `graph_dto.py` · `vector_dto.py`
6. `star_craft/adapter/outbound/graph/` — Neo4j 어댑터 (`neo4j` 드라이버)
7. `star_craft/adapter/outbound/vector/` — Qdrant 어댑터 (`qdrant-client`)
8. `star_craft/app/use_cases/hub_interactor.py`
9. `star_craft/dependencies/hub.py` — DI 팩토리
10. `star_craft/adapter/inbound/api/v1/hub_router.py`
11. `main.py` — `include_router(hub_router)`

---

## 9. 의존성 추가 (`requirements.txt`)

```
neo4j>=5.0.0
qdrant-client>=1.9.0
```
