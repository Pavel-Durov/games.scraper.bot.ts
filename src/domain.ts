export interface Fixture {
  date: Date;
  venue: string;
  leage: string;
  homeTeam: string;
  awayTeam: string;
}

export interface FixturesUpdate {
  date: Date;
  venue: string;
  fixtures: Fixture[];
  source: string;
}
