from pydantic import BaseModel

from schemas.daily_quote import DailyQuoteResponse


class DashboardResponse(BaseModel):

    total_quotes: int

    total_authors: int

    total_comments: int

    total_views: int

    total_reports: int

    total_ratings: int

    average_rating: float

    quote_of_the_day: DailyQuoteResponse