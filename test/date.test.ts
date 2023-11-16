import { describe, expect, it } from '@jest/globals';
import { formatDate, parseDate } from '../src/date';

describe('date', () => {
  it('formatDate', () => {
    expect(formatDate(new Date('2023-11-16T15:40:00.980Z'))).toBe('Thu Nov 16 - 15:40');
  });
});
