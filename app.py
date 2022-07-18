#!/usr/bin/env python3
from models import Base, User, Product, Barcode, Font
from models import KasMutatie, KasMutatieSoort
from models import BankStorting
from models import VoorraadMutatie, VoorraadMutatieSoort
from sqlalchemy import func
from database import Session, engine
import os, time
from console import clearConsole, succes, question, info, warning, error, input_yesno, input_currency



def logo(font):
    clearConsole()
    if font is None:
        print("ACKbar with font issues")
    else:
        os.system(f"figlet -t -f {font.name} ACKbar | lolcat")

def purchaseScreen(users, products, deposit, transfers, total, font):
    logo(font)
    print("")
    if users[0].name != "guest":
        print(f"Hello {users[0].name}, you have {(users[0].balance/100):.2f} on your account.")
    else:
        print(f"Hello guest!")
    print(f"")
    print(info("Commands:"))
    print(info("  cash    - Deposit with cash"))
    if users[0].name != "guest":
        print(info("  bank    - Deposit with wire transfer"))
    print(info("  ------"))
    print(info("  cancel  - Cancel transaction"))
    print(info("  accept  - Accept transaction"))
    print("")
    if users[0].name != "guest":
        print(f"{'balance' : <25} {(users[0].balance/100):6.2f}")
    if deposit > 0:
        print(f"{'deposit'.ljust(25)} {(deposit/100):6.2f}")

    for transfer in transfers:
        foo = f"transfer {transfer[1]}"
        print(f"{foo.ljust(25)} {(transfer[0]/100):6.2f}")

    if len(products) > 0:
        for product in products:
            print(f"{product.name.ljust(25)} {(-product.price/100):6.2f}")
    print("-"*32)
    if users[0].name == "guest":
        if total >= 0:
            print(f"{'your change'.ljust(25)} {(total/100):6.2f}")
        else:
            print(f"{'please deposit'.ljust(25)} {(-total/100):6.2f}")
    else:
        print(f"{'new balance'.ljust(25)} {(total/100):6.2f}")

def startScreen(font):
    logo(font)
    print("")
    if font is not None:
        print(info(f"{font.name} {font.score}"))
    print()
    print("Commands:")
    print("  guest - use a guest account")
    print("  u     - upvote logo")
    print("  d     - downvote logo")

def randomFont(session):
    return session.query(Font).order_by(func.random()).first()

def performCheckout(user, products, deposit, session, transfers):
    # Add the prices of all the products
    totalPrice = 0
    for product in products:
        totalPrice += product.price

    # What balance would this checkout result in?
    resulting_balance = user.balance + deposit - totalPrice
    for transfer in transfers:
        resulting_balance += transfer[0]

    # Can the user afford this?
    if resulting_balance < 0:
        return False

    # The user has enough money and the transaction is going to be executed
    else:
        if user.name == "guest":
            user.balance = 0
        else:
            user.balance = resulting_balance

        # If cash has been deposited, we record a kas mutation
        if user.name == "guest": # Guests always deposit totalPrice
            session.add( KasMutatie(mutatiesoort=KasMutatieSoort.storting, user_id=user.id, bedrag=totalPrice) )
        elif deposit > 0:
            session.add( KasMutatie(mutatiesoort=KasMutatieSoort.storting, user_id=user.id, bedrag=deposit) )

        # If products have been bought, we record a voorraad mutation
        voorraadmutaties = {}
        for product in products:
            if voorraadmutaties.get(product.id, None) is None:
                voorraadmutaties[product.id] = {"count":1, "unitprice":product.price}
            else:
                voorraadmutaties[product.id]["count"] += 1
        for product_id in voorraadmutaties:
            hoeveelheid = voorraadmutaties[product_id]["count"]
            bedrag = voorraadmutaties[product_id]["unitprice"] * hoeveelheid
            voorraadmutatie = VoorraadMutatie(
                mutatiesoort=VoorraadMutatieSoort.koop,
                product_id=product_id,
                user_id=user.id,
                hoeveelheid=-hoeveelheid,
                bedrag=bedrag
            )
            session.add(voorraadmutatie)

        # We finalize the transaction
        session.commit()
        return True



