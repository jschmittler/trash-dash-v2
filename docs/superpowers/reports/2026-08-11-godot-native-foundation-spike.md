# Godot native foundation spike report

Assessment dates: 2026-08-11–12

User approval date: 2026-08-12

Assessment label: **SPIKE**

Final V2 release-gate status: **INCOMPLETE**

## Recommendation and approval scope

**Accept with revised scope:** use Godot 4.7.1 Standard, typed GDScript, and the
Compatibility renderer as the foundation for a macOS desktop MVP through a
meaningful working prototype.

This acceptance authorizes macOS production infrastructure, runtime
scaffolding, and prototype gameplay. It does not approve a production asset,
canonical level, complete platform matrix, signed/store package, or release.
Windows, Android, and iOS are deferred and nonblocking for the current MVP,
not permanently rejected. Linux and web are out of scope.

The macOS foundation is acceptable even though the overall SPIKE/V2 gate is
`INCOMPLETE`. The remaining macOS blockers for a future completion claim are
human packaged traversal/physical-keyboard feel, one isolated real-audio-test
exit warning, and import/validation of clean production assets.

## Clean-room boundary

The disposable implementation was built on an unmerged spike branch from main
commit `22d0f11b141316daa4bf8fbb5e3246f937a715d3`. No spike implementation,
generated spike asset, V1 code/art, archive content, production level, or
gameplay commit was promoted to `main`.

The sibling V1 repository remained read-only. The synthetic world, test tone,
and source-sheet-derived idle were test fixtures only. After this reviewed
record is safely committed and pushed, the temporary spike branch/worktree is
removed rather than merged.

## Exact assessed toolchain

| Component | Version/result |
| --- | --- |
| Godot Standard and export templates | `4.7.1.stable.official.a13da4feb` / templates `4.7.1.stable` |
| Renderer on assessed macOS host | Compatibility; OpenGL 4.1 through Metal; Apple M2 |
| Xcode | 16.4, build `16F6` |
| Java | OpenJDK 17.0.20, Homebrew build `17.0.20+0` |
| Android tools | adb protocol 1.0.41; Platform Tools 37.0.1 (`15733141`) |
| Asset-proof encoder | Pillow 12.3.0; Pillow zlib codec `1.3.1.zlib-ng`; Python zlib compile/runtime `1.2.11`/`1.2.12` |
| Historical Windows guest | Windows 11 version `10.0.22621.4317` in Parallels |

No Apple Team ID, certificate, provisioning profile, keystore, password, or
store credential was requested, guessed, or committed. The project owner now
has an Apple Developer account but chose to perform local hookup later.

## Contracts and test results

The dependency-free headless suite discovered 52 `test_` methods across eight
test scripts. The final command
`godot --headless --path <spike-project> --script res://tests/run_all.gd`
exited 0 on the assessed Godot version. Clean import/editor smoke and bounded
Compatibility-renderer boots also exited 0. The full-suite process still
reported the isolated audio-test leak described below, so the automated gate
is not `PASS`.

| Area | Evidence-backed result |
| --- | --- |
| Display | Fixed 960×540 logical world and centered 16:9 integer content rectangle; `canvas_items` + `keep`; nearest filtering. Zero, tiny, odd, wide, tall, and portrait-window policy cases were tested. |
| Input | `move_left`, `move_right`, `jump`, `dash`, `action`, and `pause` share one action router. Virtual press/hold/release, physical+virtual merge, focus/pause clearing, and exact keyboard defaults were tested. Mobile UI is enabled only for Android/iOS/mobile features and hidden on macOS/Windows. |
| Camera | Typed `FOLLOW`, `TRANSITION`, `ARENA_LOCK`, `DEFEAT_RELEASE`, and `CHECKPOINT_RECOVERY` states passed deterministic clamp, monotonicity, explicit-release, recovery, and zero/negative-delta contracts. |
| Level/collision | A typed level resource validated stable IDs, bounds, supports, and boss arena. Visual geometry and `StaticBody2D`/`CollisionShape2D` geometry used separate fields and node paths; arena scene geometry was aligned to resource coordinates. |
| Save | Schema version 1, strict integer-token/type validation, unknown-field rejection, defaults, same-directory atomic replacement, storage failure behavior, unique corrupt backups, and byte-exact non-UTF-8 preservation were tested. |
| Audio | Mute, pause/resume, transition replacement/cancellation, one-current/one-outgoing ownership, physical child disposal, and zero/negative fades were tested. A real player verified that playback begins only after SceneTree parenting. Human listening and packaged control-path observation were not performed. |
| Animation fixture | Four 6-FPS looping idle cells rebuilt deterministically with shared bottom-center baseline, nearest filtering, uniform scale, alpha/RGB oracles, and collision independence. It covers one disposable idle only, not production state coverage. |
| Runtime capture | A focused real-renderer component verified exact 960×540 output, independent SHA recomputation, safe labels, non-overwrite, error propagation, and rollback after either final-file rename boundary. |

