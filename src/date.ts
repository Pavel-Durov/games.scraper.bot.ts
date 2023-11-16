import { parse } from 'date-fns';
export function parseDate(dateString: string) {
  return parse(dateString, 'EEE MMM d - HH:mm', new Date());
}
