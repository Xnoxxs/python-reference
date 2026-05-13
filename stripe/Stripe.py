


import stripe
from datetime import datetime, timezone

api_key = ""
stripe.api_key = api_key  # Your secret key

# BASICS

def add_test_funds():
    try:
        # Create a charge to images funds to your Stripe test balance
        charge = stripe.Charge.create(
            amount=10000,  # Amount in cents (e.g., 10000 = 100 euros)
            currency="eur",
            source="tok_bypassPending",  # z token to bypass delays
        )
        print("Added test funds:", charge)
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def make_payout_from_main_account(amount):
    try:
        payout = stripe.Payout.create(
            amount=amount,  # €90 in cents
            currency="eur",  # Currency of your Stripe account
            method="standard",  # "instant" if eligible for instant payout
        )

        print(f"Payout initiated: {payout.id}")

        # Retrieve the status of the payout
        payout_status = stripe.Payout.retrieve(payout.id)
        print(f"Payout status: {payout_status['status']}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def create_payment_intent(amount, customer_id):
    try:
        # Create a PaymentIntent for a destination charge
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in the smallest currency unit (e.g., cents)
            currency="eur",
            payment_method_types=["card"],
            customer=customer_id,  # Replace with the Customer ID

        )

        print(f"PaymentIntent created: {payment_intent.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def complete_payment_intent (payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.confirm(
            payment_intent_id,  # Replace with your PaymentIntent ID
            payment_method="pm_card_visa"  # Replace with a valid test payment method ID
        )

        print(f"PaymentIntent ID: {payment_intent.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def create_split_payment_intent(amount, fee, connected_account_id):
    try:
        # Create a PaymentIntent for a destination charge
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in the smallest currency unit (e.g., cents)
            currency="eur",
            payment_method_types=["card"],
            application_fee_amount=fee,  # Platform's commission (20% of the total amount)
            transfer_data={
                "destination": connected_account_id  # Connected account ID where th rest of the amount will go to
            }
        )

        print(f"PaymentIntent created: {payment_intent.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def create_payment_intent_using_token(token, amount, currency="usd"):
    try:
        # Create a Payment Intent with the token
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in the smallest currency unit (e.g., cents for USD)
            currency=currency,
            payment_method_data={
                "type": "card",
                "card": {
                    "token": token  # Use the token generated from the client
                }
            },
        )
        print(f"Payment Intent {payment_intent.id }created successfully:")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def make_off_session_payment(amount, payment_method_id, customer_id):
    try:

        # Create a PaymentIntent for a destination charge
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in the smallest currency unit (e.g., cents)
            currency="eur",
            payment_method_types=["card"],
            customer=customer_id,  # Replace with the Customer ID
            payment_method=payment_method_id,  # Replace with the PaymentMethod ID
            off_session=True,  # Indicates the payment is made without the customer's interaction
            confirm=True # Must have for off session payments
        )

        print(f"Payment successful: {payment_intent.id}")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def get_payment_balance(payment_intent_id):
    try:
        # Step 1: Retrieve the PaymentIntent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        # Step 2: Retrieve the Charge object associated with the PaymentIntent
        charge = stripe.Charge.retrieve(payment_intent.latest_charge)

        # Step 3: Retrieve the Balance Transaction associated with the charge
        balance_transaction = stripe.BalanceTransaction.retrieve(charge.balance_transaction)

        # Step 4: Output relevant balance information
        processed_amount = balance_transaction.amount / 100  # Amount processed (in EUR)
        fee = balance_transaction.fee / 100  # Stripe fee (in EUR)
        net_amount = balance_transaction.net / 100  # Net amount after fees (in EUR)

        print({
            "processed_amount": processed_amount,
            "fee": fee,
            "net_amount": net_amount
        })
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def transfer_money_to_connected_account(amount, account_id):

    try:
        transfer = stripe.Transfer.create(
            amount=amount,  # Amount in the smallest currency unit (e.g., 9000 cents = €90)
            currency="eur",  # The currency you want to use
            destination=account_id,  # Connected account ID
            metadata={"purpose": "Payout for makeBooking"}  # Optional metadata
        )
        print(f"Transfer Succeeded: {transfer.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def get_card_details_from_payment(payment_method_id):
    payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

    # Extract card details
    if payment_method.type == "card":
        card_details = {
            "brand": payment_method.card.brand,
            "last4": payment_method.card.last4,
            "exp_month": payment_method.card.exp_month,
            "exp_year": payment_method.card.exp_year,
        }
        print(f"Payment Method ID: {payment_method_id}")
        print(f"Card Details: {card_details}")

def create_setup_intent_(customer_id):
    try:
        # Create a Setup Intent
        setup_intent = stripe.SetupIntent.create(
            customer=customer_id,  # Replace with the Stripe customer ID
        )

        print(f"SetUpIntent created: {setup_intent.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def refund_payment(payment_intent_id):
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent_id
            # amount=8000,  # €80 , if you want to refund a specific amount

        )
        print(f"Full refund successful: {refund.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def refund_split_payment(payment_intent_id):
    try:
        refund = stripe.Refund.create(
            payment_intent=payment_intent_id,
            refund_application_fee=True,
            reverse_transfer=True
            # amount=8000,  # €80 , if you want to refund a specific amount
        )
        print(f"Full refund successful: {refund.id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")




# CUSTOMERS



def create_customer():
    # Step 1: Create a customer
    customer = stripe.Customer.create(
        name="John Doe",
        email="john.doe@example.com",
        description="Customer for Advera",
        metadata={"user_id": "12345"}  # Add custom metadata if needed
    )
    print(f"Customer created: {customer.id}")

def delete_customer(customer_id):
    try:
        # Delete the customer
        deleted_customer = stripe.Customer.delete(customer_id)
        print(f"Customer {customer_id} deleted successfully: {deleted_customer}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def attach_card_to_customer(payment_method_id, customer_id):

    try:
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id
        )
        print(f"Payment method {payment_method_id} attached to customer {customer_id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def attach_card_using_token_to_customer(token, customer_id):
    try:
        # Attach the card token to the customer
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={"token": token},  # Use the token from the client
        )

        print(f"Payment method {payment_method.id} attached to customer {customer_id}")

        stripe.PaymentMethod.attach(
            payment_method.id,
            customer=customer_id,
        )

        print(f"Payment method {payment_method.id} attached to {customer_id}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")

def get_customer_cards(customer_id):
    try:
        # Fetch payment methods for the customer
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )

        cards = []
        for pm in payment_methods["repositories"]:
            # Ensure 'card' key exists in the response
            if "card" in pm:
                card_details = {
                    "id": pm["id"],  # Unique identifier for the payment method
                    "last4": pm["card"]["last4"],
                    "brand": pm["card"]["brand"],
                    "expiry_month": pm["card"]["exp_month"],
                    "expiry_year": pm["card"]["exp_year"],
                }
                cards.append(card_details)

        print(f"cards: {cards}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def get_specific_customer_card(payment_method_id):
    try:
        # Retrieve the payment method directly using its ID
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

        # Extract card details if the payment method is of type "card"
        if payment_method["type"] == "card":
            card_details = {
                "payment_method_id": payment_method["id"],
                "last4": payment_method["card"]["last4"],
                "brand": payment_method["card"]["brand"],
                "expiry_month": payment_method["card"]["exp_month"],
                "expiry_year": payment_method["card"]["exp_year"],
                "customer_id": payment_method.get("customer"),  # Customer ID associated with the card (if any)
            }
            print(f"card details: {card_details}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def set_customer_card_to_default(customer_id, payment_method_id):
    try:
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id
            }
        )

        print("Card set to default successfully")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def get_customer_invoices(customer_id):
    try:
        invoices = stripe.Invoice.list(customer=customer_id)

        # Print out the retrieved invoices
        for invoice in invoices['repositories']:
            print(f"Invoice ID: {invoice.get('id')}")
            print(f"Amount Due: {invoice.get('amount_due')}")
            print(f"Status: {invoice.get('status')}")
            print(f"Created At: {invoice.get('created')}")
            print(f"Payment Intent: {invoice.get('payment_intent')}")
            print(f"Hosted Invoice URL: {invoice.get('hosted_invoice_url')}")
            print("-" * 30)

    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")



# SUBSCRIPTIONS



def create_subscription(customer_id, price_id):
    try:
        # Create a subscription
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": price_id},  # Replace with your Price ID
            ],
            payment_behavior="default_incomplete",  # Handle payment failure properly
            expand=["latest_invoice.payment_intent"],  # Expand fields for easier access
        )
        print(f"Subscription ID: {subscription.id}")

        # Access the PaymentIntent
        payment_intent = subscription["latest_invoice"]["payment_intent"]

        # Attempt to confirm the PaymentIntent
        payment_intent = stripe.PaymentIntent.confirm(
            payment_intent.id,
            payment_method="pm_card_visa"  # Replace with a valid test payment method ID
        )

        # Check the PaymentIntent status
        if payment_intent["status"] == "requires_action":
            pass

        elif payment_intent["status"] == "succeeded":
            print("subscription created successfully")

        return subscription
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
    except Exception as e:
        print(f"Error: {e}")