The source-runtime state runner produced 11 deterministic captures covering
action-router movement, camera recovery/arena states, idle wrap, audio service
state, and corrupt-save recovery. These used injected actions or direct service
hooks and are supporting evidence only; they are not physical keyboard input
or uninterrupted packaged gameplay.

## Post-spike regression fixes

Two defects found by later integrated evidence were fixed before the final
macOS assessment:

1. **Audio play-before-parent:** the real `AudioStreamPlayer` initially called
   `play()` before it was inside the SceneTree, producing `Playback can only
   happen when a node is inside the scene tree`. The service now parents the
   next player immediately before playback and disposes stale players
   physically as well as logically. The final source-runtime captures contain
   no play-before-tree diagnostic.
2. **Duplicate desktop touch UI:** both the orientation autoload and the main
   scene instantiated touch controls, so the copies separated under camera
   movement and appeared on macOS. The main-scene copy was removed and a
   platform policy hides touch/orientation UI on desktop. Final packaged views
   at all four assessed sizes show no touch controls, rotate gate, or ghost
   copy.

The historical macOS UI regression remains a recorded `FAIL` observation but
does not support any final result.

## Disposable sprite derivation boundary

The spike used the approved 1086×1448 Trashy presentation sheet only to test a
hash-pinned deterministic derivation pipeline. Its source SHA-256 was
`770aa14d05d0e2db32c1948a58a2db5053500bf6c9a23812a81ecc74d2d764d6`;
the four-frame generated strip SHA-256 was
`d5af42ac34d73e96dbb071c1f01f348af22c0cc3e8eaa8eefd9ec0659303a37c`.

That strip is disposable spike evidence. It must not enter main,
`assets/runtime/`, or production. The project owner is generating clean
sprites/assets and will supply them after this task. Do not derive further
production assets from concept sheets unless explicitly requested or necessary
and reviewed first.

## macOS package identity and viewport evidence

The final reviewed package was an unsigned universal arm64+x86_64 ZIP built
from clean spike source commit
`398503d30ed9f4f558c29229be3062ad34d6e6c7`:

- ZIP SHA-256:
  `b24927ee14a84f478f1626db70bcc72cf36f9961571ced25c112aa634a12f2b8`;
- ZIP size: 65,434,528 bytes;
- executable SHA-256:
  `1914b5c4aa84bbc17725742d477eb80b2b26c73b4738e04196096d1d77380679`;
- ZIP integrity: no errors;
- executable architecture: universal Mach-O, x86_64 and arm64.

The artifact was reproducible, ephemeral evidence stored outside Git. It was
not an immutable or retained release artifact, and its temporary path may no
longer exist. Rebuilding requires the exact source commit, Godot/templates
version, export preset, and command shape:

```text
/opt/homebrew/bin/godot --headless --path <spike-project> --export-debug macOS <temporary-output>/trash-dash-spike-macos.zip --log-file <temporary-output>/export.log
```

A rebuild must be hash-verified before use; reproducibility does not guarantee
that a rebuild under a changed host/toolchain will have the historical hash.

Direct packaged observations:

| Requested macOS window | Status | Screenshot SHA-256 | Observation |
| --- | --- | --- | --- |
| 1280×720 | PASS | `fe38bfea0ba3edcfe9cc3fd409b474ffdcd6c2a5223c12a77804ece01f2dea58` | Full 16:9 FOV; grounded fixture; clean layers; desktop UI only. |
| 1440×900 | PASS | `d1513da24a092ec62e792b70a3d4790fb86c9b3c272aadf76596db4a009e85c3` | Same FOV with symmetric top/bottom letterbox bars; no stretch or crop. |
| 1280×800 | PASS | `b2efdc84c7803e87869584a934928be49ec20a7f086853e56f650a6bbec85a78` | Same FOV with symmetric letterboxing; no mobile UI. |
| 390×844 | PASS | `063ba15cfc3ff98b33f41222fdcfeceff9009e7db93bf7c5c2cbda080598239f` | Desktop narrow/portrait-window policy: centered 16:9 region and large symmetric bars; mobile UI hidden. This is not mobile proof. |

These rows cover package boot, renderer, FOV, letterboxing, and UI policy only.
No human packaged traversal or physical-keyboard feel test was performed.

## Export and platform matrix

