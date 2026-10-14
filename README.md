# womier-k87-clock-linux

Set the screen clock on the **Womier K87 / QK87** keyboard from Linux. Womier's tool is Windows-only; this is a small
Python script that sends the same USB commands. It has no dependencies and can sync automatically when you plug the keyboard in.

> Unofficial. Not affiliated with or endorsed by Womier. No vendor software is included or needed.

## Does it work for my keyboard?

Tested on one **Womier QK87** (TKL, wireless, with the mini screen), connected by USB cable. It should also work for the K87,
which uses the same screen utility and hardware. Check that this shows a `0c45:800b` entry named WOMIER-K87 Gaming Keyboard:

```sh
grep -l 0c45 /sys/bus/usb/devices/*/idVendor | xargs -n1 dirname | xargs -I{} sh -c 'echo {}: $(cat {}/idProduct) $(cat {}/product)'
```

If your keyboard has a different ID or no screen, please open an issue (see below).

## Requirements

- Linux with Python 3.6+
- The keyboard connected with a **USB cable**, mode switch set to **USB (wired)**

## Install

Arch / Omarchy (AUR):

```sh
yay -S womier-k87-clock-linux     # or paru / your AUR helper
```

Any distro:

```sh
git clone https://github.com/mieksr/womier-k87-clock-linux
cd womier-k87-clock-linux
sudo ./install.sh
```

This installs `womier-clock-sync`, a udev rule and a systemd service. The rule lets the logged-in user talk to the
keyboard's screen controller without sudo. The service sets the clock whenever the keyboard is plugged in.
Remove it again with `sudo ./uninstall.sh`.

## Use

```sh
womier-clock-sync                      # set the screen to the current local time
womier-clock-sync --dry-run            # print the packets, send nothing
womier-clock-sync --at 2026-10-14T03:33:33   # set a test time to check it works
```

Without the udev rule, run it with `sudo`.

## Limits

- **Wired mode only.** In 2.4 GHz or Bluetooth mode the screen controller isn't on the USB bus. To sync, plug in the
  cable for a few seconds, then switch back.
- The screen clock doesn't seem to keep time across power-off (the manual doesn't promise it), so you may need to sync again.
- Tested on one unit. Other firmware revisions might behave differently.

## Troubleshooting

- **`not found`**: the keyboard is in wireless mode, or the cable is power-only.
- **`No permission`**: install the udev rule (`sudo ./install.sh`), unplug and replug, or use `sudo`.
- **`Interface 3 is in use`**: another program has the device open. Close the vendor tool, any VM, or `qmk`/`vial` tools.
- **Command succeeds but the screen doesn't change**: open an issue with your keyboard model and the output of
  `lsusb -v -d 0c45:800b`.

## How it was found

The vendor tool doesn't work under Wine, because Wine hides this keyboard's boot interface. So the tool was run in a
Windows VM with the keyboard passed through, and its USB traffic was captured with usbmon. The clock isn't sent to the
interface that Linux exposes as `hidraw`. It goes to a fourth interface that `usbhid` doesn't bind. Details are in
[docs/PROTOCOL.md](docs/PROTOCOL.md).

## Reporting a problem

Please include: keyboard model (K87 / QK87 / other Womier), whether it has a screen, the output of `lsusb -d 0c45:800b -v`,
and what the screen shows after running `womier-clock-sync --at 2026-10-14T03:33:33`.

## License

MIT, see [LICENSE](LICENSE).
