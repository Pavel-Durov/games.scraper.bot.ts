import TelegramBot from 'node-telegram-bot-api';
import { TELEGRAM_BOT_TOKEN } from './config';
import { initLog } from './logger';

const logger = initLog('telegram');

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });

let chatId = 361786193;

export function sendRichText(richText: string) {
  if (chatId) {
    bot.sendMessage(chatId, richText, { parse_mode: 'Markdown' });
  } else {
    logger.error('No chatId!');
  }
}

bot.onText(/\/start/, (msg) => {
  chatId = msg.chat.id;
  logger.info(chatId);
});

bot.on('text', (msg) => {
  const chatId = msg.chat.id;
  const messageText = msg.text;
  // Echo the received message
  bot.sendMessage(chatId, `You said: ${messageText}`);
});
