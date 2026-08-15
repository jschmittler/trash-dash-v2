# Canonical Assets

The canonical register is `docs/design/trash-dash/manifests/canonical-asset-manifest.json`.

- Isolated props and tilesheets are approved source art, never automatically runtime assets.
- Concept art and blueprints define environment appearance and composition; foreground sheets are contact/reference sheets.
- Level specifications define interpretation and use; Enemy Master Specifications define enemy identity and behavior.
- Generated/runtime derivatives must record their `derived-from` relationship and may not redefine source appearance.

Run `python3 tools/verify/audit_canonical_assets.py` after any canonical import or asset replacement.
