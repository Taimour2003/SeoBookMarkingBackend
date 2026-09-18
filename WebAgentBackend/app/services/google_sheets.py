import gspread

from app.config import settings


# def get_google_client():
#     gc = gspread.service_account(filename=str(settings.google_service_account_file))
#     return gc

# def fetch_bookmarking_urls():
#     gc = get_google_client()
#     sheet = gc.open_by_key(settings.bookmarking_sheet_id).worksheet(settings.bookmarking_sheet_name)
#     urls = sheet.col_values(1)  # Assuming URLs are in the first column
#     return urls


def get_sheets_client() -> gspread.Client:
    """Google Sheets client ko return karein."""
    gc = gspread.service_account_from_dict(settings.google_service_account_file_path)
    return gc
