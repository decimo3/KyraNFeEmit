# Fix InterceptedClickException 2

This error occurred when the [EMIT_AVANCAR](src/nfe_bot.path#L25) button was clicked before the modal dialog had fully closed.

To resolve the issue, the program now waits for the modal to disappear before attempting further interactions. This prevents premature clicks and eliminates the `InterceptedClickException`.
