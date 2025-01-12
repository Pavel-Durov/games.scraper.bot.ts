import axios from 'axios';
import * as cheerio from 'cheerio';

import { Fixture, FixturesUpdate } from './domain';
import { parseDate } from './date';
import { fixturesToRichText } from './format';
import { initLog } from './logger';
import { sendRichText } from './telegram';

const logger = initLog('main');

async function parseFixtures(content: string): Promise<Fixture[]> {
  const result: Fixture[] = [];
  const $ = cheerio.load(content);

  const cards = $('.fixture-card');
  for (const card of cards) {
    const headers = $(card).find('.card__header');
    let fixture = undefined;

    for (const header of headers) {
      const date = $(header).find('.event-info__date').text().trim();
      const venue = $(header).find('.event-info__venue').text().trim();
      const extra = $(header).find('.event-info__extra').text().trim();

      fixture = { date: parseDate(date), venue, leage: extra };
    }
    const contents = $(card).find('.team-crest__name-value');

    if (contents.length > 0) {
      fixture.homeTeam = $(contents[0])
        .text()
        .trim();
    }
    if (contents.length > 1) {
      fixture.awayTeam = $(contents[1])
        .text()
        .trim();
    }

    result.push(fixture);
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
        fixtures: fixtures.filter((f) => f.venue === VENUE && f.date > now),
        source: URL
      };
      const message = fixturesToRichText(update, now);
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
