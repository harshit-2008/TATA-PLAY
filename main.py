import json, subprocess

from pyrogram import Client, filters

from tata import download_catchup, download_playback_catchup  

from utils import check_user, get_tplay_data

from config import api_id, api_hash, bot_token, script_developer




print("Installing YT-DLP")
subprocess.run("pip install yt-dlp".split())


data_json = get_tplay_data()

app = Client("Tpleeybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)




@app.on_message(filters.incoming & filters.text)
def tplay_past_catchup_dl_cmd_handler(app, message):

    if "/start" in message.text:
        app.send_photo(chat_id = message.chat.id, photo= "https://graph.org/file/9a10b85e931057451b73d.jpg",caption = "<b>TataPlay Catchup Bot</b>\n\n`> >`<b>Made By @LostIddd</b>")
    
        

    auth_user = check_user(message)
    if auth_user is None:
        return
    
    if "/tata" in message.text:
        
        if len(message.text.split()) < 3:
            message.reply_text("<b>Syntax: </b>`/tata [channelName] | [filename]`")
            return
        
        # with open("text.txt","w+") as f:
        #     f.writelines(str(data_json))
        # await app.send_document(message.chat.id, "text.txt")

        cmd = message.text.split("|")
        print(cmd)
        z = cmd[0].replace("/tata", "")
        z = z.replace("[", "")
        z = z.replace("]", "")
        print(z)
        channel = z.strip()

        if channel not in data_json:
            message.reply_text(f"<b>Channel Not in DB</b>")
            return

        download_playback_catchup(channel, cmd[1].strip() , data_json, app, message)

    if not "watch.tataplay.com" in message.text:
        return 
    
    if "coming-soon" in message.text:
        message.reply_text(f"<b>Can't DL something which has not aired yet\nCheck URL and try again...</b>")
        return
    download_catchup(message.text , data_json, app, message)

    if not "watch.tataplay.com" in message.text:
        return 
    
    if "coming-soon" in message.text:
        message.reply_text(f"<b>Can't DL something which has not aired yet\nCheck URL and try again...</b>")
        return
    download_catchup(message.text , data_json, app, message)


    

@app.on_message(filters.incoming & filters.command(['start']) & filters.text)
def start_cmd_handler(app, message):

    message.reply_text("<b>TataPlay Catchup Bot</b>\n\n`> >`<b> Made By @LostIddd</b>")
    

print(script_developer , "\n")

app.run()
