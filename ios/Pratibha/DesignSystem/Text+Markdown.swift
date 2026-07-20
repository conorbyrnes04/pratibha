import Foundation

extension AttributedString {
    /// Interprets inline markdown (**bold**, *italic*) while preserving the
    /// original whitespace and line breaks — ideal for the commentary and
    /// teaching prose, which use light markdown inside multi-line text.
    static func fromCommentary(_ source: String) -> AttributedString {
        let options = AttributedString.MarkdownParsingOptions(
            interpretedSyntax: .inlineOnlyPreservingWhitespace
        )
        return (try? AttributedString(markdown: source, options: options))
            ?? AttributedString(source)
    }
}