def confirm_subscription_payment(payment_intent_id):
    try:
        # Attempt to confirm the PaymentIntent
        payment_intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method="pm_card_visa"  # Replace with a valid test payment method ID
        )
        print(f"PaymentIntent {payment_intent.id} confirmed successfully")
    except stripe.error.StripeError as e:
       print(f"Stripe Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def check_subscription_status(subscription_id):
    try:

        # Retrieve the subscription
        subscription = stripe.Subscription.retrieve(subscription_id)

        if subscription["status"] == "active":
            print(f"Subscription {subscription_id} is active.")
        else:
            print(f"Subscription {subscription_id} is not active. Status: {subscription['status']}")

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

def get_customer_subscriptions(customer_id):
    try:

        # Retrieve subscriptions for the customer
        subscriptions = stripe.Subscription.list(customer=customer_id)

        subscriptions_list = []

        # Print subscription details
        for subscription in subscriptions.data:

            if subscription.status == "active":

                print(subscription.id)

                data = {
                    "subscription_id": subscription.id,
                    "start_date": datetime.fromtimestamp(subscription['start_date'], tz=timezone.utc).isoformat(),
                    "next_payment": datetime.fromtimestamp(subscription['current_period_end'], tz=timezone.utc).isoformat(),
                    "cancel_at_period_end": subscription.get("cancel_at_period_end")  # Add cancel_at_period_end
                }

                for item in subscription['items']['repositories']:
                    #repositories["price_id"] = item['price']['id']
                    data["price"] = item['price']['unit_amount']  # Retrieve the actual price amount

                    # Get the product associated with the price
                    product_id = item['price']['product']  # Get the product ID
                    product = stripe.Product.retrieve(product_id)  # Retrieve the product
                    data["subscription_name"] = product['name']  # Add the product name

                # Access the latest invoice
                invoice = stripe.Invoice.retrieve(subscription["latest_invoice"])
                # Access the payment intent from the invoice
                payment_intent = stripe.PaymentIntent.retrieve(invoice["payment_intent"])
                # Retrieve the payment method details from the payment intent
                payment_method_id = payment_intent.get("payment_method")
                # Retrieve the payment method details from the payment method id
                payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

                # Extract card details
                if payment_method.type == "card":

                    data["card_details"] = {
                        "brand": payment_method.card.brand,
                        "last4": payment_method.card.last4,
                        "exp_month": payment_method.card.exp_month,
                        "exp_year": payment_method.card.exp_year,
                    }

                subscriptions_list.append(data)


        print(subscriptions_list)

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Exception Error: {e}")

def cancel_subscription(subscription_id):
    try:

        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
            # True to end it until the next billing, False to end it immediately
        )
        print(f"Subscription {subscription_id} canceled successfully!")
        print(f"Status: {subscription['status']}")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
    except Exception as e:
        print(f"Error: {e}")

