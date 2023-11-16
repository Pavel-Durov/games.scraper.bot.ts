import { scrapeArsenalFixtures } from './scrape';

export async function start(chatId?: string) {
  await scrapeArsenalFixtures(chatId);
}

start();
