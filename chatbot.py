'''
此程序需要以下模块：
- python-telegram-bot==22.5 
- urllib3==2.6.2 
''' 
from telegram import Update 
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters 
import configparser 
import logging 
from ChatGPT_HKBU import ChatGPT

gpt = None

def main(): 
    # 配置日志记录，以便查看初始化和错误消息
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level=logging.INFO) 
    
    # 从文件加载配置数据
    logging.info('INIT: 正在加载配置...') 
    config = configparser.ConfigParser() 
    config.read('config.ini') 

    # 在配置加载后、注册 handlers 之前创建 ChatGPT 客户端
    global gpt
    gpt = ChatGPT(config)

    # 为您的机器人创建一个应用程序
    logging.info('INIT: 正在连接 Telegram 机器人...') 
    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build() 

    # 注册消息处理程序
    logging.info('INIT: 注册消息处理程序...') 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback)) 

    # 启动机器人
    logging.info('INIT: 初始化完成！') 
    app.run_polling() 

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text(response)
    logging.info("UPDATE: " + str(update))
    loading_message = await update.message.reply_text('Thinking...')

    # send the user message to the ChatGPT client
    response = gpt.submit(update.message.text)

    # send the response to the Telegram box client
    await loading_message.edit_text(response)

if __name__ == '__main__': 
    main()
