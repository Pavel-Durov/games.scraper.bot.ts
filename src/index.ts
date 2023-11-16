import { TELEGRAM_BOT_CHAT_ID } from './config';
import { scrapeArsenalFixtures } from './scrape';

export async function start(chatId?: string) {
  await scrapeArsenalFixtures(chatId);
}

start(TELEGRAM_BOT_CHAT_ID);
