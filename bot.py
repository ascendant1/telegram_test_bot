from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
import praw

MSG_START = 'Hi, type a subreddit name, you want. For example: worldnews'
MSG_SUGGEST = 'You can find popular subreddits on redditlist.com'
MSG_RANDOM = 'Random Subreddit'
MSG_HELP = '/suggest - recive suggestions about subreddits'
MSG_INVALID_SUB = 'Invalid subreddit'
USERAGENT = "super simple telegram bot v1.0 by /u/qualityq1"

reddit = praw.Reddit()


class RedditBot:
    def __init__(self):
        updater = Updater(token='token')
        dispatcher = updater.dispatcher
        start_command_handler = CommandHandler('start', self.start)
        suggest_command_handler = CommandHandler('suggest', self.suggest)
        help_command_handler = CommandHandler('help', self.help)
        receive_message_handler = MessageHandler(Filters.text, self.receive)
        dispatcher.add_handler(start_command_handler)
        dispatcher.add_handler(suggest_command_handler)
        dispatcher.add_handler(help_command_handler)
        dispatcher.add_handler(receive_message_handler)

        updater.start_polling()

        self.message = ''
        self.chat_id = None
        self.user_id = None
        self.subreddit = None
        self.submission = []

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=MSG_START)

    def suggest(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=MSG_SUGGEST)

    def help(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=MSG_HELP)

    def receive(self, bot, update):
        print("Received", update.message)
        self.set_message(update)
        self.set_chat_id(update)
        self.set_user_id(update)
        self.set_subreddit(bot)

        if self.subreddit is not None:
            self.get_feed()
            self.show_feed(bot)

    def set_message(self, update):
        self.message = update.message.text

    def set_chat_id(self, update):
        self.chat_id = update.message.chat_id

    def set_user_id(self, update):
        self.user_id = update.message.from_user.id

    def set_subreddit(self, bot, name=None):
        if 'random' in self.message.lower().split():
            name = str(reddit.random_subreddit())
            bot.sendMessage(chat_id=self.chat_id, text=name)
        elif name is None:
            name = self.message.lower()
            print(name)
        try:
            self.subreddit = reddit.subreddit(name)
            print(str(self.subreddit.fullname))
        except:
            bot.sendMessage(chat_id=self.chat_id, text=MSG_INVALID_SUB)
            self.subreddit = None

    def get_feed(self):
        for submission in self.subreddit.hot(limit=10):
            self.submission.append(submission)

    def show_feed(self, bot):
        for submission in self.submission:
            text = "[%s](%s)" % (submission.title, submission.url)
            bot.sendMessage(chat_id=self.chat_id,
                            text=text,
                            parse_mode=ParseMode.MARKDOWN)
        del self.submission[:]


if __name__ == '__main__':
    RedditBot()
