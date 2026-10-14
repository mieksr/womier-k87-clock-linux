# Screen-clock protocol (Womier K87 / QK87)

Found by capturing the official Windows tool (`DeviceDriver.exe`, "Womier K87" / "Womier QK87") talking to
the keyboard with usbmon, while it ran in a Windows VM with the keyboard passed through. Nothing here
comes from the vendor's source code, and no vendor files are included in this repository.

## Device

The keyboard in wired mode shows up as two USB devices:

| ID | Role |
|---|---|
| `fffe:0087` | QMK/VIA, keys and lighting |
| `0c45:800b` (SONiX) | screen controller, the one this tool talks to |

`0c45:800b` has four HID interfaces:

| Interface | Use |
|---|---|
| 0 | boot keyboard (Linux exposes it as `hidraw`) |
| 1 | consumer / mouse / keyboard reports |
| 2 | vendor channel, 64 B in / 4096 B out (image and GIF upload) |
| **3** | **screen commands, 1 interrupt-OUT endpoint (0x06); `usbhid` does not bind it, so there is no `hidraw` node** |

Because interface 3 has no `hidraw` node, sending the clock to interface 0 (as a first guess from reading the
vendor binary suggests) is accepted by the USB stack and silently ignored by the firmware.

## Sequence

Four USB control transfers to interface 3, each followed by a read of the reply (about 36 ms apart):

- Request type `0x21`, request `0x09` (SET_REPORT), `wValue = 0x0300` (feature report, ID 0),
  `wIndex = 3`, `wLength = 64`, no report-ID prefix in the data.
- Then `0xA1` / `0x01` (GET_REPORT), `wValue = 0x0300`, `wIndex = 3`, 64 bytes.

Payloads (64 bytes each, unlisted bytes are zero):

| # | Bytes |
|---|---|
| 1 | `04 18` |
| 2 | `04 28`, byte 8 = `01` |
| 3 | clock, see below |
| 4 | `04 02` |

### Clock payload

| Offset | Value |
|---|---|
| 0 | `00` |
| 1 | `00` |
| 2 | `5A` |
| 3 | year − 2000 (plain number, not BCD) |
| 4 | month 1–12 |
| 5 | day of month |
| 6 | hour 0–23 |
| 7 | minute |
| 8 | second |
| 9 | `00` |
| 10 | weekday, Sunday = 0 |
| 62–63 | `AA 55` |

Example, captured at 2026-10-14 10:07:48 (Wednesday):
`00 00 5a 1a 0a 0e 0a 07 30 00 03 … aa 55`

## Not known

- Whether byte 1 (always `00` in the capture) selects a display page on other firmware.
- Behaviour over the 2.4 GHz receiver and Bluetooth. The screen controller is not on the USB bus in those modes.
- The keyboard's clock does not appear to survive power-off.