| Platform | Export/runtime result | Current MVP effect |
| --- | --- | --- |
| macOS | Universal development export built and launched. Final packaged viewport cases above are `PASS`; human traversal/input, packaged audio/save paths, and the overall gate remain `INCOMPLETE`/`CANNOT VERIFY`. | Foundation accepted for macOS MVP scaffolding/prototype. |
| Windows | A development x86_64 export was built. Historical Parallels runtime reached Compatibility OpenGL 3.3, then repeatedly produced GLES3 vertex-shader compilation failure: renderer `FAIL`. Input/traversal/save/audio are `CANNOT VERIFY`. | Deferred and nonblocking. Requires a supported GPU/driver proof before re-entry. |
| Android | An ARM64 debug APK was built and structurally inspected. No authorized device/emulator was attached, so install, renderer, touch, save, and audio runtime are `CANNOT VERIFY`. Release AAB configuration also remains unproved. | Deferred and nonblocking. |
| iOS | The unsigned export probe stopped because no App Store Team ID was configured. No Team/signing data was fabricated; no physical-device runtime occurred, so iOS proof is `CANNOT VERIFY`. | Deferred and nonblocking; user-led local signing hookup comes later. |
| Linux/web | No presets or runtime work. | Out of scope. |

## V2 release gate

| Gate item | Status | Basis |
| --- | --- | --- |
| 1. Provenance | INCOMPLETE | Disposable derived idle is not production content; clean owner assets are pending. |
| 2. Derivation | INCOMPLETE | Spike fixture was never promoted to production/runtime. |
| 3. Contracts | INCOMPLETE | Unit/controller/display contracts succeeded, but natural packaged traversal did not exercise all consumers. |
| 4. Asset integrity | INCOMPLETE | Spike inspection found no stretch, fringe, clipping, or size pop; production sprite validation is pending. |
| 5. Collision and placement | INCOMPLETE | Package/source views are grounded and aligned, but uninterrupted packaged collision play was not performed. |
| 6. Animation | INCOMPLETE | One source-runtime idle wrap was observed; packaged transitions/facings and clean production states remain unverified. |
| 7. Encounter structure | INCOMPLETE | Synthetic arena lock/release worked through injected source-runtime actions; no packaged encounter traversal. |
| 8. Automated checks | INCOMPLETE | Tests exit 0, but the isolated real-audio test leaves two ObjectDB stream/playback instances and orphan `Master` at process exit. |
| 9. Real runtime | INCOMPLETE | Final package booted, but no uninterrupted human gameplay traversal occurred. |
| 10. Target resolutions | PASS | Final macOS package directly captured and inspected at all four assessed desktop window sizes. |
| 11. Regression scope | PASS | Final package and source captures show the duplicate touch UI fix holds and renderer/FOV remain stable. |
| 12. Evidence | PASS | Source/build identity, commands, ephemeral hashes, viewports, input truth, defects, and limitations were recorded. |

Final SPIKE/V2 gate: **INCOMPLETE**, not `PASS`.

## Unresolved audio-test warning

The normal full suite exits 0 but reports two leaked ObjectDB instances. A
verbose isolation run attributes them to `AudioStreamWAV` (reference count 1),
`AudioStreamPlaybackWAV` (reference count 1), and orphan StringName `Master`
from `test_audio_service.gd::test_real_player_is_inside_tree_before_playback_begins`.
The focused runtime-capture component and normal-speed state runner exit
without those diagnostics. This isolates the warning to the real-audio product
test boundary; it remains unresolved and blocks a clean automated-gate claim.

## Next macOS MVP steps

1. Scaffold the production Godot project from the accepted contracts without
   copying spike implementation or fixtures.
2. Reproduce the input, camera, collision, save, and audio contracts as focused
   production infrastructure, retaining the play-after-parent and desktop UI
   regression protections.
3. Fix the isolated real-audio-test leak warning.
4. Import the owner's clean sprites/assets, validate provenance, geometry,
   alpha, anchors, state coverage, and promotion, and run per-feature gates.
5. Build and hash-verify a fresh universal macOS package, then have a human use
   a physical keyboard for uninterrupted traversal, checkpoint/arena behavior,
   pause/mute/resume, and save/relaunch before any `PASS` completion claim.

## Deferred-platform re-entry gates

- **Windows:** use a supported Windows GPU/driver environment; resolve the
  historical Compatibility shader `FAIL`; repeat package boot, physical
  keyboard traversal, save, audio, and target-window evidence.
- **Android:** attach an authorized physical device or reviewed emulator;
  verify Compatibility rendering, landscape touch lifecycle, safe areas,
  pause/focus clearing, save/audio/relaunch, and the signed Gradle/AAB path.
- **iOS:** let the owner configure Team ID/signing locally outside Git; use a
  physical iPhone/iPad to verify Compatibility rendering, landscape touch,
  safe areas, lifecycle clearing, save/audio/relaunch, and export/package
  behavior. A simulator cannot replace the required physical-device proof.

Re-entry is intentionally deferred until the macOS prototype is meaningful.
No deferred platform inherits acceptance from the macOS foundation.
