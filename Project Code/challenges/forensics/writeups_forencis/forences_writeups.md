# F1 – Echoes in the Binary

Run `strings f1_basic_strings.bin | grep DNCTF`.
You should see `DNCTF{binary_whispers}` – submit it as flag.

# F2 – Eyes of the Shinigami

Use `exiftool f2_image_meta.jpg` or `strings f2_image_meta.jpg | grep DNCTF`.
The description contains `DNCTF{meta_shinigami}`.

# F3 – Hidden in Plain Sight

Use `binwalk -e f3_stego.jpg` or `strings f3_stego.jpg | grep DNCTF`.
The appended data reveals `DNCTF{hidden_in_plain_sight}`.

# F4 – Whispers on the Wire

Open `f4_network.pcap` with a text viewer.
The HTTP body shows `DNCTF{pcap_unmasked}`.

# F5 – DNS of the Dead

Open `f5_dns.pcap`. Each DNS query encodes 4 characters of the flag.
Read chunks in order and reconstruct `DNCTF{dns_whispered_secrets}`.

# F05 - log contains flag
line 242750 contains base64 string, decrypt two times base 64 as hint was mentioned The flag's pattern is likely designed to be missed by a simple and an important also a consistant ip:250
to only search for plus the fake flag hints.

# F6 – Footprints of Kira

Open `f6_logs.txt`. At the bottom analyst note shows `stolen_flag=DNCTF{k1ra_trace_uncovered}`.

# f7 - shadows of DNS 

filter: dns and dns.qry.name contains "covert-c2" 