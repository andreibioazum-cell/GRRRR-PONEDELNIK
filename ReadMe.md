PonedelnikOS
=======================
**[Upstream Homepage](https://www.haiku-os.org/)
| [Mailing Lists](https://www.haiku-os.org/community/ml)
| [IRC Channels](https://www.haiku-os.org/community/irc)
| [Issue Tracker](https://dev.haiku-os.org/)
| [API docs](https://api.haiku-os.org)**

PonedelnikOS is a downstream operating system based on Haiku. It keeps the
Haiku code base, build system, and application compatibility, while using the
PonedelnikOS name for its own images and user-facing branding.

Haiku is an open-source operating system that specifically targets personal
computing. Inspired by the BeOS, Haiku is fast, simple to use, easy to learn
and yet very powerful.

Attribution
------------
PonedelnikOS is derived from Haiku. The original copyright notices and author
credits are kept in the source files. Copyright in the original Haiku code
remains with Haiku, Inc. and the respective authors where expressly noted.
See `License.md` and `NOTICE.md`.

Goals
------------
 * Sensible defaults with minimal configuration required.
 * Clean, clear, concise code.
 * Unified desktop environment.

Trying PonedelnikOS
---------------
PonedelnikOS images are built from this repository by the GitHub Actions
workflow in `.github/workflows/build.yml`. It publishes a bootable
`PonedelnikOS.iso` - an anyboot image that can be written to a CD/DVD or a USB
stick, or attached to a virtual machine as a CD drive.

Upstream Haiku provides pre-built [nightly images](http://download.haiku-os.org/) and
[release images](https://www.haiku-os.org/get-haiku). Haiku is compatible
with a large variety of hardware, but in case you don't want to "take the
plunge" and install Haiku on bare metal, you can install it on a virtual
machine (VM) instead. If you've never used a VM before, you can follow one of
the ["Emulating Haiku"](https://www.haiku-os.org/guides/virtualizing/) guides.

Compiling PonedelnikOS
---------------
See `ReadMe.Compiling.md`. The build still uses Haiku's `configure` and Jam
tooling. Internal Haiku target and package names are kept for compatibility.

Contributing
-------------------
Upstream Haiku is a meritocratic open source project with a large variety of tasks. Even
if you can't write code, *you can still help*! Haiku needs designers,
(technical) writers, translators, testers... [Get involved](https://www.haiku-os.org/community/getting-involved/)
and help out!

### Contributing code
If you're submitting a patch to us, please make sure you're following the
[patch submitting guidelines](https://dev.haiku-os.org/wiki/CodingGuidelines/SubmittingPatches).

If you're having trouble finding something in the source tree, you can use
one of our web-based source code browsers:

 * https://grok.nikisoft.one/opengrok/ (OpenGrok, provided by Niklas Poslovski)
 * https://git.haiku-os.org/ (git, provided by Haiku, Inc.)

### Contributing documentation
The main piece of documentation that still needs work are the API docs (found
in the tree at `docs/user`). Just find an undocumented class, write
documentation for it, and [submit a patch](https://dev.haiku-os.org/wiki/CodingGuidelines/SubmittingPatches).

### Contributing translations
See [wiki:i18n](https://dev.haiku-os.org/wiki/i18n).

### Contributing software ports
See [HaikuPorts](https://github.com/haikuports/haikuports/).

### Contributing to our infrastructure
See [Infrastructure](https://github.com/haiku/infrastructure/).
