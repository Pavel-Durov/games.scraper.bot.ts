"""Tests for HTML parsing and scraping functionality."""

import sys
from datetime import datetime

sys.path.insert(0, "src")

from scrape import parse_fixtures


def test_parse_single_fixture():
    """Test parsing a single valid fixture."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    fixture = fixtures[0]
    assert fixture.home_team == "Arsenal"
    assert fixture.away_team == "Chelsea"
    assert fixture.venue == "Emirates Stadium"
    assert fixture.league == "Premier League"
    assert fixture.date.month == 12
    assert fixture.date.day == 16


def test_parse_multiple_fixtures():
    """Test parsing multiple fixtures."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Wed Dec 20 - 20:00</div>
            <div class="event-info__venue">Stamford Bridge</div>
            <div class="event-info__extra">Carabao Cup</div>
        </div>
        <div class="team-crest__name-value">Chelsea</div>
        <div class="team-crest__name-value">Arsenal</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 2
    assert fixtures[0].home_team == "Arsenal"
    assert fixtures[0].away_team == "Chelsea"
    assert fixtures[0].venue == "Emirates Stadium"
    assert fixtures[1].home_team == "Chelsea"
    assert fixtures[1].away_team == "Arsenal"
    assert fixtures[1].venue == "Stamford Bridge"


def test_parse_fixture_with_only_home_team():
    """Test parsing fixture with only home team."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal"
    assert fixtures[0].away_team is None
    assert fixtures[0].venue == "Emirates Stadium"


def test_parse_fixture_with_no_teams():
    """Test parsing fixture with no team information."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team is None
    assert fixtures[0].away_team is None
    assert fixtures[0].venue == "Emirates Stadium"
    assert fixtures[0].league == "Premier League"


def test_parse_fixture_with_missing_venue():
    """Test parsing fixture with missing venue."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].venue == ""
    assert fixtures[0].league == "Premier League"


def test_parse_fixture_with_missing_league():
    """Test parsing fixture with missing league info."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].league == ""
    assert fixtures[0].venue == "Emirates Stadium"


def test_parse_fixture_with_missing_date():
    """Test parsing fixture with missing date (should use current date)."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    # Date should default to now
    assert isinstance(fixtures[0].date, datetime)


def test_parse_fixture_with_whitespace():
    """Test parsing fixture with extra whitespace in text."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">  Sat Dec 16 - 15:40  </div>
            <div class="event-info__venue">  Emirates Stadium  </div>
            <div class="event-info__extra">  Premier League  </div>
        </div>
        <div class="team-crest__name-value">  Arsenal  </div>
        <div class="team-crest__name-value">  Chelsea  </div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal"
    assert fixtures[0].away_team == "Chelsea"
    assert fixtures[0].venue == "Emirates Stadium"
    assert fixtures[0].league == "Premier League"


def test_parse_empty_html():
    """Test parsing empty HTML."""
    html = ""
    fixtures = parse_fixtures(html)
    assert len(fixtures) == 0


def test_parse_html_with_no_fixtures():
    """Test parsing HTML with no fixture cards."""
    html = """
    <html>
        <body>
            <div class="some-other-class">Not a fixture</div>
        </body>
    </html>
    """
    fixtures = parse_fixtures(html)
    assert len(fixtures) == 0


def test_parse_fixture_with_special_characters():
    """Test parsing fixture with special characters in team names."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 16 - 15:40</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal FC</div>
        <div class="team-crest__name-value">Brighton & Hove Albion</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal FC"
    assert fixtures[0].away_team == "Brighton & Hove Albion"


def test_parse_fixture_women_team():
    """Test parsing fixture with women's team."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sun Oct 12 - 14:30</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Barclays Women's Super League</div>
        </div>
        <div class="team-crest__name-value">Arsenal Women</div>
        <div class="team-crest__name-value">Chelsea Women</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal Women"
    assert fixtures[0].away_team == "Chelsea Women"
    assert fixtures[0].league == "Barclays Women's Super League"


def test_parse_fixture_uefa_competition():
    """Test parsing fixture with UEFA competition."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Tue Oct 21 - 20:00</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">UEFA Champions League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Club Atlético de Madrid</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal"
    assert fixtures[0].away_team == "Club Atlético de Madrid"
    assert fixtures[0].league == "UEFA Champions League"


def test_parse_complex_html_structure():
    """Test parsing with nested HTML structure."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info">
                <div class="event-info__date">
                    <span>Sat Dec 16 - 15:40</span>
                </div>
                <div class="event-info__venue">
                    <span>Emirates Stadium</span>
                </div>
                <div class="event-info__extra">
                    <span>Premier League</span>
                </div>
            </div>
        </div>
        <div class="team-info">
            <div class="team-crest__name-value">Arsenal</div>
        </div>
        <div class="team-info">
            <div class="team-crest__name-value">Chelsea</div>
        </div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 1
    # Should handle nested spans correctly
    assert fixtures[0].venue == "Emirates Stadium"


def test_parse_fixture_card_without_header():
    """Test parsing fixture card that has no header section."""
    html = """
    <div class="fixture-card">
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Chelsea</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    # Should still create a fixture but with minimal info
    assert len(fixtures) == 1
    assert fixtures[0].home_team == "Arsenal"
    assert fixtures[0].away_team == "Chelsea"
    assert fixtures[0].venue == ""
    assert fixtures[0].league == ""
    assert isinstance(fixtures[0].date, datetime)


def test_parse_fixtures_maintains_order():
    """Test that parsed fixtures maintain their order."""
    html = """
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 1 - 15:00</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Team A</div>
    </div>
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 8 - 15:00</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Team B</div>
    </div>
    <div class="fixture-card">
        <div class="card__header">
            <div class="event-info__date">Sat Dec 15 - 15:00</div>
            <div class="event-info__venue">Emirates Stadium</div>
            <div class="event-info__extra">Premier League</div>
        </div>
        <div class="team-crest__name-value">Arsenal</div>
        <div class="team-crest__name-value">Team C</div>
    </div>
    """
    fixtures = parse_fixtures(html)

    assert len(fixtures) == 3
    assert fixtures[0].away_team == "Team A"
    assert fixtures[1].away_team == "Team B"
    assert fixtures[2].away_team == "Team C"
