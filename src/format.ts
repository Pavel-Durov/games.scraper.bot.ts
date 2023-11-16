import { formatDate } from './date';
import { FixturesUpdate } from './domain';

export function fixturesToRichText(update: FixturesUpdate): string {
  if (update.fixtures === undefined || update.fixtures.length === 0) {
    return '*No upcoming games for the year*\n';
  }
  let result = `*Games at ${update.venue} for this year*\n\n`;
  for (const fixture of update.fixtures) {
    result += `*${formatDate(fixture.date)}* - _${fixture.leage}_\n`;
  }
  return result;
}
