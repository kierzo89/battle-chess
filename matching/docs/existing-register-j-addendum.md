# Final existing-local register control: inner counter j

The remaining live local `j` in retired init_rays9840 was independently qualified as register under unchanged pinned C5.00 AS/Zi. No local, type, helper or operation was added. This emits a complete187-byte CV procedure /188-byte CODE segment, with an8-byte frame and the existing SI/DI saves, versus original185 bytes. There are142 complete comparison differences. Both emitted and original MZ sets are empty. No matching credit is restored.

This completes the three individual existing-live-value controls: direction_index183 bytes, entry189 bytes andj187 bytes. All three produce frame8 rather than baseline6, but none matches original185. No combinations or additional variants were attempted. The earlier four-control proof remains frozen and unchanged.

Complete source, compiler log/command/tool pins, object hash, full CODE/CV/linked/original bytes, all raw/resolved fixups and differing positions are retained separately in `evidence/existing-register-j-frame-addendum.json`. Reproducer: `build/existing-register-j-control/probe.py`. Retained original REA is reused; no new session was opened. Canonical source, registry, core and tests remain untouched.
