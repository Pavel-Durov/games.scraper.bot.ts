import { formatDate, isToday, formatDateWithYear } from './date';
import { FixturesUpdate } from './domain';

export function fixturesToRichText(update: FixturesUpdate): string {
  let result = `📟 *Update for ${formatDateWithYear(update.date)}*\n`;
  if (update.fixtures === undefined || update.fixtures.length === 0) {
    result += '*No upcoming games for the year*\n';
  } else {
    result += `⚽ *Games at ${update.venue} for this year*\n\n`;
    for (const fixture of update.fixtures) {
      if (isToday(fixture.date)) {
        result += `Today 👉 *${formatDate(fixture.date)}* - _${fixture.leage}_\n`;
      } else {
        result += `*${formatDate(fixture.date)}* - _${fixture.leage}_\n`;
      }
    }
  }
  return result;
}
