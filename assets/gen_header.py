"""Generates assets/header.svg: a fake Neovim session (dotnet-tree + buffer + dotnet-counters)."""
import sys
from html import escape

OUT = sys.argv[1]

W, H = 1000, 430
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
FS = 13
CW = 7.85          # approx advance of a 13px monospace glyph
LH = 21            # line height in the buffer

C = dict(
    bg="#1a1b26", bg_dark="#16161e", bg_hl="#292e42", border="#2a2e42",
    fg="#c0caf5", dim="#565f89", nr="#3b4261",
    kw="#bb9af7", type="#2ac3de", str="#9ece6a", num="#ff9e64",
    fn="#7aa2f7", op="#89ddff", cmt="#565f89", green="#9ece6a",
    yellow="#e0af68", red="#f7768e", blue="#7aa2f7", cyan="#7dcfff", purple="#bb9af7",
)

TOP = 38                      # below the window title bar
TREE_W = 215
PANEL_W = 190
BUF_X = TREE_W
BUF_W = W - TREE_W - PANEL_W
STATUS_Y = H - 52
CMD_Y = H - 28

# ---------------------------------------------------------------- buffer code
K, T, S, N, F, O, M, P = "kw", "type", "str", "num", "fn", "op", "cmt", "fg"
CODE = [
    [("namespace ", K), ("Cermenate", T), (".", O), ("Italy", T), (";", O)],
    [],
    [("/// Shipping code since I was 14: PHP first, .NET now.", M)],
    [("public sealed record ", K), ("Alessandro", T), (" : ", O), ("Developer", T)],
    [("{", O)],
    [("    public ", K), ("string  ", T), (" Company  ", P), ("=> ", O), ('"@WiseDigitalStudio"', S), (";", O)],
    [("    public ", K), ("string  ", T), (" Role     ", P), ("=> ", O), ('"Co-founder"', S), (";", O)],
    [("    public ", K), ("string[]", T), (" Stack    ", P), ("=> ", O), ("[", O), ('"C#"', S), (", ", O),
     ('".NET"', S), (", ", O), ('"Azure"', S), (", ", O), ('"Angular"', S), ("];", O)],
    [("    public ", K), ("string  ", T), (" Editor   ", P), ("=> ", O), ('"Neovim"', S), (";", O),
     (" // yes, for .NET too", M)],
    [("    public ", K), ("string  ", T), (" OS       ", P), ("=> ", O), ('"macOS"', S), (";", O)],
    [("    public ", K), ("string  ", T), (" AIAgent  ", P), ("=> ", O), ('"Claude Code"', S), (";", O)],
    [("    public ", K), ("string  ", T), (" Based    ", P), ("=> ", O), ('"Como, Italy"', S), (";", O)],
    [("}", O)],
]

T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
CPS = float(sys.argv[3]) if len(sys.argv) > 3 else 75


