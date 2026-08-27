from pydantic import BaseModel
from typing import Optional

class ProdutoCreate(BaseModel):
    nome: str
    categoria: str
    preco: float
    disponivel: Optional[bool]=True

class ProdutoResponse(ProdutoCreate):
    id: int

    class Config:
        from_attributes=True