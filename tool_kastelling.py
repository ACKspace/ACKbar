#!/usr/bin/python
from models import Base, User, Product, Barcode, Font
from models import KasMutatie, KasMutatieSoort
from models import VoorraadMutatie, VoorraadMutatieSoort
from sqlalchemy import func
from database import Session, engine
import os, time
from console import clearConsole, succes, question, info, warning, error

with Session() as session:
    som = 0
    for kasmutatie in session.query(KasMutatie):
        som += kasmutatie.bedrag
    print(f"ACKbar geeft aan dat er (minstens) {som/100:.2f} in de kas moet liggen")
    daadwerkelijk = int(float(input("Hoeveel ligt er: ")) * 100)
    correctie = daadwerkelijk - som
    if correctie < 0:
        print(f"Er ontbreekt {correctie*-0.01:.2f} in de kas")
    elif correctie > 0:
        print(f"Er ligt {correctie*0.01:.2f} te veel in de kas!")
    afromen = int(float(input("Hoeveel geld afromen: ")) * 100)

    user = session.query(User).filter(User.name=="Bestuur")

    session.add(KasMutatie(mutatiesoort=KasMutatieSoort.correctie, user_id=user[0].id, bedrag=correctie))
    session.add(KasMutatie(mutatiesoort=KasMutatieSoort.afroming, user_id=user[0].id, bedrag=-afromen))
    session.commit()
