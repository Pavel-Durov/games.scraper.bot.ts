import { createLogger, transports, format, Logger } from 'winston';
import { LOG_LEVEL } from './config';

export function initLog(label: string): Logger {
  const logFormat = format.printf(({ level, timestamp, message, label }) => {
    return `${timestamp} [${label}] ${level}: ${message}`;
  });
  const logger = createLogger({
    level: LOG_LEVEL,
    format: format.combine(format.timestamp(), format.label({ label }), logFormat),
    transports: [new transports.Console()]
  });
  return logger;
}
