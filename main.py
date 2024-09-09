import logging
from modelFER import predict_emotion
import cv2

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"👋 Привет {user.mention_html()}!"
        "\n"
        "Я бот, который умеет определять эмоции людей на фото.\n"
        "Просто отправь мне фотографию , и я проанализирую эмоции на ней.\n"
        "Затем я сообщу тебе, какие эмоции я обнаружил!\n\n"
        "❗️Фото лучше отправлять без очков и головных уборов❗️\n\n"
        "Команды, которые ты можешь использовать:\n"
        "/start: Начать диалог.\n"
        "/help: Получить информацию о том, как использовать бота.",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Просто отправь мне свое фото!!!")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Я не чат бот, вы должны отправить мне фотографию!")


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    image_path = 'user_photo.jpg'
    result_frame, predicted_emotions = predict_emotion("user_photo.jpg")
    cv2.imwrite('result_image.jpg', result_frame)
    await update.message.reply_photo('result_image.jpg')



    # Define messages based on predicted emotions
    if 'happy' in predicted_emotions:
        message = "Похоже, что вы счастливы! Продолжайте улыбаться 😊"
    elif 'sad' in predicted_emotions:
        message =  "Похоже, что вы грустите 😔"
    elif 'angry' in predicted_emotions:
        message = "Кажется, вы злитесь. Примите глубокий вдох и оставайтесь спокойными 🧘‍♂️"
    elif 'disgust' in predicted_emotions:
        message = "Вы кажется испытываете неприязнь 😒"
    elif 'fear' in predicted_emotions:
        message = "Кажется, вы испытываете страх 😱"
    elif 'surprise' in predicted_emotions:
        message = "Похоже, вы удивлены! 😮 Жизнь полна неожиданных моментов, принимайте их!"
    elif 'neutral' in predicted_emotions:
        message = "Кажется, вы чувствуете себя спокойно.😐 "
    else:
        message = "Я не уверен, какую эмоцию вы испытываете на данной фотографии 🤔"

    # Send the emotion-based text message
    await update.message.reply_text(
        f"{message}\n\n"
        "Если у вас есть еще фотографии 📸, не стесняйтесь отправить их мне! 😉"
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6736526778:AAFdkJy8CGDN9Kcw8u694F92oJtTQONeByg").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, photo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
