# Task ownership and memory

Trace owner → stored task → closure captures → suspended operation. A weak capture becomes a strong reference again when unwrapped. If that strong reference spans an endless observation loop or an indefinitely suspended method, `deinit` cannot be relied on to cancel the very task keeping the owner alive.

## Choose an explicit lifetime

- For work owned by a screen, use the established lifecycle boundary; SwiftUI `.task` offers cancellation of its own task when the view lifetime ends, not automatic cancellation of unrelated tasks it starts.
- For an owner-stored unstructured task, provide a real stop/replacement path. Cancel before replacing it and prevent old cleanup from clearing the new task handle or loading state.
- Capture immutable dependencies separately when a suspended operation need not retain the UI owner. Reacquire the owner only for the brief state application, inside its isolation domain.
- For streams, avoid holding a strong owner for the full iteration lifetime. An explicit stop path must remove observers, finish/cancel production as required, and terminate consumption.

Weak capture and cancellation solve different problems. Cancellation is cooperative; inspect what makes the suspended operation actually return. A canceled sleep must exit the loop rather than be swallowed by `try?` and immediately repeated. Deinitialization cleanup is a backstop, not the sole lifecycle design.

Use permitted runtime inspection for release/lifetime confirmation; a source review can identify a retention path without proving deallocation.
