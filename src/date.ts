import { parse, format } from 'date-fns';
export function parseDate(dateString: string) {
  return parse(dateString, 'EEE MMM d - HH:mm', new Date());
}

export function formatDate(date: Date): string {
  return format(date, 'EEE MMM d - HH:mm');
}
