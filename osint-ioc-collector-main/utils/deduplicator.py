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

    if new.get('threat_type') and not existing.get('threat_type'):
        merged['threat_type'] = new['threat_type']

    existing_tags = set(existing.get('tags', '').split(',')) if existing.get('tags') else set()
    new_tags = set(new.get('tags', '').split(',')) if new.get('tags') else set()
    all_tags = existing_tags.union(new_tags)
    if all_tags:
        merged['tags'] = ','.join(sorted(filter(None, all_tags)))

    existing_sources = set(existing.get('source', '').split(','))
    new_source = new.get('source', '')
    if new_source and new_source not in existing_sources:
        existing_sources.add(new_source)
        merged['source'] = ','.join(sorted(existing_sources))

    if new.get('raw_data'):
        merged['raw_data'] = new['raw_data']

    return merged
