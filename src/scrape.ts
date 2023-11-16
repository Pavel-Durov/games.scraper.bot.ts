import axios from 'axios';
import * as cheerio from 'cheerio';

import { Fixture, FixturesUpdate } from './domain';
import { parseDate } from './date';
import { fixturesToRichText } from './format';
import { sendRichText } from './telegram';
import { initLog } from './logger';

const logger = initLog('main');

async function parseFixtures(content: string): Promise<Fixture[]> {
  const result: Fixture[] = [];
  const $ = cheerio.load(content);
  const fixtures = $('.card__header');
  for (const element of fixtures) {
    const event = $(element).find('.event-info');
    const date = $(element).find('.event-info__date').text().trim();
    const venue = $(event).find('.event-info__venue').text().trim();
    const extra = $(event).find('.event-info__extra').text().trim();
    result.push({ date: parseDate(date), venue, leage: extra });
  }
  return result;
}

const URL =
  'https://www.arsenal.com/fixtures?field_arsenal_team_target_id=All&field_competition_target_id=All&field_home_away_or_neutral_value=All&field_tv_channel_target_id=All&revision_information=';

const VENUE = 'Emirates Stadium';
export async function scrapeArsenalFixtures(chatId?: string) {
  const now = new Date();

  try {
    const response = await axios.get(URL);
    if (response.status === 200) {
      const fixtures = await parseFixtures(response.data);
      const update: FixturesUpdate = {
        date: now,
        venue: VENUE,
        fixtures: fixtures.filter((f) => f.venue === VENUE && f.date > now)
      };
      const message = fixturesToRichText(update);
      logger.info(message);
      await sendRichText(message, chatId);
    } else {
      logger.error(`Error: Unable to fetch the page. Status Code: ${response.status}`);
    }
  } catch (error) {
    logger.error(`Error: ${error.message}`);
  }
  logger.info(`Process ${process.pid} is about to exit.`);
  process.exit(0);
}
