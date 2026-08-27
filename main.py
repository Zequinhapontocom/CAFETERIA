from fastapi import FastAPI

app=FastAPI(title="API da Cafeteria")

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API da Cafeteria!"}

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI(title="API da Cafeteria")

@app.post("/api/produtos", response_model=schemas.ProdutosResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session=Depends(get_db)):

    novo_produto=models.ProdutoBD(**produto.model_dump())

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto

from fastapi import HTTPException
from typing import List

@app.get("/api/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session=Depends(get_db)):
    return db.query(models.ProdutoBD).all()

@app.get("/api/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(produto_id: int, db: Session= Depends(get_db)):
    produto=db.query(models.ProdutoDB).filter(models.ProdutoBD.id==produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado na cafeteria"
        )
    return produto

@app.put("/api/produto_id/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados_novos: schemas.ProdutoCreate, db: Session=Depends(get_db)):
    query=db.query(models.ProductBD).filter(models.ProductBD.id == produto_id)
    produto=query.first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produtos não encontrado")

    query.update(dados_novos.model_dump(), synchronize_session=False)
    db.commit()

    return query.first()

@app.delete("/api/produtos/{produto_id}")
def remover_produtos(produto_id: int, db: Session = Depends(get_db)):
    produto=db.query(models.ProductBD).filter(models.ProductBD.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()

    return {"mensagem": f"Produto '{produto.nome}' removido com sucesso"}