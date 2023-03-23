# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
stripe.api_key = "sk_test_51Mi5SeAxQsk8kssvom87yN3TqmqI9LLlTReUD3iKxMGn3WItkeaZTb5lqAVxVnOhFNErGUCV7ENpyz5FT1DWRzBy00pkk56HcU"

stripe.PaymentLink.create(
  line_items=[{"price": "{{PRICE_ID}}", "quantity": 1}],
  after_completion={"type": "redirect", "redirect": {"url": "https://example.com"}},
)