from jobs.fetch_team_stats import DataFetcher


def main_function():
    test_obj = DataFetcher()
    test_obj.fetchAndWritePLTeamStats()

if __name__ == "__main__":
    main_function()