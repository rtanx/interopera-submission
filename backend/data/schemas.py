from typing import List, Dict
from pydantic import BaseModel


class Deal(BaseModel):
    client: str
    value: int
    status: str


class Client(BaseModel):
    name: str
    industry: str
    contact: str


class SalesRep(BaseModel):
    id: int
    name: str
    role: str
    region: str
    skills: List[str]
    deals: List[Deal]
    clients: List[Client]

    def total_closed_won(self) -> float:
        """Calculate the total value of closed won deals."""
        return sum(deal.value for deal in self.deals if deal.status == "Closed Won")

    def deals_by_status(self, status: str) -> List[Deal]:
        """Get deals by their status."""
        return [deal for deal in self.deals if deal.status == status]

    def get_deals_value_by_status(self, status: str) -> int:
        """Get total value of deals by their status."""
        return sum(deal.value for deal in self.deals if deal.status == status)

    def deal_count_by_status(self) -> Dict[str, int]:
        """Count deals by status."""
        counts = {}
        for deal in self.deals:
            counts[deal.status] = counts.get(deal.status, 0) + 1

        return counts

    def win_rate(self) -> float:
        """Calculate the win percentage."""
        statuses = self.deal_count_by_status()
        closed_won = statuses.get("Closed Won", 0)
        closed_lost = statuses.get("Closed Lost", 0)
        total = closed_won + closed_lost
        if total == 0:
            return 0.0
        return closed_won / total * 100


class SalesData(BaseModel):
    salesReps: List[SalesRep]