def text(x, y, s, fill, size=FS, weight=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"{w} {extra}>{escape(s)}</text>'


parts = []
add = parts.append

add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="A Neovim session: Alessandro.cs being typed, a .NET solution tree and live counters">
<style>text{{font-family:{FONT};white-space:pre}}</style>
<defs>
  <clipPath id="win"><rect width="{W}" height="{H}" rx="12"/></clipPath>
  <linearGradient id="spark" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{C['cyan']}" stop-opacity=".35"/><stop offset="1" stop-color="{C['cyan']}" stop-opacity="0"/>
  </linearGradient>
</defs>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="{C['bg']}"/>''')

# ---------------------------------------------------------------- title bar
add(f'<rect width="{W}" height="{TOP}" fill="{C["bg_dark"]}"/>')
for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
    add(f'<circle cx="{22 + i * 20}" cy="{TOP / 2}" r="6" fill="{col}"/>')
add(text(W / 2, TOP / 2 + 4.5, "nvim — ~/alessandro", C["dim"], 12, extra='text-anchor="middle"'))
add(f'<line x1="0" y1="{TOP}" x2="{W}" y2="{TOP}" stroke="{C["border"]}"/>')

# ---------------------------------------------------------------- tree (dotnet-tree.nvim)
add(f'<rect x="0" y="{TOP}" width="{TREE_W}" height="{STATUS_Y - TOP}" fill="{C["bg_dark"]}"/>')
add(f'<line x1="{TREE_W}" y1="{TOP}" x2="{TREE_W}" y2="{STATUS_Y}" stroke="{C["border"]}"/>')
TREE = [
    (0, "sln", "Solution 'alessandro'", C["fg"], True),
    (1, "proj", "profile", C["blue"], False),
    (2, "cs", "Alessandro.cs", C["fg"], False),
    (1, "proj", "neovim", C["blue"], False),
    (2, "lua", "dotnet-tree.nvim", C["fg"], False),
    (2, "lua", "nuget.nvim", C["fg"], False),
    (2, "lua", "dotnet-counters.nvim", C["fg"], False),
    (1, "proj", "work", C["blue"], False),
    (2, "pkg", "WiseDigitalStudio", C["fg"], False),
    (1, "closed", "legacy (php, 2012)", C["dim"], False),
]
ty = TOP + 26
ICON = {"sln": C["purple"], "proj": C["blue"], "cs": "#68217a", "lua": "#51a0cf", "pkg": C["yellow"], "closed": C["dim"]}
for depth, kind, label, col, bold in TREE:
    x = 12 + depth * 14
    if label == "Alessandro.cs":
        add(f'<rect x="0" y="{ty - 15}" width="{TREE_W}" height="{LH}" fill="{C["bg_hl"]}"/>')
    if kind in ("proj", "closed"):
        add(text(x, ty, "▾" if kind == "proj" else "▸", C["dim"], 11))
        x += 12
    if kind == "cs":
        add(f'<rect x="{x}" y="{ty - 10}" width="11" height="11" rx="2" fill="#9b4f96"/>')
        add(text(x + 1.2, ty - 1.5, "C#", "#fff", 7, "bold"))
    else:
        add(f'<rect x="{x + 1}" y="{ty - 9}" width="9" height="9" rx="{4.5 if kind == "lua" else 2}" fill="{ICON[kind]}"/>')
    add(text(x + 17, ty, label, col, 12.5, "bold" if bold else None))
    ty += LH

# ---------------------------------------------------------------- buffer
# tab line
add(f'<rect x="{BUF_X}" y="{TOP}" width="{BUF_W}" height="26" fill="{C["bg_dark"]}"/>')
add(f'<rect x="{BUF_X}" y="{TOP}" width="128" height="26" fill="{C["bg"]}"/>')
add(f'<rect x="{BUF_X}" y="{TOP}" width="128" height="2" fill="{C["blue"]}"/>')
add(text(BUF_X + 14, TOP + 17.5, "Alessandro.cs", C["fg"], 12))
add(text(BUF_X + 150, TOP + 17.5, "nuget://installed", C["dim"], 12))

CODE_TOP = TOP + 52
GUTTER = 42
cx0 = BUF_X + GUTTER + 12
add('<g>')
t = T0
cursor_anims = []
ROWS = 13
for i in range(ROWS):
    y = CODE_TOP + i * LH
    if i < len(CODE):
        add(text(BUF_X + GUTTER - 6, y, str(i + 1), C["nr"], 12, extra='text-anchor="end"'))
        line = CODE[i]
        n = sum(len(s) for s, _ in line)
        dur = max(n / CPS, 0.12)
        width = n * CW + 4
        cid = f"l{i}"
        add(f'<clipPath id="{cid}"><rect x="{cx0}" y="{y - 15}" height="{LH}" width="0">'
            f'<animate attributeName="width" from="0" to="{width:.1f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" values="{";".join(f"{min(k * CW, width):.1f}" for k in range(n + 1)) if n else "0"}"/>'
            f'</rect></clipPath>')
        spans = "".join(f'<tspan fill="{C[c] if c in C else C["fg"]}">{escape(s)}</tspan>'
                        for s, c in line)
        add(f'<text x="{cx0}" y="{y}" font-size="{FS}" clip-path="url(#{cid})">{spans}</text>')
        cursor_anims.append((t, dur, y, n))
        t += dur + (0.12 if CPS < 1000 else 0)
    else:
        add(text(BUF_X + GUTTER - 6, y, "~", C["nr"], 12, extra='text-anchor="end"'))
add('</g>')
T_END = t

# cursor
cur = [f'<rect x="{cx0}" y="{CODE_TOP - 14}" width="{CW:.1f}" height="17" fill="{C["fg"]}" opacity=".85">']
for (b, d, y, n) in cursor_anims:
    cur.append(f'<set attributeName="y" to="{y - 14}" begin="{b:.2f}s" fill="freeze"/>')
    if n:
        vals = ";".join(f"{cx0 + k * CW:.1f}" for k in range(n + 1))
        cur.append(f'<animate attributeName="x" values="{vals}" calcMode="discrete" begin="{b:.2f}s" dur="{d:.2f}s" fill="freeze"/>')
    else:
        cur.append(f'<set attributeName="x" to="{cx0}" begin="{b:.2f}s" fill="freeze"/>')
cur.append(f'<animate attributeName="opacity" values=".85;.85;0;0" keyTimes="0;.5;.5;1" dur="1.1s" begin="{T_END:.2f}s" repeatCount="indefinite"/>')
cur.append('</rect>')
add("".join(cur))

# ---------------------------------------------------------------- counters panel (dotnet-counters.nvim)
PX = W - PANEL_W
add(f'<rect x="{PX}" y="{TOP}" width="{PANEL_W}" height="{STATUS_Y - TOP}" fill="{C["bg_dark"]}"/>')
add(f'<line x1="{PX}" y1="{TOP}" x2="{PX}" y2="{STATUS_Y}" stroke="{C["border"]}"/>')
add(text(PX + 14, TOP + 24, "dotnet-counters", C["fg"], 12.5, "bold"))
add(text(PX + 14, TOP + 41, "pid 2012 · uptime 14y", C["dim"], 11))

METRICS = [
    ("CPU · curiosity", C["green"], "0.78;0.95;0.84;0.99;0.78", "4.1s"),
    ("Memory · open tabs", C["blue"], "0.55;0.62;0.71;0.66;0.55", "5.3s"),
    ("GC · refactoring", C["purple"], "0.30;0.62;0.25;0.48;0.30", "3.7s"),
    ("Espresso / hour", C["yellow"], "0.40;0.40;0.85;0.40;0.40", "6.2s"),
]
BAR_W = PANEL_W - 28
my = TOP + 70
for label, col, vals, dur in METRICS:
    add(text(PX + 14, my, label, C["dim"], 11))
    add(f'<rect x="{PX + 14}" y="{my + 6}" width="{BAR_W}" height="7" rx="3.5" fill="{C["bg_hl"]}"/>')
    ws = ";".join(f"{float(v) * BAR_W:.1f}" for v in vals.split(";"))
    add(f'<rect x="{PX + 14}" y="{my + 6}" width="{float(vals.split(";")[0]) * BAR_W:.1f}" height="7" rx="3.5" fill="{col}">'
        f'<animate attributeName="width" values="{ws}" dur="{dur}" repeatCount="indefinite" calcMode="spline" '
        f'keySplines="{";".join([".4 0 .2 1"] * (len(vals.split(";")) - 1))}"/></rect>')
    my += 38

add(text(PX + 14, my, "Exceptions", C["dim"], 11))
add(text(PX + PANEL_W - 14, my, "0  (good day)", C["green"], 11, extra='text-anchor="end"'))
my += 26
add(text(PX + 14, my, "commits / week", C["dim"], 11))
# sparkline that scrolls left forever
pts = [6, 9, 7, 12, 8, 14, 11, 18, 10, 15, 21, 13, 17, 24, 16, 20, 26, 19, 14, 9, 6]
step = BAR_W / (len(pts) - 1)
sy = my + 44
def poly(off):
    return " ".join(f"{PX + 14 + off + k * step:.1f},{sy - v * 1.3:.1f}" for k, v in enumerate(pts))
add(f'<clipPath id="sp"><rect x="{PX + 14}" y="{sy - 40}" width="{BAR_W}" height="44"/></clipPath>')
add(f'<g clip-path="url(#sp)"><g>'
    f'<polygon points="{PX + 14:.1f},{sy} {poly(0)} {PX + 14 + BAR_W:.1f},{sy}" fill="url(#spark)"/>'
    f'<polyline points="{poly(0)}" fill="none" stroke="{C["cyan"]}" stroke-width="1.6" stroke-linejoin="round"/>'
    f'<polygon points="{PX + 14 + BAR_W:.1f},{sy} {poly(BAR_W)} {PX + 14 + 2 * BAR_W:.1f},{sy}" fill="url(#spark)"/>'
    f'<polyline points="{poly(BAR_W)}" fill="none" stroke="{C["cyan"]}" stroke-width="1.6" stroke-linejoin="round"/>'
    f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-BAR_W:.1f} 0" dur="9s" repeatCount="indefinite"/>'
    f'</g></g>')

# ---------------------------------------------------------------- status line (lualine-ish)
add(f'<rect x="0" y="{STATUS_Y}" width="{W}" height="24" fill="{C["bg_hl"]}"/>')
mode = f'<rect x="0" y="{STATUS_Y}" width="84" height="24" fill="{C["blue"]}"/>'
add(mode)
add(f'<text x="42" y="{STATUS_Y + 16.5}" font-size="12" font-weight="bold" fill="{C["bg"]}" text-anchor="middle">'
    f'<tspan>INSERT<set attributeName="display" to="none" begin="{T_END:.2f}s" fill="freeze"/></tspan></text>')
add(f'<text x="42" y="{STATUS_Y + 16.5}" font-size="12" font-weight="bold" fill="{C["bg"]}" text-anchor="middle" display="none">'
    f'NORMAL<set attributeName="display" to="inline" begin="{T_END:.2f}s" fill="freeze"/></text>')
# mode colour: insert = green, normal = blue
parts[-3] = (f'<rect x="0" y="{STATUS_Y}" width="84" height="24" fill="{C["green"]}">'
             f'<set attributeName="fill" to="{C["blue"]}" begin="{T_END:.2f}s" fill="freeze"/></rect>')
add(text(98, STATUS_Y + 16.5, " master", C["purple"], 12))
add(text(178, STATUS_Y + 16.5, "Alessandro.cs", C["fg"], 12))
add(text(W - 14, STATUS_Y + 16.5, "C#  utf-8  Cermenate, IT  45.70N 9.10E", C["dim"], 12, extra='text-anchor="end"'))

# ---------------------------------------------------------------- command line
add(f'<text x="12" y="{CMD_Y + 16}" font-size="12.5" fill="{C["fg"]}">:e Alessandro.cs'
    f'<set attributeName="display" to="none" begin="{T0:.2f}s" fill="freeze"/></text>')
add(f'<text x="12" y="{CMD_Y + 16}" font-size="12.5" fill="{C["dim"]}" display="none">-- INSERT --'
    f'<set attributeName="display" to="inline" begin="{T0:.2f}s" fill="freeze"/>'
    f'<set attributeName="display" to="none" begin="{T_END:.2f}s" fill="freeze"/></text>')
add(f'<text x="12" y="{CMD_Y + 16}" font-size="12.5" fill="{C["fg"]}" display="none">"Alessandro.cs" {len(CODE)}L written'
    f'<set attributeName="display" to="inline" begin="{T_END + 0.4:.2f}s" fill="freeze"/></text>')

add('</g>')
add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{C["border"]}"/>')
add('</svg>')

with open(OUT, "w") as f:
    f.write("\n".join(parts) + "\n")
print(f"wrote {OUT}, typing ends at {T_END:.1f}s")