def resume_subscription(subscription_id):
    try:

        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )

        print(f"subscription: {subscription_id} renewed successfully")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Execption Error: {e}")



# CONNECTED ACCOUNTS

def create_magic_link(account_id):

    try:
        # This is to send the link to the stripe dashboard to a specific connected account
        login_link = stripe.Account.create_login_link(account_id)
        print(f"Login link: {login_link.url}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def make_payout(amount, account_id):

    try:
        payout = stripe.Payout.create(
            amount=amount,  # €90 , If you want to extract all funds, just don't put the parameter 'amount'
            currency="eur",  # Replace with the currency of the connected account
            stripe_account=account_id,  # connected account ID
            # destination="ba_12345ABCDE",  # External account ID for the connected account
        )

        print(f"Payout initiated: {payout.id}")

        payout_status = stripe.Payout.retrieve(
            payout.id,  # Payout ID
            stripe_account="acct_1Qj0aZQrMBgoBv3U",
        )

        print(f"Payout status: {payout_status['status']}")
    except stripe.error.StripeError as e:
        print(f"StripeError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def reverse_transfer(transfer_id):

    """
       Take money from a connected account back to my main account
       Example:
           Customer pays 100 euros, you took 20 euros, connected account(Hamid) took 80
           In that payment of 100 euros, in the 'Payment Details' section
           there is information about the transfer of 80 euros you made to Hamid
           There, you can find the transfer id and use it
           You can take back the full 80 euros or less from Hamid

        IMPORTANT:
           Stripe allows connected accounts to have negative balances
           Meaning, if Hamid has only 80 euros and I reverse transfer and take 100 euros
           then he can have a balance of -20 euros
           Therefore always check to see if the connected account has enough fund


    """
    try:
        reversal = stripe.Transfer.create_reversal(
            transfer_id,
            amount= 1000  # €10.00
        )
        print(f"Reversal {reversal.id} successful!")
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None


def delete_account(account_id):
    try:
        stripe.Account.delete(account_id)
        print("Account Deleted")
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None


# WEB

def create_customer_portal_session(customer_id):
    try:

        session = stripe.billing_portal.Session.create(
            customer= customer_id,
            return_url='https://yourwebsite.com/dashboard'  # Redirect URL after leaving the portal
        )
        print(f"session url: {session.url}")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
    except Exception as e:
        print(f"Error: {e}")

def create_checkout_session(customer_id, amount):
    try:

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Sample Product',
                    },
                    'unit_amount': amount,  # Amount in cents ($50.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            customer= customer_id,
            success_url='http://localhost:8080/success',  # Replace with your URL
            cancel_url='http://localhost:8080/cancel',    # Replace with your URL
        )
        print(f"session url: {session.url}")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
    except Exception as e:
        print(f"Error: {e}")

def create_setup_session(customer_id):
    try:

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='setup',  # Use 'setup' mode for saving cards
            success_url='http://localhost:8080/success',  # Replace with your success URL
            cancel_url='http://localhost:8080/cancel',    # Replace with your cancel URL
            customer=customer_id,  # Replace with your existing customer ID or create a new one
        )
        print(f"session url: {session.url}")
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e.user_message}")
    except Exception as e:
        print(f"Error: {e}")

def get_checkout_session(session_id):
    try:

        # Retrieve the checkout session details from Stripe
        session = stripe.checkout.Session.retrieve(session_id)

        # Send the payment details back to the client
        print({
            "payment_intent": session.get('payment_intent'),
            "customer": session.get('customer'),
            "amount_total": session.get('amount_total'),
            "status": session.get('status'),
        })
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
