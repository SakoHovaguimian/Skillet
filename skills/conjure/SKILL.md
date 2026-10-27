---
name: conjure
description: Create a modular brand identity and UI design system dashboard in one HTML file. Use when asked for a brand dashboard, a visual identity with web and iOS component previews, or targeted updates to a Conjure dashboard. Do not use for production app implementation or project scaffolding.
disable-model-invocation: true
---

# Conjure

## Outcome

Act as a Principal UI/UX Engineer and Lead Brand Designer. Turn the user's concept, palette, and inspiration into a complete Brand Identity and UI Design System Dashboard in one HTML file, with embedded CSS and JavaScript.

Present a coherent identity, a Web Portal component showcase, and an iOS Grimoire simulator with Rune design tokens. Make every section and theme independently addressable for later surgical updates. This skill owns the design artifact; it does not implement or reconfigure the user's production web or iOS project.

## Inputs and preconditions

Always ask for inputs as the first user-facing action on every invocation, before research, design, code generation, file edits, or tool calls. This intake is required even when the invocation already contains a complete brief: summarize the supplied answers and ask the user to confirm or revise them and add any images. Wait for a reply before proceeding. An output-only-HTML instruction applies to delivery, not this intake.

Ask for these inputs together in one concise message:

1. **Concept:** Brand or product name, what it does, and who it serves.
2. **Brand colors:** Exact colors or a palette, including any fixed colors. Offer to choose colors if the user prefers.
3. **Inspiration/vibe:** Desired visual tone, references or links, and anything to avoid.
4. **Optional images:** Invite attached images, logos, screenshots, moodboards, local image paths, or image links. Ask whether they should guide the aesthetic or appear in the dashboard.

Use a normal chat message to invite attachments; do not rely on a text-only question widget for image submission. Images are optional. If the user says images are still coming, wait for them or for the user to say to proceed without them.

For an existing dashboard, prefill the intake from the current conversation and ask the user to confirm the brief and requested change. Do not make the user retype known inputs.

The reply may explicitly delegate palette or aesthetic choices. Treat that as an answer, choose a coherent direction, and proceed without another approval round. If a required input remains unanswered and has not been delegated, ask only for that input and wait. Do not substitute guesses or elapsed time for the required reply.

## Workflow

1. Complete the intake above. Once answered, continue through delivery without repeating the gate during the same invocation.
2. Read [references/dashboard-contract.md](references/dashboard-contract.md) for the required deliverables, token architecture, semantic IDs, and verification criteria.
3. Inspect supplied images and relevant inspiration links. Distinguish explicit requirements from visual references. Extract useful direction such as palette, type character, shapes, texture, density, and composition. Ask about a conflict only when it materially changes the result.
4. Establish one visual direction across the identity, web, and mobile sections. Use the confirmed concept and palette to write real brand copy, choose fonts, design the SVG mark, and create illustrations or complete image prompts.
5. Build the complete HTML dashboard according to the contract. Keep visual tokens in CSS `:root`, isolate theme data from interaction code, and derive shared web/iOS values from the same tokens.
6. For a targeted update, inspect the existing file and trace the requested section or token dependencies before editing. Preserve unrelated sections, stable IDs, and established behavior. Propagate shared token changes to affected previews and serialized theme output; keep a platform-specific change scoped to that platform.
7. Check completeness, token consistency, responsive layout, and working demo interactions. Preview the HTML when a browser is available. Correct observed issues before delivery and avoid claiming visual verification if no preview was possible.

## Constraints

- Respect the user's explicit requirements over inferred reference styling. Do not replace a supplied concept, fixed palette, or existing identity without direction.
- Deliver one HTML file. Embed its CSS, JavaScript, SVGs, and any user images used in the output; Google Fonts and necessary verified Unsplash imagery are the external asset exceptions described in the contract.
- Write finished content and functioning component demonstrations. Do not use unfinished sections, TODOs, lorem ipsum, dead controls, or omitted code.
- Preserve modularity through semantic IDs, named token groups, and clearly commented theme and interaction script blocks.
- Treat Rune JSON as a proposed design-token mapping unless supplied project sources establish the actual schema. Do not invent Rune APIs, claim native integration, or present a CSS phone frame as an iOS runtime.
- Keep the work limited to the dashboard and authorized reference inspection. Do not scaffold projects, edit production app sources, publish the result, or upload supplied images to an external service as part of this workflow.

## Failure handling

- **No intake reply:** Leave the input request pending and stop before generating or editing the dashboard.
- **Unavailable reference:** State which image or link could not be inspected. Ask for an accessible replacement when it is essential; otherwise continue from the confirmed brief and record the reference limitation in the dashboard.
- **Conflicting references:** Keep explicit user choices authoritative. Ask for a decision when equally authoritative inputs would force incompatible results.
- **Raster assets cannot be embedded:** Prefer CSS or inline SVG when the user permits substitution. If the exact asset is required, ask for an accessible asset rather than leaving a broken image.
- **Fonts unavailable:** Keep the chosen font stacks and usable local fallbacks. Distinguish an external font-loading limit from a design decision in the dashboard.
- **No native schema available:** Include the complete proposed Rune token object and label its status within the iOS section; continue with the HTML preview.
- **Preview unavailable:** Inspect source and data consistency, and put a brief verification limitation inside the dashboard instead of claiming a browser check passed.

## Output contract

After intake is complete, deliver one complete `index.html`, or the complete updated HTML file for a surgical edit. Use the user's requested destination when writing a file. Otherwise choose a dedicated dashboard output location rather than overwriting an unrelated application entry point.

The file must contain every deliverable and stable section ID in [references/dashboard-contract.md](references/dashboard-contract.md). Keep assumptions, asset notes, and material verification limits inside the relevant dashboard sections.

Return only raw HTML when the platform renders it directly. Otherwise return one `html` code block identified as `index.html`, with the entire document and no surrounding prose. Intake questions precede this final-output restriction. Never return only a patch, a fragment, or a shortened document.
