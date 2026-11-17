# Async/Await Basics

## Core Rules

- Mark asynchronous work with `async`.
- Mark fallible asynchronous work with `async throws`.
- Use `await` only at suspension points.
- Keep sequential code sequential unless parallelism is needed.

## Calling Patterns

```swift
func fetchUser() async throws -> User { ... }

Task {
    let user = try await fetchUser()
    print(user)
}
```

## Parallel Work With async let

Use `async let` when task count is known at compile time.

```swift
async let profile = fetchProfile()
async let posts = fetchPosts()
let (p, ps) = try await (profile, posts)
```

## URLSession Pattern

```swift
func load(_ request: URLRequest) async throws -> Data {
    let (data, response) = try await URLSession.shared.data(for: request)
    guard let http = response as? HTTPURLResponse,
          (200...299).contains(http.statusCode) else {
        throw NetworkError.invalidResponse
    }
    return data
}
```

## Typed Errors (Swift 6)

Use typed throws when API contracts benefit from explicit error sets.

```swift
enum APIError: Error { case badStatus, transport(URLError) }
func fetch() async throws(APIError) -> Data { ... }
```
