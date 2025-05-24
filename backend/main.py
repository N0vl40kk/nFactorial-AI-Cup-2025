from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from db.models import SessionLocal, Order
from sqlalchemy.exc import SQLAlchemyError

openai.api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

class Query(BaseModel):
    text: str

class OrderCreate(BaseModel):
    description: str
    user_name: str
    type: str
    email: str = None
    phone: str = None

class OrderOut(BaseModel):
    id: int
    description: str
    user_name: str
    type: str
    email: str = None
    phone: str = None
    status: str
    created_at: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/ai-consultant/")
async def ai_consultant(query: Query):
    prompt = f"User wants: {query.text}\nSuggest best products or tenders."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role":"user", "content": prompt}]
    )
    return {"answer": response.choices[0].message.content.strip()}

@app.post("/api/order/")
async def create_order(
    description: str = Form(...),
    user_name: str = Form(...),
    type: str = Form(...),
    email: str = Form(None),
    phone: str = Form(None),
    db=Depends(get_db)
):
    try:
        order = Order(description=description, user_name=user_name, type=type, email=email, phone=phone)
        db.add(order)
        db.commit()
        db.refresh(order)
        return {"id": order.id, "status": "ok"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при создании заказа")

@app.get("/api/orders/")
def list_orders(db=Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()

@app.get("/api/orders/last/5", response_model=list[OrderOut])
def last_5_orders(db=Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    return orders