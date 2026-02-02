'''
此程序需要以下模块：
- python-telegram-bot==22.5 
- urllib3==2.6.2 
''' 
from telegram import Update 
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters 
import configparser 
import logging 

def main(): 
    # 配置日志记录，以便查看初始化和错误消息
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        level=logging.INFO) 
    
    # 从文件加载配置数据
    logging.info('INIT: 正在加载配置...') 
    config = configparser.ConfigParser() 
    config.read('config.ini') 

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
    logging.info("UPDATE: " + str(update)) 

    # 将回显发送回客户端
    text = update.message.text.upper() 
    await update.message.reply_text(text) 

if __name__ == '__main__': 
    main()
