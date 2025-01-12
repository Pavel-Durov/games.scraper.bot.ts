import { parse, format } from 'date-fns';

export function parseDate(dateString: string) {
  return parse(dateString, 'EEE MMM d - HH:mm', new Date());
}

export function formatDate(date: Date): string {
  return format(date, 'EEE MMM d - HH:mm');
}

export function formatDateWithYear(date: Date): string {
  return format(date, 'EEE MMM d - HH:mm (yyyy)');
}
export function isToday(date: Date, today: Date): boolean {
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
}