def main(Session):
    isRunning = True
    with Session() as session:
        font = randomFont(session)
        startScreen(font)
    
    scanned = input(question("\nType nickname or scan barcode: "))
    with Session() as session:

        users = []

        # User wants to quit the program
        if scanned.lower() == "q" or scanned.lower() == "quit":
            isRunning = False

        # User wants to upvote the logo
        elif scanned == "u":
            font = session.query(Font).filter(Font.name==font.name).first()
            font.score += 1
            session.commit()
            font = None

        # User wants to downvote the logo
        elif scanned == "d":
            font = session.query(Font).filter(Font.name==font.name).first()
            font.score -= 1
            session.commit()
            font = None

        # User entered nothing, refresh screen
        elif scanned == "":
            pass

        # User wants to login or create a new account
        else:
            for userQuery in session.query(User).filter(func.lower(User.name)==scanned.lower()):
                users.append(userQuery)
            assert len(users) < 2, "Database returned multiple users!"
            # We could not find this user in our DB
            if len(users) == 0:
                print(f"{scanned} is not registered")
                yn = input_yesno("Do you wish to register this user?")
                if yn == "y":
                    user = User(name=scanned, balance=0)
                    users.append(user)
                    session.add(user)
                    session.commit()

        # We found a user or they have just registered
        if len(users) == 1:
            userBusy = True
            products = []
            transfers = []
            deposit = 0

            while userBusy:
                total = users[0].balance + deposit
                for product in products:
                    total -= product.price
                for transfer in transfers:
                    total += transfer[0]
                purchaseScreen(users, products, deposit, transfers, total, font)
                scanned = input(question("\nType command or scan product: "))

                # User wants to deposit money
                if scanned.lower() in ["cash", "deposit"]:
                    deposit += input_currency()

                # User wants to transfer money
                elif scanned.lower() == "bank" and users[0].name != "guest":
                    session.flush()
                    transactionNo = session.query(BankStorting).filter(BankStorting.user_id==users[0].id).count()
                    code = f"BAR-{users[0].id}-{transactionNo}"
                    print()
                    print(f"Please perform a wire transfer with the following info:")
                    print(f"Rekening      -  NL16 ABNA 0563 9410 06")
                    print(f"Ten name van  -  Stichting ACKspace")
                    print(f"Omschrijving  -  {code}")
                    print()
                    bedrag = input_currency()
                    isTransfer = input_yesno("Confirm transfer?") == "y"
                    if isTransfer:
                        transfers.append([bedrag, code])
                        session.add( BankStorting(user_id=users[0].id, bedrag=bedrag, code=code) )

                # User wants to finish transaction
                elif scanned.lower() in ["accept", "checkout"]:
                    if performCheckout(users[0], products, deposit, session,transfers):
                        print(succes("Transaction confirmed!"))
                        time.sleep(2)
                        userBusy = False
                    else:
                        print(warning(f"Not enough funds! Check the tab."))
                        time.sleep(1)

                # User wants to cancel transaction
                elif scanned.lower() in ["cancel", "abort"]:
                    print(warning(f"Transaction canceled!"))
                    session.rollback()
                    userBusy = False
                    time.sleep(2)

                # User wants to scan a product
                else:
                    productQueries = []
                    for barcodeQuery in session.query(Barcode).filter(Barcode.barcode==scanned):
                        productQueries.append(barcodeQuery.product)
                    if len(productQueries) == 0:
                        print(warning("Invalid product code or command."))
                        time.sleep(1)
                    else:
                        products.extend(productQueries)
    return isRunning

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    isRunning = True
    font = None
    while isRunning:
        isRunning = main(Session)
