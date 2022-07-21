# PhD Thesis

## Fonts
The LaTeX engine (xelatex) does not natively support raster fonts (required for coloured noto emoji). lualatex is an alternative engine, but breaks other things. Really, we can use a hack to replace unicode characters with images that are pre-rendered emoji glyphs.

It's possible to render out the glyphs [using freetype](https://stackoverflow.com/questions/71092136/how-to-load-colorful-emojis-in-pygame) or PIL. Both of these cases require special care. Thankfully, there is also [emojicdn](https://emojicdn.elk.sh/%F0%9F%8C%8A?style=Google) that serves emoji PNGs as a service.
