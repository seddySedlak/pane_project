## Why We Switched from ESP32 to Raspberry Pi 🤖➡️🍓

In the `old_esp32_code.py` file, we wrote code to send G-code commands to the Prusa MK3S 3D printer. 🖨️

We sent all the required G-code commands, but the printer kept sending back raw binary data, like the sample shown below: 🧩💾

### Sample of Raw UART Data Received from the Printer 📡

`````
b"\x00\x00\x00\xde\x00\x00\x00\x00\x00\x00\x00\xc0\xf7\x6d\x00\x00\x00\x92\xb8\x02\x04
x00\x80\xfe\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x80\xff\x03\x00\x00\x00\x00\x00\x00
xff\x5c\x02\x00\x00\x00\x00\x00\x00\xfc\x00\x00\x00\x80\xc0\x01\x00\x00\x00\x00\x00
xfe\x02\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\xff\x0c\x00\x00\x00
x00\x00\x00\x00\x00\x00\x00\xff\xc7\x00\x00\x00\x00\x00\x00\x80\xcf\x02\x00\x04\x00
x00\xa0\x00\x00\x00\x00\x00"
`````

We were not sure what this data represented and tried various decoding methods, including all known protocols such as ASCII, various UTF encodings (UTF-8, UTF-16, etc.), and others, but without success. 🤔

After a lot of investigation, we found that most likely the UART port we connected to is not the main communication interface with the printer. Instead, it was an internal UART channel used for communication between the printer's motherboard and its display. 🖥️🔄🖥️

Because of this, the data we received was a binary stream intended for the display, not meaningful status messages. 🚫

Due to this limitation, we decided to switch our project platform from ESP32 to Raspberry Pi, which provided more flexibility for communication and data processing.

---

If you want, we can explore other ways to communicate with the printer or improve the Raspberry Pi implementation. 🚀
