//! Independent Rust implementation of Rule 30.
//!
//! The implementation is added only after shared reference vectors are frozen.

#![forbid(unsafe_code)]

/// Package readiness marker used by the initial workspace smoke test.
pub const BACKEND_IMPLEMENTED: bool = false;

#[cfg(test)]
mod tests {
    use super::BACKEND_IMPLEMENTED;

    #[test]
    fn scaffold_is_explicitly_unimplemented() {
        assert!(!BACKEND_IMPLEMENTED);
    }
}
