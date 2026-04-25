from fastapi import FastAPI

# Aqui a gente cria a "instância" do aplicativo
app = FastAPI()

# Isso é uma "Rota". Quando você acessar o endereço do servidor, 
# ele vai executar essa função abaixo.
@app.get("/")
def home():
    return {"status": "Servidor do Inventário On-line!"}

@app.get("/item/{item_id}")
def buscar_item(item_id: int):
    # Imagine que isso aqui virá de um banco de dados depois
    return {"item_id": item_id, "nome": "Teclado Mecânico", "status": "Disponível"}