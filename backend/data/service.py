from typing import Optional, List, Dict, Any
import json
from functools import lru_cache
from pathlib import Path

from .schemas import SalesRep, SalesData


class SalesRepService:
    """Service class to handle sales representative data operations"""

    def __init__(self, data_file_path: str = "sales_data.json"):
        """
        Initialize the service with the path to the JSON data file

        Args:
            data_file_path: Path to the JSON data file
        """
        self.data_file_path = data_file_path
        self._data = self._load_data()

    @lru_cache(maxsize=1)
    def _load_data(self) -> SalesData:
        """
        Load data from JSON file and parse it into Pydantic models
        Returns cached results after first call

        Returns:
            SalesRep: Parsed data in Pydantic model
        """
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return SalesData(**data)
        except FileNotFoundError:
            raise Exception(f"Data file not found: {self.data_file_path}")
        except json.JSONDecodeError:
            raise Exception(
                f"Invalid JSON in data file: {self.data_file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def get_all_sales_reps(self) -> List[SalesRep]:
        """
        Get all sales representatives

        Returns:
            List[SalesRep]: List of all sales representatives
        """
        return self._data.salesReps

    def get_sales_rep_by_id(self, rep_id: int) -> Optional[SalesRep]:
        """
        Get a sales representative by ID

        Args:
            rep_id: ID of the sales representative to find

        Returns:
            Optional[SalesRep]: Sales representative with the given ID or None if not found
        """
        for rep in self._data.salesReps:
            if rep.id == rep_id:
                return rep
        return None

    def get_sales_reps_by_region(self, region: str) -> List[SalesRep]:
        """
        Get all sales representatives in a specific region

        Args:
            region: Region to filter by

        Returns:
            List[SalesRep]: List of sales representatives in the specified region
        """
        return [rep for rep in self._data.salesReps if region.lower() in rep.region.lower()]

    def get_sales_reps_by_skill(self, skill: str) -> List[SalesRep]:
        """
        Get all sales representatives who have a specific skill

        Args:
            skill: Skill to filter by

        Returns:
            List[SalesRep]: List of sales representatives with the specified skill
        """
        return [rep for rep in self._data.salesReps if skill.lower() in [s.lower() for s in rep.skills]]

    def get_deals_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all deals with a specific status, including rep information

        Args:
            status: Deal status to filter by

        Returns:
            List[Dict]: List of deals with rep information
        """
        deals = []
        for rep in self._data.salesReps:
            for deal in rep.deals:
                if deal.status == status:
                    deals.append({
                        "rep_id": rep.id,
                        "rep_name": rep.name,
                        "deal": deal
                    })
        return deals

    def get_reps_with_deals_above_value(self, value: int) -> List[SalesRep]:
        """
        Get all sales representatives who have at least one deal above the specified value

        Args:
            value: Minimum deal value to filter by

        Returns:
            List[SalesRep]: List of sales representatives with deals above the specified value
        """
        return [
            rep for rep in self._data.salesReps
            if any(deal.value > value for deal in rep.deals)
        ]

    def get_rep_performance_summary(self) -> List[Dict[str, Any]]:
        """
        Get a summary of each rep's performance

        Returns:
            List[Dict]: List of performance summaries
        """
        summaries = []
        for rep in self._data.salesReps:
            total_value = sum(
                deal.value for deal in rep.deals if deal.status == "Closed Won")
            won_deals = sum(
                1 for deal in rep.deals if deal.status == "Closed Won")
            lost_deals = sum(
                1 for deal in rep.deals if deal.status == "Closed Lost")
            in_progress = sum(
                1 for deal in rep.deals if deal.status == "In Progress")

            summaries.append({
                "rep_id": rep.id,
                "rep_name": rep.name,
                "region": rep.region,
                "total_value_won": total_value,
                "won_deals": won_deals,
                "lost_deals": lost_deals,
                "in_progress_deals": in_progress,
                "client_count": len(rep.clients)
            })

        return summaries


def get_sales_rep_service() -> SalesRepService:
    """
    Get an instance of the SalesRepService

    Returns:
        SalesRepService: Instance of the service
    """
    return SalesRepService(Path(__file__).parent / "mock/dummyData.json")
