# Sistem Tempahan Fasiliti MPC Wilayah Utara

Portal Bahasa Melayu untuk permohonan dewan, bilik latihan dan penginapan MPC Wilayah Utara.

Portal awam: https://tempahan-mpc-wilayah-utara.groupmpc-0630.chatgpt.site

Dashboard showcase: https://tempahan-mpc-wilayah-utara.groupmpc-0630.chatgpt.site/dashboard

## Fungsi prototaip

- Katalog fasiliti, gambar dan kadar berasaskan brosur.
- Beberapa fasiliti, termasuk dewan bersama asrama lelaki dan perempuan, dalam satu permohonan.
- Anggaran kos mengikut pakej, hari, bilik, malam dan caj tambahan yang tersedia.
- Kalendar ketersediaan awam serta halaman pentadbir untuk tarikh dan baki bilik.
- Maklumat pemohon dan perakuan persetujuan.
- Draf emel kepada zamri@mpc.gov.my serta cetak atau simpan ringkasan sebagai PDF.
- Dashboard interaktif dengan data simulasi Jan–Jun 2026, penapis dan senarai terperinci.

Pemohon perlu menekan Hantar dalam aplikasi emel sendiri. Tiada penghantaran emel pelayan, kutipan bayaran atau kelulusan automatik. PDF merupakan salinan permohonan. Pemilihan tarikh tidak mengunci inventori; status masih tersedia tertakluk pengesahan rasmi MPC. Data dashboard ialah simulasi, bukan rekod hasil sebenar.

## Jalankan pada komputer sendiri

Keperluan: Node.js 20 atau lebih baharu dan Python 3, tanpa pakej npm tambahan.

```sh
npm run build
npm test
npm run dev
```

Buka http://127.0.0.1:4173. Pelayan pratonton menyediakan akses pentadbir simulasi pada komputer setempat dan menyimpan kalendar ujian dalam `.sites-runtime/`. Jangan dedahkan pelayan pembangunan ini kepada internet.

## Struktur kod

- `content/` — halaman, gaya, logik borang, katalog dan data dashboard simulasi.
- `assets/` — logo MPC, ilustrasi hero dan gambar fasiliti.
- `content/server.js.txt` — backend asal Sites dengan storan `BUCKET` dan identiti yang dibekalkan platform Sites.
- `scripts/assemble.py` — menjana bundle `worker/index.js` daripada sumber dan aset.
- `scripts/check.mjs` — semakan pentadbir, Origin, inventori dan konflik versi.
- `cloudflare/server.js.txt` — penyesuai Cloudflare untuk portal awam.
- `cloudflare/build.py` dan `cloudflare/wrangler.jsonc` — membina bundle Cloudflare.

## Deployment Cloudflare

Jalankan `npm run build`, kemudian deploy `cloudflare/worker.js` menggunakan konfigurasi `cloudflare/wrangler.jsonc` pada akaun Cloudflare yang disahkan. Contoh CLI selepas Wrangler dipasang dan akaun dilog masuk:

```sh
wrangler deploy --config cloudflare/wrangler.jsonc
```

Penyesuai Cloudflare membaca kalendar daripada portal awam asal dan mengalihkan halaman pentadbir ke portal Sites asal. Ia tidak memindahkan storan, pengesahan pengguna atau pentadbiran ke Cloudflare. Backend asal dalam `worker/index.js` mempercayai identiti daripada platform Sites dan tidak sesuai dideploy terus pada pelayan awam tanpa lapisan pengesahan yang dipercayai.

Kod dalam repositori ini belum bermaksud deployment awam baharu telah dilakukan. GitHub Pages sahaja tidak menjalankan backend Worker atau API pentadbir ini.

## Penyelenggaraan

Kadar dan kapasiti berada dalam `content/catalog.json`; sahkan dengan NRO sebelum operasi sebenar. Jalankan build semula selepas mengubah sumber. Data showcase boleh dijana semula dengan `python3 scripts/generate-showcase.py`. Jangan masukkan data peribadi pemohon, kalendar operasi, kata laluan atau token ke repositori awam.
