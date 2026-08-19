# Tasks

## Choose The Right Primitive

- `Task {}`: Bridge sync to async or start unstructured work.
- `async let`: Fixed-count parallel operations.
- `withTaskGroup`: Dynamic parallel fan-out/fan-in.
- `Task.detached`: Independent work that must not inherit parent context.

## Cancellation

Treat cancellation as cooperative.

```swift
func work() async throws {
    try Task.checkCancellation()
    let data = try await fetch()
    try Task.checkCancellation()
    process(data)
}
```

## Task Groups

```swift
let images = try await withThrowingTaskGroup(of: UIImage.self) { group in
    for url in urls {
        group.addTask { try await download(url) }
    }

    var out: [UIImage] = []
    for try await image in group {
        out.append(image)
    }
    return out
}
```

## SwiftUI Integration

- Use `.task {}` for lifecycle-bound async work.
- Use `.task(id:)` for cancel-and-restart behavior tied to state changes.
