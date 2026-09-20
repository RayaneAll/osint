from datetime import datetime


def is_duplicate(ioc_value, db):
    """
    Check if an IOC already exists in the database.

    Args:
        ioc_value: The IOC value to check
        db: IOCDatabase instance

    Returns:
        Boolean indicating if the IOC exists
    """
    existing = db.get_ioc_by_value(ioc_value)
    return existing is not None


def merge_ioc_data(existing, new):
    """
    Merge new IOC data with existing record.

    Args:
        existing: Existing IOC dict from database
        new: New IOC dict from feed

    Returns:
        Merged IOC dict
    """
    merged = existing.copy()

    merged['last_seen'] = new.get('last_seen', datetime.utcnow().isoformat())
    merged['updated_at'] = datetime.utcnow().isoformat()

    return merged
