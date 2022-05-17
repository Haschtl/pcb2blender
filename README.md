[![freecad](https://img.shields.io/badge/blender-3.1.0-orange)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![freecad](https://img.shields.io/badge/kicad-6.0.5-blue)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![gplv3](https://img.shields.io/badge/license-GPLv3-lightgrey)](https://www.gnu.org/licenses/gpl-3.0.txt)

<img src="images/header.jpg"/>

The pcb2blender workflow lets you create professionally looking product renders of all your
KiCad projects in minutes! Simply export your board as a `.pcb3d` file in KiCad, import it into
Blender and start creating!

It lets you focus all your time on actually composing and lighting an interesting scene,
skipping all the boring cleanup work that would be required without it.

Its quick export/import times also make it viable to create renders of WIP boards or to update
them, after last minute board revisions.

<table><tr>
     <td><img src="images/pcb_material.jpg"/></td>
     <td><img src="images/breakout.jpg"/></td>
</tr></table>

## Usage

1. Hit the `Export to Blender (.pcb3d)` button in pcbnew.
2. Import the file in Blender via `File -> Import -> PCB (.pcb3d)`
3. Start creating awesome renders!

## Installation

### Exporter (KiCad)

- (not available yet) via the builtin plugin manager<br>
  `Tools -> Plugin and Content Manager -> Plugins -> pcb2blender`

- (manual) Download the `pcb2blender_exporter.zip` from the
  [latest release](https://github.com/30350n/pcb2blender/releases/latest),
  unpack the `plugins` directory from it into your
  [Kicad Plugin directory](https://dev-docs.kicad.org/en/python/pcbnew/) and rename it to
  `pcb2blender_exporter`.

### Importer (Blender)

- (manual) Download the `pcb2blender_importer.zip` from the
  [latest release](https://github.com/30350n/pcb2blender/releases/latest)
  and install it in Blender via<br>
  `Edit -> Preferences -> Add-ons -> Install`.<br>
  (You need to install the actual zip file, don't unpack it!)

## Other Projects

- The [protorack-kicad](https://github.com/30350n/protorack-kicad) KiCad library, contains
  all the custom symbols and footprints I use for eurorack module development.

- My [svg2blender](https://github.com/30350n/svg2blender) workflow enables you to export
  2D graphical designs from [Inkscape](https://inkscape.org/) to Blender. It's mainly intended
  for use with front panel designs, but could be used for other ones as well.

## Credits

- The name of this project is inspired by the awesome
  [svg2shenzhen](https://github.com/badgeek/svg2shenzhen) Inkscape extension by
  [badgeek](https://github.com/badgeek).

- The PCB Shader node setup this addon comes with is inspired by the
  [stylized-blender-setup](https://github.com/PCB-Arts/stylized-blender-setup)
  repository by [PCB-Arts](https://www.pcb-arts.com).

## License

- This project is licensed under
  [GPLv3](https://github.com/30350n/pcb2blender/blob/master/LICENSE).
