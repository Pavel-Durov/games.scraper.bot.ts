import { describe, expect, it } from '@jest/globals';
import { formatDate, parseDate, isToday } from '../src/date';

describe('date', () => {
  it('formatDate', () => {
    expect(formatDate(new Date('2023-11-16T15:40:00.980Z'))).toBe('Thu Nov 16 - 15:40');
  });
});

describe('isToday', () => {
  it('isToday', () => {
    expect(isToday(new Date('2023-11-16T15:40:00.980Z'), new Date('2023-11-16T15:40:00.980Z'))).toBe(true);
    expect(isToday(new Date('2023-11-16T15:40:00.980Z'), new Date('2023-11-17T15:40:00.980Z'))).toBe(false);
  });
});
