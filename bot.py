from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from db import init_db, add_hit, get_stats, clear_db, get_hits
from checks import adobe_check, check_email_regex
from lines import lines_init, lines_clear, add_line, del_lines, request_lines
from license_db import init_license, add_license, user_license, clear_license, get_license, find_license, is_registered, revoke_license, license_exists
load_dotenv()

auid = int(os.getenv("ADMIN_ID"))


async def start(update: Update, context: ContextTypes):
    uid = ("@" + update.effective_user.username) or update.effective_user.name
    await update.message.reply_text(f"😸 Meow, {uid}!\n\n- Use /help for commands")


async def read_file(update: Update, context: ContextTypes):
    uid = update.effective_user.id

    if is_registered(uid) == 0:
        await update.message.reply_text("[-] You are not registered, use /key!")
        return

    doc = update.message.document

    if not doc.file_name.endswith(".txt"):
        await update.message.reply_text("[-] Please upload a .txt file!")
        return

    del_lines(uid)

    new_file = await context.bot.get_file(doc.file_id)
    await new_file.download_to_drive(f"temp_{uid}.txt")

    count = 0
    with open("temp_{uid}.txt", "r") as f:
        for line in f:
            email = line.strip()
            if check_email_regex(email):
                add_line(uid, email)
                count += 1
    await update.message.reply_text(f"[+] Loaded {count} emails into your queue!")


async def hits(update: Update, context: ContextTypes):
    uid = update.effective_chat.id

    if is_registered(uid) == 0:
        await update.message.reply_text("[-] You are not registered, use /key!")
        return

    allhits = get_hits(uid)
    newstr = ""
    for hit in allhits:
        newstr = newstr + str(hit[0]) + '\n'
    if newstr == "":
        await update.message.reply_text("[-] You have no hits!")
    else:
        await update.message.reply_text("💎 Your hits: \n\n" + newstr)


async def createhits(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        init_db()
        await update.message.reply_text("[+] DB created! (Could've already existed)")
    except Exception as e:
        await update.message.reply_text(f"[-] Error creating DB: {e}")


async def createlines(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        lines_init()
        await update.message.reply_text("[+] DB created! (Could've already existed)")
    except Exception as e:
        await update.message.reply_text(f"[-] Error creating DB: {e}")


async def createlicense(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        init_license()
        await update.message.reply_text("[+] DB created! (Could've already existed)")
    except Exception as e:
        await update.message.reply_text(f"[-] Error creating DB: {e}")


async def clearhits(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        clear_db()
        await update.message.reply_text("[+] Hits cleared!")
    except Exception as e:
        await update.message.reply_text(f"[-] Error clearing Hits: {e}")


async def clearlines(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        lines_clear()
        await update.message.reply_text("[+] Lines cleared!")
    except Exception as e:
        await update.message.reply_text(f"[-] Error clearing Lines: {e}")


async def clearlicense(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        clear_license()
        await update.message.reply_text("[+] Licenses cleared!")
    except Exception as e:
        await update.message.reply_text(f"[-] Error clearing Licenses: {e}")


async def clearall(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    try:
        lines_clear()
        clear_db()
        clear_license()
        await update.message.reply_text("[+] All DBs cleared!")
    except Exception as e:
        await update.message.reply_text(f"[-] Error clearing Lines: {e}")


# single check command
async def check(update: Update, context: ContextTypes):
    uid = update.effective_user.id

    if is_registered(uid) == 0:
        await update.message.reply_text("[-] You are not registered, use /key!")
        return

    email = context.args[0] if context.args else ""

    if not check_email_regex(email):
        await update.message.reply_text("[-] Enter a valid email!")
        return

    if adobe_check(email):
        add_hit(uid, email, 'Good')
        await update.message.reply_text(f"[+] {email} is registered!")
    else:
        await update.message.reply_text(f"[-] {email} is not registered!")

# mass check command - will be done using an uploaded .txt file (eventually)


async def checkall(update: Update, context: ContextTypes):
    uid = update.effective_chat.id

    if is_registered(uid) == 0:
        await update.message.reply_text("[-] You are not registered, use /key!")
        return

    emails = request_lines(uid)
    if not emails:
        await update.message.reply_text("[-] Your queue is empty!")
        return
    await update.message.reply_text(f"[+] Starting mass check for {len(emails)} emails...")

    results = {'hits': 0, 'bad': 0}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(adobe_check, email)                   : email for email in emails}

        for future in as_completed(futures):
            email = futures[future]
            try:
                is_hit = future.result()

                if is_hit:
                    add_hit(uid, email, 'Good')
                    results['hits'] += 1
                else:
                    results['bad'] += 1
            except Exception as e:
                print(f"[-] Error checking {email}: {e}")

    await update.message.reply_text(f"[+] Check complete!\n\n- Hits: {results['hits']}\n\n- Bad: {results['bad']}")


async def addlicense(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    add_license()
    await update.message.reply_text("New license created!")


async def getlicense(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    licenses = get_license()
    licStr = ""
    for l in licenses:
        licStr = licStr + (f"#{l[0]}\n\n")
    if len(licenses) < 1:
        await update.message.reply_text("[-] No current licenses.")
        return
    else:
        await update.message.reply_text(f"Current licenses:\n\n{licStr}")
        return


async def key(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    lkey = context.args[0] if context.args else ""
    if lkey == "":
        await update.message.reply_text("[-] Usage: /key <code>")
        return

    if is_registered(uid) == 1:
        await update.message.reply_text("[-] You have already redeemed a key!")
        return

    if find_license(lkey) == 1:
        user_license(uid, lkey)
        await update.message.reply_text(f"[+] License key redeemed!")
        return
    else:
        await update.message.reply_text(f"[-] License key not found!")
        return


async def revoke(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    if uid != auid:
        return
    lkey = context.args[0] if context.args else ""

    if lkey == "":
        await update.message.reply_text("[-] Usage: /revoke <code>")
        return

    if license_exists(lkey) == 1:
        revoke_license(lkey)
        await update.message.reply_text(f"[+] License key revoked!")
        return
    else:
        await update.message.reply_text(f"[-] License key not found!")
        return


async def me(update: Update, context: ContextTypes):
    uid = update.effective_user.id
    username = update.effective_user.name
    name = update.effective_user.full_name

    regstr = "Yes" if is_registered(uid) else "No"

    await update.message.reply_text(f"Profile:\n\n- User ID: {uid}\n- Username: {username}\n- Name: {name}\n- Registered: {regstr}")


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("checkall", checkall))
    app.add_handler(CommandHandler("createlines", createlines))
    app.add_handler(CommandHandler("createhits", createhits))
    app.add_handler(CommandHandler("clearlines", clearlines))
    app.add_handler(CommandHandler("clearhits", clearhits))
    app.add_handler(CommandHandler("clearall", clearall))
    app.add_handler(CommandHandler("hits", hits))
    app.add_handler(CommandHandler("read_file", read_file))
    app.add_handler(CommandHandler("createlicense", createlicense))
    app.add_handler(CommandHandler("clearlicense", clearlicense))
    app.add_handler(CommandHandler("addlicense", addlicense))
    app.add_handler(CommandHandler("getlicense", getlicense))
    app.add_handler(CommandHandler("key", key))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(MessageHandler(filters.Document.ALL, read_file))

    print("[+] Bot running!")
    app.run_polling()
