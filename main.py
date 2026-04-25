from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. CONFIGURAÇÃO DO BANCO DE DADOS (SQLite)
DATABASE_URL = "sqlite:///./inventario.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. MODELAGEM: Definindo o que é um "Equipamento" no Banco de Dados
class EquipamentoDB(Base):
    __tablename__ = "equipamentos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    marca = Column(String)
    serie = Column(String)

# Cria as tabelas no arquivo .db automaticamente
Base.metadata.create_all(bind=engine)

# 3. MODELAGEM PARA O FASTAPI (O que o usuário envia)
class EquipamentoCreate(BaseModel):
    nome: str
    marca: str
    serie: str

app = FastAPI()

# --- ROTAS CRUD ---

# Rota para LISTAR tudo (Read)
@app.get("/equipamentos")
def listar_equipamentos():
    db = SessionLocal()
    itens = db.query(EquipamentoDB).all()
    db.close()
    return itens

# Rota para ADICIONAR novo (Create)
@app.post("/equipamentos")
def criar_equipamento(item: EquipamentoCreate):
    db = SessionLocal()
    novo_item = EquipamentoDB(nome=item.nome, marca=item.marca, serie=item.serie)
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    db.close()
    return {"mensagem": "Equipamento cadastrado!", "dados": novo_item}

# Rota para DELETAR (Delete)
@app.delete("/equipamentos/{item_id}")
def deletar_equipamento(item_id: int):
    db = SessionLocal()
    item = db.query(EquipamentoDB).filter(EquipamentoDB.id == item_id).first()
    if not item:
        db.close()
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    db.delete(item)
    db.commit()
    db.close()
    return {"mensagem": f"Item {item_id} deletado com sucesso!"}