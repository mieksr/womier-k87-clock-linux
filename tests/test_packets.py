import importlib.machinery
import importlib.util
import unittest
from datetime import datetime
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "womier-clock-sync"
loader = importlib.machinery.SourceFileLoader("womier_clock_sync", str(SCRIPT))
spec = importlib.util.spec_from_loader("womier_clock_sync", loader)
w = importlib.util.module_from_spec(spec)
loader.exec_module(w)

# Clock packet captured from the vendor app at 2026-10-14 10:07:48 (Wednesday)
CAPTURED_CLOCK = bytes.fromhex(
    "00005a1a0a0e0a07300003000000000000000000000000000000000000000000"
    "000000000000000000000000000000000000000000000000000000000000aa55")


class Packets(unittest.TestCase):
    def test_clock_packet_matches_vendor_capture(self):
        self.assertEqual(w.build_packets(datetime(2026, 10, 14, 10, 7, 48))[2], CAPTURED_CLOCK)

    def test_sequence_and_sizes(self):
        p = w.build_packets(datetime(2026, 1, 2, 3, 4, 5))
        self.assertEqual([len(x) for x in p], [64] * 4)
        self.assertEqual(p[0][:2], b"\x04\x18")
        self.assertEqual(p[1][:2] + bytes([p[1][8]]), b"\x04\x28\x01")
        self.assertEqual(p[3][:2], b"\x04\x02")

    def test_weekday_sunday_is_zero(self):
        self.assertEqual(w.build_packets(datetime(2026, 10, 11))[2][10], 0)   # Sunday
        self.assertEqual(w.build_packets(datetime(2026, 10, 12))[2][10], 1)   # Monday
        self.assertEqual(w.build_packets(datetime(2026, 10, 17))[2][10], 6)   # Saturday

    def test_year_range(self):
        with self.assertRaises(ValueError):
            w.build_packets(datetime(1999, 1, 1))

    def test_usbfs_ioctl_numbers(self):
        if w.struct.calcsize("P") == 8:
            self.assertEqual(w.USBDEVFS_CONTROL, 0xC0185500)
        self.assertEqual(w.USBDEVFS_CLAIMINTERFACE, 0x8004550F)
        self.assertEqual(w.USBDEVFS_RELEASEINTERFACE, 0x80045510)


if __name__ == "__main__":
    unittest.main()
