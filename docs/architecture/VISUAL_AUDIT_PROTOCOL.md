# Visual audit protocol

Visual acceptance uses the final running build. Automated geometry, manifest, alpha, and state tests are required supporting evidence, but they cannot replace uninterrupted gameplay.

For each affected feature, record build identity, route/section, world position, input path, viewport resolution and orientation, states/facings exercised, screenshots or sequences, source/runtime measurements, automated commands, observed defects, regression scope, and final `PASS`, `FAIL`, `INCOMPLETE`, or `CANNOT VERIFY` status.

Evidence belongs under `tools/visual-audit/evidence/` during a validation run and should be promoted into a dated tracked report when approved. Audit real gameplay at every target resolution, including transitions into and out of the changed content. Fixture scenes may diagnose a state but cannot produce release-gate `PASS` on their own.
