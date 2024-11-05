# Signatures

DIYivi offers a front-end to use Yivi's attribute-based signatures. Users can:

- Create a signature.
- Verify a signature.
- Request a signature from someone else.

## Background

While attribute-based signatures have been available in Yivi for quite some time, as far as I know,
they have not been used much. This likely has several reasons:

- Currently, signatures can only be made on a plain-text string. Technically, it's easy to enable
  signing of files (such as PDFs), but this has not been implemented in Yivi (especially in the
  Yivi app). As a result, for many applications, the only reasonable alternatives are:

  - Signing a hash of the file (which is not user-friendly and hence not really secure).
  - Relying on a third party that makes a classical signature on the file,
    after a _disclosure_ from the user to that party. Here, the user is not in control
    of the creation of the signature, which similarly limits the trustworthiness of the signature.

- Creating a Yivi signature (currently) requires that the message to be signed is sent to an
  `irma server`, that can theoretically spy on the message, or even try to trick the user into
  signing a different message.

- There is no publicly accessible example of how Yivi signatures can be used. At the time of
  writing, there is only an outdated demo of requesting a signature on a hardcoded message,
  which does not present the actual signature to the user, and does not allow for verification.

- There is/was no API endpoint for signature verification in `irma server`.
  For DIYivi, I have implemented this, and this may (have) be(en) merged into `irmago` some day.

## Desired properties
