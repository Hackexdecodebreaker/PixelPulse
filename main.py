import telepot
from telepot.loop import MessageLoop
from google import genai
from google.genai import types
from google.api_core import retry 
import markdown




bot=telepot.Bot(TELEGRAM_BOT_TOKEN)




def handle(msg):
    
    try:
        chat_id=msg['chat']['id']
        command=msg['text']
        bot.sendMessage(chat_id,"Processing your request...")
        result=operation(command)
        for i in range(0, len(result), 4096):
            bot.sendMessage(chat_id, result[i:i+4096])
    except Exception as e:
        print (str(e))

    






def operation(cmd):
   
    GOOGLE_API_KEY= GOOGLE_API_KEY

    is_retriable=lambda e:(isinstance(e,genai.errors.APIError) and e.code in {429,503})
    genai.models.Models.generate_content=retry.Retry(predicate=is_retriable)(genai.models.Models.generate_content)



    client=genai.Client(api_key=GOOGLE_API_KEY)
    response=client.models.generate_content(model="gemini-2.0-flash",contents=cmd)
    return response.text

   
   



try:
    MessageLoop(bot,handle).run_forever()
except Exception as e:
    bot.sendMessage(handle.chat_id,str(e))
