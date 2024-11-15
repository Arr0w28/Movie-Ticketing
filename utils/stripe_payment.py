import stripe

stripe.api_key = 'your-stripe-secret-key'

def create_payment_session(amount):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Movie Ticket',
                },
                'unit_amount': int(amount * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8501/success',
        cancel_url='http://localhost:8501/cancel',
    )
    return session.url
