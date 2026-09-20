#!/usr/bin/env python3
"""
Simple system tests for IOC Collector.
Run with: python3 test_system.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from utils import setup_logger, is_duplicate, merge_ioc_data
        from storage import IOCDatabase
        from collectors import (
            FeodoCollector, URLhausCollector,
            MalwareBazaarCollector, SpamhausCollector
        )
        from normalizers import (
            normalize_ip, normalize_domain, normalize_hash, normalize_url,
            validate_ip, validate_domain, validate_hash, validate_url
        )
        from exporters import CSVExporter, JSONExporter
        from scheduler import JobScheduler
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_normalizers():
    """Test normalization functions."""
    print("\nTesting normalizers...")
    from normalizers import (
        normalize_ip, normalize_domain, normalize_hash, normalize_url
    )

    tests = [
        (normalize_ip("192.168.1.1"), "192.168.1.1", "IP normalization"),
        (normalize_domain("Example.COM"), "example.com", "Domain normalization"),
        (normalize_hash("a"*32)[0], "a"*32, "MD5 hash normalization"),
        (normalize_url("http://example.com"), "http://example.com", "URL normalization"),
    ]

    passed = 0
    for result, expected, desc in tests:
        if result == expected:
            print(f"✓ {desc}")
            passed += 1
        else:
            print(f"✗ {desc}: got {result}, expected {expected}")

    return passed == len(tests)


def test_validators():
    """Test validation functions."""
    print("\nTesting validators...")
    from normalizers.validators import (
        validate_ip, validate_domain, validate_hash, validate_url
    )

    tests = [
        (validate_ip("192.168.1.1"), True, "Valid IPv4"),
        (validate_ip("invalid"), False, "Invalid IP"),
        (validate_domain("example.com"), True, "Valid domain"),
        (validate_domain("not..valid"), False, "Invalid domain"),
        (validate_hash("a"*32, "md5"), True, "Valid MD5"),
        (validate_hash("short", "md5"), False, "Invalid MD5"),
        (validate_url("http://example.com"), True, "Valid URL"),
        (validate_url("not-a-url"), False, "Invalid URL"),
    ]

    passed = 0
    for result, expected, desc in tests:
        if result == expected:
            print(f"✓ {desc}")
            passed += 1
        else:
            print(f"✗ {desc}: got {result}, expected {expected}")

    return passed == len(tests)


def test_database():
    """Test database operations."""
    print("\nTesting database...")
    from storage import IOCDatabase
    from datetime import datetime
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db = IOCDatabase(db_path)
        db.initialize_schema()

        test_ioc = {
            'ioc_value': '192.168.1.100',
            'ioc_type': 'ip',
            'threat_type': 'test',
            'source': 'test_source',
            'first_seen': datetime.utcnow().isoformat(),
            'last_seen': datetime.utcnow().isoformat()
        }

        ioc_id, is_new = db.insert_ioc(test_ioc)
        print(f"✓ IOC insertion (new={is_new})")

        retrieved = db.get_ioc_by_value('192.168.1.100')
        if retrieved:
            print("✓ IOC retrieval")
        else:
            print("✗ IOC retrieval failed")
            return False

        all_iocs = db.get_all_active_iocs()
        print(f"✓ Active IOCs query (count={len(all_iocs)})")

        stats = db.get_statistics()
        print(f"✓ Statistics generation (active={stats['total_active_iocs']})")

        db.close()
        return True

    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


def test_exporters():
    """Test export functionality."""
    print("\nTesting exporters...")
    from exporters import CSVExporter, JSONExporter
    from datetime import datetime
    import tempfile
    import os

    tmp_dir = tempfile.mkdtemp()

    try:
        test_iocs = [
            {
                'ioc_value': '192.168.1.1',
                'ioc_type': 'ip',
                'threat_type': 'test',
                'source': 'test',
                'first_seen': datetime.utcnow().isoformat(),
                'last_seen': datetime.utcnow().isoformat(),
                'confidence_score': 75,
                'tags': 'test'
            }
        ]

        csv_exporter = CSVExporter(tmp_dir)
        csv_file = csv_exporter.export_full(test_iocs)
        if os.path.exists(csv_file):
            print("✓ CSV export")
        else:
            print("✗ CSV export failed")
            return False

        json_exporter = JSONExporter(tmp_dir)
        json_file = json_exporter.export_full(test_iocs)
        if os.path.exists(json_file):
            print("✓ JSON export")
        else:
            print("✗ JSON export failed")
            return False

        return True

    except Exception as e:
        print(f"✗ Exporter test failed: {e}")
        return False
    finally:
        import shutil
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)


def main():
    """Run all tests."""
    print("=" * 60)
    print("IOC Collector System Tests")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Normalizers", test_normalizers),
        ("Validators", test_validators),
        ("Database", test_database),
        ("Exporters", test_exporters),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
