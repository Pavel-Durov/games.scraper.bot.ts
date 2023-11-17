import { formatDate, isToday, formatDateWithYear } from './date';
import { Fixture, FixturesUpdate } from './domain';

function getFixtureLine({ date, leage, homeTeam, awayTeam }: Fixture): string {
  const fdate = formatDate(date);
  let result = '';
  if (homeTeam === undefined || awayTeam === undefined) {
    result = `*${fdate}* - (${leage})\n`;
  } else if (awayTeam === undefined) {
    result = `*${fdate}* - ${homeTeam} (${leage})\n`;
  } else {
    result = `*${fdate}* - ${homeTeam} VS ${awayTeam} (${leage})\n`;
  }
  if (isToday(date)) {
    result = `Today 👉 *${result}`;
  }
  return result;
}

/**
 * Converst fixtures update object to telegram richstring message.
 * @param update fixture update object
 * @returns formatted telegram richstring message
 */
export function fixturesToRichText(update: FixturesUpdate): string {
  let result = `📟 *Update for ${formatDateWithYear(update.date)}*\n`;
  if (update.fixtures === undefined || update.fixtures.length === 0) {
    return `${result}*No upcoming games for the year*\n`;
  }

  result += `⚽ *Games at ${update.venue} for this year*\n\n`;
  for (const fixture of update.fixtures) {
    result += getFixtureLine(fixture);
  }
  result += `\n📡 [Source](${update.source})\n`;
  return result;
}
