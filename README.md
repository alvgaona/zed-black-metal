# Black Metal for Zed

Pitch-black [base16](https://github.com/chriskempson/base16) **Black Metal** themes for the
[Zed](https://zed.dev) editor — a port of metalelf0's band-named
[`base16-black-metal`](https://github.com/metalelf0/base16-black-metal) family, plus a
frosted-glass **Blurred** companion for every variant.

Each theme is dead black (`#000000`) with low-saturation foregrounds. The bands differ in
exactly two accent slots — strings/additions and types/modified — so picking a band only
changes the syntax accent color, not the overall mood.

## Variants

Every theme ships in two flavors: **opaque** and **Blurred** (translucent window with macOS
vibrancy blur, `background.appearance = "blurred"`).

| Theme | Strings / additions | Types / modified |
| --- | --- | --- |
| Black Metal _(default)_ | `#dd9999` | `#a06666` |
| Black Metal (Bathory) | `#fbcb97` | `#e78a53` |
| Black Metal (Burzum) | `#ddeecc` | `#99bbaa` |
| Black Metal (Dark Funeral) | `#d0dfee` | `#5f81a5` |
| Black Metal (Gorgoroth) | `#9b8d7f` | `#8c7f70` |
| Black Metal (Immortal) | `#7799bb` | `#556677` |
| Black Metal (Khold) | `#eceee3` | `#974b46` |
| Black Metal (Marduk) | `#a5aaa7` | `#626b67` |
| Black Metal (Mayhem) | `#f3ecd4` | `#eecc6c` |
| Black Metal (Nile) | `#aa9988` | `#777755` |
| Black Metal (Venom) | `#f8f7f2` | `#79241f` |

## Install

### As a local Zed extension

1. Open Zed → command palette → **`zed: install dev extension`**
2. Select this repository folder.

### Manual

Copy the generated theme into your Zed themes directory:

```sh
just install            # copies themes/black-metal.json to ~/.config/zed/themes/
```

Then open the theme selector (`cmd-k cmd-t`) and pick any variant.

> **Blurred variants:** the `background.appearance` key changes how the OS window itself is
> created, so switching **to** or **from** a Blurred variant needs a full Zed restart
> (`cmd-q` then reopen) — reselecting alone won't toggle the transparency.

## Develop

The committed `themes/black-metal.json` is **generated** — don't edit it by hand. The source
of truth is:

- `src/base.json` — the two canonical base themes (opaque + Blurred), including all the
  surface transparency tuning for the frosted look.
- `palettes/*.yaml` — the vendored Warp base16 Black Metal palettes; each band's two accent
  colors are read from here.
- `scripts/generate.py` — derives every variant by swapping the two accent slots.

```sh
just build      # regenerate themes/black-metal.json
just check      # regenerate, fail if stale, validate JSON
just install    # build + copy into ~/.config/zed/themes
just clean      # remove generated output
```

The generator uses only the Python standard library — no dependencies.

## Credits

- [metalelf0/base16-black-metal](https://github.com/metalelf0/base16-black-metal) — the
  original palette and band variants.
- [base16](https://github.com/chriskempson/base16) — the framework.
- Structure inspired by [catppuccin/zed](https://github.com/catppuccin/zed).

## License

[MIT](./LICENSE)
