export interface Fixture {
  date: Date;
  venue: string;
  leage: string;
}

export interface FixturesUpdate {
  date: Date;
  venue: string;
  fixtures: Fixture[];
}
