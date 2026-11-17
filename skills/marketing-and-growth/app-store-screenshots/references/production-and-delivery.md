# Production and delivery

Use this reference before choosing a production pipeline, verifying platform requirements, or exporting a set. No bundled exporter or private runtime is required. Discover the environment's available tools and follow their actual capabilities and restrictions.

## Verify current Apple requirements

Read the relevant sections of these primary sources and record their URLs and the check date in the campaign handoff:

| Source | What to verify |
| --- | --- |
| [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) | Supported target device/display classes, required sets, accepted dimensions/orientations, formats, transparency, and scaling behavior |
| [Asset best practices](https://developer.apple.com/app-store/asset-best-practices/) | Screenshot placement, product visibility, sequence, and distinctions from other marketing asset types |
| [App Review screenshot guidance](https://developer.apple.com/help/app-review/guideline-reference/2-3-3-screenshots/) | Authentic app-in-use coverage for each supported device set, overlays, marketing panels, and misleading content |
| [Product page optimization](https://developer.apple.com/app-store/product-page-optimization/) | Experiment requirements and interpretation, only when optimization is in scope |

These links were checked while authoring the skill on 2026-11-13. That authoring check does not verify requirements for a later campaign. Do not hardcode a size table as timeless policy or extrapolate one device's rules to every supported device.

Build a compact requirement record for each requested device/locale: selected size and orientation, source supporting it, required panel count/coverage constraints, and unresolved requirements. Check the screenshot set as well as individual files. A correct canvas size does not prove accurate app representation or Apple acceptance.

## Choose a fidelity pipeline

### Concept artwork

Use approved image generation/editing to explore the complete panel, with authentic captures as content references. Inspect generated UI for material deviations. Mark output as concept when interface pixels, text, or data have been regenerated, even if the final dimensions are accepted by the store.

### Submission artwork

Use a permitted method that retains the real captured interface as a controlled image element. Preserve its proportions and depicted behavior. Record meaningful crop/scale transformations; “authentic capture” does not mean every exported pixel is unchanged after resampling.

Generate decorative assets separately when useful and permitted. Keep typography and original logos controlled when possible. Inspect the composition against the source capture. A flattened generative panel cannot be certified as authentic by its filename or by asking the model to preserve it.

If exact composition is unavailable or forbidden by active tool rules, keep concept work useful and identify the missing production operation. Do not install dependencies, call paid APIs, or use an alternative editing route solely to evade a tool restriction.

### Source quality

Prefer fresh, appropriate captures over repairing developer overlays, broken states, inconsistent data, or personal information in generated UI. A request for screenshot artwork does not authorize building or modifying the app to obtain them. Ask for suitable captures or use an already available authorized capture workflow.

For insufficient resolution, request a better source or choose a layout that uses it at a credible scale. Upscaling does not recover authentic detail. Do not fabricate a larger device's interface by stretching or regenerating a smaller one.

## Export checks

Use actual file metadata and a rendered inspection, not requested generation settings, to verify:

- File count and order match the selected storyboard for every requested device/locale.
- Pixel dimensions, orientation, format, color mode, and transparency satisfy the checked requirements.
- The file decodes and the exported image matches the selected artwork; no accidentally included alternate, old copy, or contact sheet occupies a panel slot.
- Resizing has not distorted the device, clipped text, changed a seam, or made the UI illegible.
- Unsupported trust claims, unintended personal information, debug overlays, and inconsistent app states have been addressed within the permitted workflow.

Do not silently crop to force an aspect ratio. Recompose when needed. Preserve originals and use a new destination or version for revisions rather than overwriting the only accepted source. Apply the same checks after any final format conversion.

## Package the result

For a saved campaign, use ordered filenames and separate requested device/locale sets. Keep concept and submission-candidate exports clearly separated. A simple layout is sufficient:

```text
campaign/
  campaign.md
  originals/
  exports/
    en-US/
      selected-device-set/
        01-core-benefit.png
        02-workflow.png
  previews/
    en-US-selected-device-set.png
```

Names above illustrate structure, not a required locale, device, count, or format. Preserve source assets only where authorized and useful; never copy an entire unrelated asset directory. Keep the user's originals intact. Produce a ZIP when useful and supported, containing the selected deliverables rather than stale variants or unrelated private files.

The compact campaign manifest records:

- Brief, delivery mode, visual-system decisions, exact copy, and stable panel IDs/order.
- Original source references and their roles, successful prompts or composition recipe, and editable-source paths when created.
- Per-export relative path, device/locale, native and exported dimensions, format, meaningful transformations, and fidelity status.
- Apple sources/check date, actual metadata and visual checks, connected pairs inspected, and remaining limitations.

Use relative paths inside saved delivery records. Avoid exposing private developer-home paths, secrets, or sensitive source content. Keep records proportional to the set; a compact Markdown table is enough for a small campaign.

Show the review preview and link the selected files in the final response. If a preview or archive cannot be produced, deliver the individual images and disclose the missing artifact. Submission candidate means the documented checks passed; it is not an upload or an Apple approval.
