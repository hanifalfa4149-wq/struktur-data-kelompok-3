"""Entry point for the logistics system CLI."""

from services.logistics import LogisticsService


def main() -> None:
    """Run the main CLI menu."""
    service = LogisticsService()
    service.run()


if __name__ == "__main__":
    main()
