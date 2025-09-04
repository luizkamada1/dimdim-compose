import os
from flask import Flask, jsonify, request, render_template
from sqlalchemy.exc import SQLAlchemyError
from db import init_engine_and_session, Base
from models import Customer

# Cria a app Flask
app = Flask(__name__)

# Config DB
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://dimdim:dimdimpwd@db:5432/dimdimdb")
engine, SessionLocal = init_engine_and_session(DATABASE_URL)

# Cria as tabelas se não existirem
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
  return jsonify(status="ok"), 200

@app.get("/")
def index():
  return render_template("index.html")

# ----------- API CRUD -----------
@app.post("/api/customers")
def create_customer():
  data = request.get_json() or {}
  name = data.get("name")
  email = data.get("email")
  if not name or not email:
    return jsonify(error="name e email são obrigatórios"), 400

  session = SessionLocal()
  try:
    c = Customer(name=name, email=email)
    session.add(c)
    session.commit()
    session.refresh(c)
    return jsonify(c.to_dict()), 201
  except SQLAlchemyError as e:
    session.rollback()
    return jsonify(error=str(e)), 500
  finally:
    session.close()

@app.get("/api/customers")
def list_customers():
  session = SessionLocal()
  try:
    customers = session.query(Customer).order_by(Customer.id.asc()).all()
    return jsonify([c.to_dict() for c in customers])
  finally:
    session.close()

@app.get("/api/customers/<int:customer_id>")
def get_customer(customer_id: int):
  session = SessionLocal()
  try:
    c = session.get(Customer, customer_id)
    if not c:
      return jsonify(error="Customer não encontrado"), 404
    return jsonify(c.to_dict())
  finally:
    session.close()

@app.put("/api/customers/<int:customer_id>")
def update_customer(customer_id: int):
  data = request.get_json() or {}
  session = SessionLocal()
  try:
    c = session.get(Customer, customer_id)
    if not c:
      return jsonify(error="Customer não encontrado"), 404

    c.name = data.get("name", c.name)
    c.email = data.get("email", c.email)
    session.commit()
    session.refresh(c)
    return jsonify(c.to_dict())
  except SQLAlchemyError as e:
    session.rollback()
    return jsonify(error=str(e)), 500
  finally:
    session.close()

@app.delete("/api/customers/<int:customer_id>")
def delete_customer(customer_id: int):
  session = SessionLocal()
  try:
    c = session.get(Customer, customer_id)
    if not c:
      return jsonify(error="Customer não encontrado"), 404
    session.delete(c)
    session.commit()
    return jsonify(deleted=True)
  except SQLAlchemyError as e:
    session.rollback()
    return jsonify(error=str(e)), 500
  finally:
    session.close()

if __name__ == "__main__":
  port = int(os.getenv("APP_PORT", "8000"))
  app.run(host="0.0.0.0", port=port)
