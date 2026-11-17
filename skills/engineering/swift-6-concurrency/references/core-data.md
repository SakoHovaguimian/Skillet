# Core Data and concurrency

Keep live managed objects within their managed object context's confinement rules. Transfer a suitable `NSManagedObjectID` or immutable value snapshot instead of the live object. Inspect whether an ID is temporary and whether another context can resolve the object yet; obtaining an ID alone does not publish unsaved changes.

Use the context's supported `perform` APIs for context work and inspect the returned values before crossing isolation. An arbitrary Swift actor wrapping a context does not replace Core Data's queue-confinement contract. Main-queue and private-queue contexts have distinct execution requirements.

When a diagnostic appears, identify the exact context, object, callback, and transfer first. Do not suppress Sendable errors to share managed objects. Follow the imported SDK's actual annotations and repository verification limits.

Sources: [Apple's Core Data concurrency guide](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreData/Concurrency.html) and [temporary object IDs](https://developer.apple.com/documentation/coredata/nsmanagedobjectid/istemporaryid).
