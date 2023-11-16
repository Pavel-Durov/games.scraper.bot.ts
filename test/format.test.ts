import { describe, expect, it } from '@jest/globals';
import { fixturesToRichText } from '../src/format';
describe('Fixtures format', () => {
  it('expect no games', () => {
    expect(
      fixturesToRichText({
        fixtures: [],
        date: new Date(),
        venue: 'Emirates Stadium'
      })
    ).toBe('*No upcoming games for the year*\n');
  });
  it('expect single game', () => {
    expect(
      fixturesToRichText({
        date: new Date('2021-01-01'),
        venue: 'Emirates Stadium',
        fixtures: [
          {
            date: new Date('2021-01-01'),
            venue: 'Emirates Stadium',
            leage: 'Premier League'
          }
        ]
      })
    ).toBe('*Games at Emirates Stadium for this year*\n\n*Fri Jan 1 - 00:00* - _Premier League_\n');
  });
});
