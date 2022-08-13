#!/usr/bin/python
from models import Base, Product, Barcode, User
from models import VoorraadMutatie, VoorraadMutatieSoort
from sqlalchemy import func
from database import Session, engine
from console import clearConsole, succes, question, info, warning, error, input_yesno, input_currency

Base.metadata.create_all(bind=engine)

while True:
    with Session() as session:
        clearConsole()

        # Assure admin
        users = []
        for userQuery in session.query(User).filter(User.name=="Bestuur"):
            users.append(userQuery)

        # We could not find this user in our DB
        if len(users) < 1:
            admin = User(name="Bestuur", balance=0)
            users.append(admin)
            session.add(admin)
            session.commit()
        else:
            admin = users[0]

        products = session.query(Product)
        for product in products:
            print(f"({product.id}): {product.name}")
        print(f"(0): New product")

        choice = int(input("Choice: "))
        if choice == 0:
            name = input("Name of new product?  ")
            price = input_currency("What is the price? ")
            newBarcode = input("New barcode is: ")
            inventory = int(input("How much items are you adding? "))
            totalPrice = input_currency("What was the total cost of these items? ")
            product = Product(name=name, price=price)
            session.add(product)
            session.flush()
            session.add(Barcode(barcode=newBarcode, product_id=product.id))
            voorraadmutatie = VoorraadMutatie(
                mutatiesoort=VoorraadMutatieSoort.start,
                product_id=product.id,
                hoeveelheid=inventory,
                user_id=admin.id,
                bedrag=-totalPrice
            )
            session.add(voorraadmutatie)
        else:
            chosenProduct = session.query(Product).filter(Product.id==choice)[0]
            currentInventory = 0
            currentProfit = 0
            for mutatie in session.query(VoorraadMutatie).filter(VoorraadMutatie.product_id==chosenProduct.id):
                currentInventory += mutatie.hoeveelheid
                currentProfit += mutatie.bedrag

            print()
            print(f"== {chosenProduct.name} ==")
            print(f" Price: {(chosenProduct.price/100):.2f}")
            print(f" Inventory: {currentInventory}")
            print(f" Total profit: {(currentProfit/100):.2f}")
            print()

            if input_yesno("Do you wish to change the price?") == "y":
                newPrice = input_currency("What is the new price? ")
                chosenProduct.price = newPrice

            if input_yesno("Are you adding a new barcode?") == "y":
                newBarcode = input("New barcode is: ")
                session.add(Barcode(barcode=newBarcode, product_id=chosenProduct.id))

            if input_yesno("Are you adding inventory?") == "y":
                addInventory = int(input("How much items are you adding? "))
                currentInventory += addInventory
                totalPrice = input_currency("What was the total cost of these items? ")
                voorraadmutatie = VoorraadMutatie(
                    mutatiesoort=VoorraadMutatieSoort.koop,
                    product_id=chosenProduct.id,
                    user_id=admin.id,
                    hoeveelheid=addInventory,
                    bedrag=-totalPrice
                )
                session.add(voorraadmutatie)

            if input_yesno("Are you interested in checking inventory?") == "y":
                countInventory = int(input("How much items do you count? "))
                correction = countInventory - currentInventory
                voorraadmutatie = VoorraadMutatie(
                    mutatiesoort=VoorraadMutatieSoort.correctie,
                    product_id=chosenProduct.id,
                    user_id=admin.id,
                    hoeveelheid=correction,
                    bedrag=0 # I guess?
                )
                session.add(voorraadmutatie)

        session.commit()
